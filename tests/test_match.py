import pytest
from app.models import PromptCase
from app.eval import run_case


def test_match_contains():
    case = PromptCase(id="t1", prompt="Capital?", expect_contains="Paris")
    assert run_case(case, "The capital is Paris.")["passed"] is True
    assert run_case(case, "Paris is the capital.")["passed"] is True
    assert run_case(case, "The capital is Berlin.")["passed"] is False


def test_match_exact():
    case = PromptCase(id="t2", prompt="Capital?", expect_contains="Paris")
    assert run_case(case, "Paris", mode="exact")["passed"] is True
    assert run_case(case, " Paris ", mode="exact")["passed"] is True
    assert run_case(case, "The capital is Paris.", mode="exact")["passed"] is False


def test_match_regex():
    case = PromptCase(id="t3", prompt="Capital?", expect_contains=r"\bParis\b")
    assert run_case(case, "The capital is Paris.", mode="regex")["passed"] is True
    assert run_case(case, "Paris is the capital.", mode="regex")["passed"] is True
    assert run_case(case, "The capital is Berlin.", mode="regex")["passed"] is False