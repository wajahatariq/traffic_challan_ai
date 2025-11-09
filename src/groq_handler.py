# src/groq_handler.py

import os
from typing import Optional
from groq_client import GroqClient  # Assuming you have the Groq Python SDK installed

# Initialize the Groq client with your API key (set in environment variables)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY environment variable not set")

client = GroqClient(api_key=GROQ_API_KEY)

def analyze_violation(image_path: str, ocr_text: Optional[str] = None) -> str:
    """
    Sends the vehicle image and optional OCR text to Groq for violation analysis.
    
    Args:
        image_path (str): Path to the vehicle image.
        ocr_text (Optional[str]): Extracted number plate text to include in the prompt.
        
    Returns:
        str: Groq's textual response describing detected violations.
    """
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    
    prompt = (
        "Analyze the following image of a vehicle. "
        "Identify any visible traffic violations such as helmet violation, seatbelt violation, "
        "triple riding, or other visible infractions. "
    )
    if ocr_text:
        prompt += f"The vehicle number plate reads: {ocr_text}. "
    prompt += "Return a clear and concise description of all violations."
    
    response = client.predict(
        prompt=prompt,
        image=image_bytes,
        max_tokens=150,
        temperature=0.2
    )
    
    return response.get("text", "").strip()


# Simple test when run as script
if __name__ == "__main__":
    test_image = "dataset/img_001.jpg"
    result = analyze_violation(test_image)
    print("Groq Violation Analysis Result:")
    print(result)
