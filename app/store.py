import json
from pathlib import Path

def load_cases(path: str) -> list[dict]:
    """Load cases from a JSON file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'r') as f:
        return json.load(f)
