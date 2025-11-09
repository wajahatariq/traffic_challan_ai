# src/challan_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
import os

def generate_challan_pdf(
    challan_id: str,
    vehicle_number: str,
    violations: list,
    challan_amount: int,
    output_path: str
):
    """
    Generate a PDF challan with the given details.
    
    Args:
        challan_id (str): Unique challan identifier.
        vehicle_number (str): Extracted vehicle number plate.
        violations (list): List of violations detected.
        challan_amount (int): Total fine amount.
        output_path (str): File path to save the generated PDF.
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    margin = 30
    y_position = height - margin
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y_position, "Traffic Violation Challan")
    y_position -= 40
    
    # Challan ID and timestamp
    c.setFont("Helvetica", 12)
    c.drawString(margin, y_position, f"Challan ID: {challan_id}")
    c.drawRightString(width - margin, y_position, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y_position -= 30
    
    # Vehicle Number
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y_position, f"Vehicle Number: {vehicle_number}")
    y_position -= 25
    
    # Violations Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y_position, "Violations Detected:")
    y_position -= 20
    
    # List Violations
    c.setFont("Helvetica", 12)
    for violation in violations:
        c.drawString(margin + 15, y_position, f"- {violation}")
        y_position -= 18
    
    y_position -= 10
    
    # Challan Amount
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.red)
    c.drawString(margin, y_position, f"Total Fine Amount: ₹{challan_amount}")
    c.setFillColor(colors.black)
    
    y_position -= 40
    
    # Footer / Disclaimer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin, y_position, "Please pay your challan online or at the nearest traffic police station.")
    
    c.showPage()
    c.save()


# Simple test when run as script
if __name__ == "__main__":
    test_id = "123e4567-e89b-12d3-a456-426614174000"
    test_vehicle = "ABC-1234"
    test_violations = ["No Helmet", "No Seatbelt"]
    test_amount = 800
    output_file = "output/challans/test_challan.pdf"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    generate_challan_pdf(test_id, test_vehicle, test_violations, test_amount, output_file)
    print(f"Challan PDF generated at {output_file}")
