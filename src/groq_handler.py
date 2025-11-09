# src/groq_handler.py

from typing import Optional
from ultralytics import YOLO

# Load the YOLO model - replace 'yolov8n.pt' with your custom weights if you have them
model = YOLO('yolov8n.pt')

def analyze_violation(image_path: str, ocr_text: Optional[str] = None) -> str:
    """
    Analyze vehicle image for traffic violations such as no helmet, no seatbelt, or triple riding.
    Uses YOLO object detection model.

    Args:
        image_path (str): Path to vehicle image.
        ocr_text (Optional[str]): OCR extracted number plate text (not used here but kept for interface consistency).

    Returns:
        str: Description of detected violations or "No visible violations detected."
    """
    results = model(image_path)
    detections = results[0]

    # Extract detected class labels from the model
    detected_labels = [model.names[int(cls)] for cls in detections.boxes.cls]

    # Basic heuristic violation detection:
    violations = []

    # If people detected but no helmet detected, it's a no helmet violation
    if 'person' in detected_labels and 'helmet' not in detected_labels:
        violations.append("No Helmet")

    # If person detected but no seatbelt detected, assume no seatbelt violation
    # (This depends on your model; many models do not detect seatbelts specifically)
    if 'person' in detected_labels and 'seatbelt' not in detected_labels:
        violations.append("No Seatbelt")

    # For triple riding, if number of persons > 2, flag triple riding
    person_count = detected_labels.count('person')
    if person_count > 2:
        violations.append("Triple Riding")

    if not violations:
        return "No visible violations detected."

    return ", ".join(violations)


# Test when run standalone
if __name__ == "__main__":
    test_image = "dataset/img_001.jpg"
    result = analyze_violation(test_image)
    print("YOLO Violation Analysis Result:")
    print(result)
