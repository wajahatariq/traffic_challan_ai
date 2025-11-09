# src/utils/id_generator.py

import uuid

def generate_challan_id() -> str:
    """
    Generate a unique challan ID using UUID4.
    Returns:
        str: A unique challan ID string.
    """
    return str(uuid.uuid4())


# Simple test when run as script
if __name__ == "__main__":
    print("Generated Challan ID:", generate_challan_id())
