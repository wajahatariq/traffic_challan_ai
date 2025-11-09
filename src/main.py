# src/main.py

import os
from src.utils.id_generator import generate_challan_id
from src.ocr import extract_number_plate
from src.groq_handler import analyze_violation
from src.rule_parser import parse_violations
from src.challan_generator import generate_challan_pdf

# Configuration
DATASET_DIR = "dataset"
OUTPUT_DIR = "output/challans"
# Define fine amounts for each violation type
FINE_AMOUNTS = {
    "No Helmet": 500,
    "No Seatbelt": 300,
    "Triple Riding": 700,
    # Add more violation fines as needed
}

def calculate_total_fine(violations):
    total = 0
    for v in violations:
        total += FINE_AMOUNTS.get(v, 0)
    return total

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Iterate over all images in the dataset folder
    image_files = [f for f in os.listdir(DATASET_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print("No images found in dataset folder.")
        return

    for image_file in image_files:
        image_path = os.path.join(DATASET_DIR, image_file)
        print(f"Processing image: {image_path}")

        # Step 1: Extract vehicle number plate using OCR
        plate_text = extract_number_plate(image_path)
        if plate_text is None:
            plate_text = "UNKNOWN"
        print(f"Extracted Number Plate: {plate_text}")

        # Step 2: Send image + plate text to Groq for violation detection
        groq_response = analyze_violation(image_path, ocr_text=plate_text)
        print(f"Groq Response: {groq_response}")

        # Step 3: Parse Groq response into violation list
        violations = parse_violations(groq_response)
        print(f"Detected Violations: {violations}")

        # Step 4: Calculate total fine amount
        total_fine = calculate_total_fine(violations)
        print(f"Total Fine: ₹{total_fine}")

        # Step 5: Generate unique challan ID
        challan_id = generate_challan_id()

        # Step 6: Generate and save challan PDF
        pdf_filename = f"challan_{challan_id}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
        generate_challan_pdf(
            challan_id=challan_id,
            vehicle_number=plate_text,
            violations=violations,
            challan_amount=total_fine,
            output_path=pdf_path
        )
        print(f"Challan PDF generated: {pdf_path}\n")

if __name__ == "__main__":
    main()
