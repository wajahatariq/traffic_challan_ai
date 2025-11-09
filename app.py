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
    st.set_page_config(page_title="Traffic Violation Detection", layout="centered")
    st.title("Traffic Violation Detection & E-Challan Generator")

    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Vehicle Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        temp_img_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(temp_img_path, caption="Uploaded Image", use_column_width=True)

        plate_text = extract_number_plate(temp_img_path)
        st.markdown(f"**Extracted Number Plate:** {plate_text if plate_text else 'Not detected'}")

        # Pass the client and image path to groq_handler
        groq_response = analyze_violation(client, temp_img_path, ocr_text=plate_text or "")
        st.markdown(f"**Violation Analysis:** {groq_response}")

        violations = parse_violations(groq_response)
        st.markdown("**Detected Violations:**")
        for v in violations:
            st.write(f"- {v}")

        FINE_AMOUNTS = {
            "No Helmet": 500,
            "No Seatbelt": 300,
            "Triple Riding": 700,
        }
        total_fine = sum(FINE_AMOUNTS.get(v, 0) for v in violations)
        st.markdown(f"**Total Fine Amount:** ₹{total_fine}")

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
            st.download_button(
                label="Download Challan PDF",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
