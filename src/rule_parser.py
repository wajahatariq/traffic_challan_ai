# src/rule_parser.py

from typing import List

def parse_violations(groq_response: str) -> List[str]:
    """
    Parse the Groq AI textual response and extract standardized violation codes.
    
    Args:
        groq_response (str): The raw text response from Groq describing violations.
        
    Returns:
        List[str]: List of detected violation strings.
    """
    response_lower = groq_response.lower()
    violations = []
    
    if "helmet" in response_lower:
        # Look for phrases indicating helmet violation
        if any(phrase in response_lower for phrase in ["no helmet", "without helmet", "not wearing helmet", "helmet violation"]):
            violations.append("No Helmet")
    
    if "seatbelt" in response_lower or "seat belt" in response_lower:
        if any(phrase in response_lower for phrase in ["no seatbelt", "without seatbelt", "not wearing seatbelt", "seatbelt violation"]):
            violations.append("No Seatbelt")
    
    if any(phrase in response_lower for phrase in ["triple riding", "three people", "more than two riders"]):
        violations.append("Triple Riding")
    
    # Add more rules as needed here
    
    # If no violations detected explicitly, optionally add "No Violations"
    if not violations:
        violations.append("No Violations Detected")
    
    return violations


# Simple test when run as script
if __name__ == "__main__":
    test_responses = [
        "The rider is not wearing a helmet and there are three people on the bike.",
        "Vehicle without seatbelt detected.",
        "All riders are compliant.",
        "No helmet violation but seatbelt violation observed."
    ]
    
    for resp in test_responses:
        print(f"Input: {resp}")
        print(f"Parsed Violations: {parse_violations(resp)}\n")
