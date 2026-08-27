import re
from typing import Literal
from .models import PromptCase

MatchMode = Literal["contains", "exact", "regex"]

def run_case(case: PromptCase, output: str, mode: MatchMode = "contains") -> dict:
    """Evaluate if the output matches the expected value based on the specified mode."""
    try:
        if mode == "contains":
            passed = case.expect_contains in output
        elif mode == "exact":
            passed = output.strip() == case.expect_contains.strip()
        elif mode == "regex":
            passed = bool(re.search(case.expect_contains, output))
        else:
            passed = False
        return {"passed": passed}
    except Exception:
        return {"passed": False}
