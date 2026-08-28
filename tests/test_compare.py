import pytest
from app.eval import compare_outputs


def test_compare_outputs_newly_failed():
    """Test that newly failed cases are detected."""
    baseline_outputs = {
        "case1": "passed",
        "case2": "passed"
    }
    candidate_outputs = {
        "case1": "failed",
        "case2": "passed"
    }
    cases = [
        {"id": "case1", "prompt": "Test 1", "expect": "passed", "match": "exact"},
        {"id": "case2", "prompt": "Test 2", "expect": "passed", "match": "exact"}
    ]
    
    result = compare_outputs(baseline_outputs, candidate_outputs, cases)
    assert result["newly_failed"] == 1
    assert result["newly_passed"] == 0
    assert result["unchanged"] == 1


def test_compare_outputs_newly_passed():
    """Test that newly passed cases are detected."""
    baseline_outputs = {
        "case1": "failed",
        "case2": "passed"
    }
    candidate_outputs = {
        "case1": "passed",
        "case2": "passed"
    }
    cases = [
        {"id": "case1", "prompt": "Test 1", "expect": "passed", "match": "exact"},
        {"id": "case2", "prompt": "Test 2", "expect": "passed", "match": "exact"}
    ]
    
    result = compare_outputs(baseline_outputs, candidate_outputs, cases)
    assert result["newly_failed"] == 0
    assert result["newly_passed"] == 1
    assert result["unchanged"] == 1


def test_compare_outputs_unchanged():
    """Test that unchanged cases are detected."""
    baseline_outputs = {
        "case1": "passed",
        "case2": "passed"
    }
    candidate_outputs = {
        "case1": "passed",
        "case2": "passed"
    }
    cases = [
        {"id": "case1", "prompt": "Test 1", "expect": "passed", "match": "exact"},
        {"id": "case2", "prompt": "Test 2", "expect": "passed", "match": "exact"}
    ]
    
    result = compare_outputs(baseline_outputs, candidate_outputs, cases)
    assert result["newly_failed"] == 0
    assert result["newly_passed"] == 0
    assert result["unchanged"] == 2


def test_compare_outputs_mixed():
    """Test a mix of newly failed, newly passed, and unchanged cases."""
    baseline_outputs = {
        "case1": "passed",
        "case2": "failed",
        "case3": "passed"
    }
    candidate_outputs = {
        "case1": "failed",
        "case2": "passed",
        "case3": "passed"
    }
    cases = [
        {"id": "case1", "prompt": "Test 1", "expect": "passed", "match": "exact"},
        {"id": "case2", "prompt": "Test 2", "expect": "passed", "match": "exact"},
        {"id": "case3", "prompt": "Test 3", "expect": "passed", "match": "exact"}
    ]
    
    result = compare_outputs(baseline_outputs, candidate_outputs, cases)
    assert result["newly_failed"] == 1
    assert result["newly_passed"] == 1
    assert result["unchanged"] == 1


def test_compare_outputs_empty():
    """Test with empty outputs."""
    baseline_outputs = {}
    candidate_outputs = {}
    cases = [
        {"id": "case1", "prompt": "Test 1", "expect": "passed", "match": "exact"}
    ]
    
    result = compare_outputs(baseline_outputs, candidate_outputs, cases)
    assert result["newly_failed"] == 0
    assert result["newly_passed"] == 0
    assert result["unchanged"] == 0


def test_compare_outputs_contains_match():
    """Test with contains match mode."""
    baseline_outputs = {
        "case1": "This is a test",
        "case2": "Another test"
    }
    candidate_outputs = {
        "case1": "This is a different test",
        "case2": "Another test"
    }
    cases = [
        {"id": "case1", "prompt": "Test 1", "expect": "test", "match": "contains"},
        {"id": "case2", "prompt": "Test 2", "expect": "test", "match": "contains"}
    ]
    
    result = compare_outputs(baseline_outputs, candidate_outputs, cases)
    assert result["newly_failed"] == 0
    assert result["newly_passed"] == 0
    assert result["unchanged"] == 2