import os
import json
from datetime import datetime


def save_output(result: dict, filename: str = None) -> str:
    """Persist a generated post result to the outputs/ directory as JSON."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"post_{timestamp}.json"

    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)

    filepath = os.path.join(outputs_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Saved to {filepath}")
    return filepath
