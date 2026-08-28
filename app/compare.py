# PromptGate Compare Module

from typing import Dict, List, TypedDict


class ComparisonResult(TypedDict):
    newly_failed: int
    newly_passed: int
    unchanged: int


def compare_outputs(
    baseline_outputs: Dict[str, str],
    candidate_outputs: Dict[str, str],
    cases: List[Dict[str, str]]
) -> ComparisonResult:
    """Compare baseline and candidate outputs against test cases.

    Args:
        baseline_outputs: Dictionary mapping case IDs to baseline outputs.
        candidate_outputs: Dictionary mapping case IDs to candidate outputs.
        cases: List of test case dictionaries with 'id', 'prompt', 'expect', and 'match' keys.

    Returns:
        A dictionary with counts of newly failed, newly passed, and unchanged cases.
    """
    newly_failed = 0
    newly_passed = 0
    unchanged = 0

    for case in cases:
        case_id = case["id"]
        expected = case["expect"]
        match_mode = case.get("match", "exact")

        baseline = baseline_outputs.get(case_id, None)
        candidate = candidate_outputs.get(case_id, None)

        # Determine if baseline case passed
        baseline_passed = baseline == expected if baseline is not None else False

        # Determine if candidate case passed
        if match_mode == "exact":
            candidate_passed = candidate == expected if candidate is not None else False
        elif match_mode == "contains":
            candidate_passed = expected in candidate if candidate is not None else False
        else:
            candidate_passed = candidate == expected if candidate is not None else False

        # Compare changes
        if baseline_passed and not candidate_passed:
            newly_failed += 1
        elif not baseline_passed and candidate_passed:
            newly_passed += 1
        elif baseline_passed and candidate_passed:
            unchanged += 1

    return {
        "newly_failed": newly_failed,
        "newly_passed": newly_passed,
        "unchanged": unchanged,
    }