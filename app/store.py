import json
from pathlib import Path
from typing import List, Dict, Any


def load_cases(path: str) -> List[Dict[str, Any]]:
    """Load cases from a JSON file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'r') as f:
        return json.load(f)


def load_cases_from_db_or_file() -> List[Dict[str, Any]]:
    """Load cases from the database if it exists, otherwise from sample.json."""
    try:
        from .db import get_all_cases, get_db_path
        db_path = get_db_path()
        if db_path.exists():
            return get_all_cases()
    except Exception:
        pass
    
    # Fallback to sample.json
    sample_path = Path(__file__).parent.parent / "cases" / "sample.json"
    if sample_path.exists():
        return load_cases(str(sample_path))
    return []
import json
from pathlib import Path

def load_cases(path: str) -> list[dict]:
    """Load cases from a JSON file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'r') as f:
        return json.load(f)
