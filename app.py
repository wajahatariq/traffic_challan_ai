import streamlit as st
import os
from src.ocr import extract_number_plate
from src.groq_handler import get_client, analyze_violation
from src.rule_parser import parse_violations
from src.utils.id_generator import generate_challan_id
from src.challan_generator import generate_challan_pdf

# Access Groq API key from Streamlit secrets
GROQ_API_KEY = st.secrets["groq"]["api_key"]
client = get_client(GROQ_API_KEY)

OUTPUT_DIR = "output/challans"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    st.set_page_config(page_title="Traffic Violation & Challan Generator", layout="centered")
    st.title("🚦 Traffic Violation Detection & E-Challan Generator")

    # Load custom CSS styling if available
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    st.markdown("Upload a clear vehicle image for violation detection.")

    uploaded_file = st.file_uploader("Upload Vehicle Image", type=["jpg", "jpeg", "png"])
    if not uploaded_file:
        st.info("Please upload an image to start.")
        return

    # Save the uploaded file temporarily
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_img_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(temp_img_path, caption="Uploaded Vehicle Image", use_column_width=True)

    with st.spinner("Extracting number plate..."):
        plate_text = extract_number_plate(temp_img_path)

    st.markdown(f"**Extracted Number Plate:** {plate_text if plate_text else 'Not detected'}")

    with st.spinner("Analyzing violations..."):
        groq_response = analyze_violation(client, temp_img_path, ocr_text=plate_text or "")

    st.markdown("### Violation Analysis Result")
    st.write(groq_response)

    violations = parse_violations(groq_response)
    if violations:
        st.markdown("### Detected Violations")
        for v in violations:
            st.write(f"- {v}")
    else:
        st.success("No violations detected.")

    FINE_AMOUNTS = {
        "No Helmet": 500,
        "No Seatbelt": 300,
        "Triple Riding": 700,
    }
    total_fine = sum(FINE_AMOUNTS.get(v, 0) for v in violations)

    st.markdown(f"### Total Fine Amount: ₹{total_fine}")

    if violations:
        if st.button("Generate Challan PDF"):
            challan_id = generate_challan_id()
            pdf_filename = f"challan_{challan_id}.pdf"
            pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

            generate_challan_pdf(
                challan_id=challan_id,
                vehicle_number=plate_text or "UNKNOWN",
                violations=violations,
                challan_amount=total_fine,
                output_path=pdf_path
            )

            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.success("Challan generated successfully!")
            st.download_button(
                label="Download Challan PDF",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf"
            )
    else:
        st.info("No challan generated as no violations were detected.")

if __name__ == "__main__":
    main()
