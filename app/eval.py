import re
import json
from typing import Literal, List, Dict, Any
from pathlib import Path
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


def load_suite(suite: str) -> List[Dict[str, Any]]:
    """Load a test suite from JSON file."""
    suite_path = Path(__file__).parent.parent / "cases" / "suites" / f"{suite}.json"
    if not suite_path.exists():
        raise FileNotFoundError(f"Suite file not found: {suite_path}")
    with open(suite_path, 'r') as f:
        return json.load(f)


def compare_outputs(
    baseline_outputs: Dict[str, str],
    candidate_outputs: Dict[str, str],
    cases: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compare baseline outputs with candidate outputs for a set of cases.
    Returns newly_failed, newly_passed, unchanged counts and details.
    """
    newly_failed = 0
    newly_passed = 0
    unchanged = 0
    details = []
    
    for case in cases:
        case_id = case["id"]
        prompt = case["prompt"]
        expect = case["expect"]
        match_mode = case.get("match", "contains")
        
        baseline_output = baseline_outputs.get(case_id, "")
        candidate_output = candidate_outputs.get(case_id, "")
        
        # Determine if baseline passed
        baseline_case = PromptCase(id=case_id, prompt=prompt, expect_contains=expect)
        baseline_result = run_case(baseline_case, baseline_output, match_mode)
        baseline_passed = baseline_result["passed"]
        
        # Determine if candidate passed
        candidate_result = run_case(baseline_case, candidate_output, match_mode)
        candidate_passed = candidate_result["passed"]
        
        # Calculate changes
        if baseline_passed and not candidate_passed:
            newly_failed += 1
        elif not baseline_passed and candidate_passed:
            newly_passed += 1
        elif baseline_passed and candidate_passed:
            unchanged += 1
        
        details.append({
            "id": case_id,
            "prompt": prompt,
            "expect": expect,
            "baseline_passed": baseline_passed,
            "candidate_passed": candidate_passed,
            "baseline_output": baseline_output,
            "candidate_output": candidate_output
        })
    
    return {
        "newly_failed": newly_failed,
        "newly_passed": newly_passed,
        "unchanged": unchanged,
        "details": details
    }
