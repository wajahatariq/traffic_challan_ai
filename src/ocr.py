# src/ocr.py

import easyocr
import cv2
import numpy as np
from typing import Optional

# Initialize EasyOCR reader (English only, GPU support if available)
reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load and preprocess the image for better OCR performance.
    
    Args:
        image_path (str): Path to the vehicle image.
        
    Returns:
        np.ndarray: Preprocessed image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Optional: Apply bilateral filter to reduce noise while preserving edges
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)
    
    # Optional: Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    
    return thresh

def extract_number_plate(image_path: str) -> Optional[str]:
    """
    Extract the vehicle number plate text from the image using EasyOCR.
    
    Args:
        image_path (str): Path to the vehicle image.
        
    Returns:
        Optional[str]: Extracted number plate text or None if not found.
    """
    processed_image = preprocess_image(image_path)
    
    # Perform OCR on the processed image
    results = reader.readtext(processed_image)
    
    # Combine detected text segments that likely form the plate
    # This is a simple heuristic; more advanced filtering can be added later
    plate_texts = []
    for (bbox, text, confidence) in results:
        if confidence > 0.4:  # threshold to filter out low confidence text
            plate_texts.append(text)
    
    if plate_texts:
        # Join the texts with spaces or no space depending on format
        return " ".join(plate_texts).strip()
    else:
        return None


# Simple test when run as script
if __name__ == "__main__":
    test_image = "dataset/img_001.jpg"
    plate = extract_number_plate(test_image)
    print(f"Extracted Number Plate: {plate}")
