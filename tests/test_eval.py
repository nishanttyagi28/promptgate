import pytest
from app.models import PromptCase
from app.eval import run_case

@pytest.fixture
def passing_case():
    return PromptCase(
        id="test1",
        prompt="What is the capital of France?",
        expect_contains="Paris"
    )

def test_run_case(passing_case):
    result = run_case(passing_case, "The capital of France is Paris.")
    assert result["passed"] is True
