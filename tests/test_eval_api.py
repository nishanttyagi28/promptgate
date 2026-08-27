import os
import pytest
from fastapi.testclient import TestClient
from app.main import app


def setup_function(function):
    os.environ.pop("PROMPTGATE_KEY", None)


def teardown_function(function):
    os.environ.pop("PROMPTGATE_KEY", None)


def test_eval_passing():
    client = TestClient(app)
    body = {
        "prompt": "What is the capital of France?",
        "expect_contains": "Paris",
        "output": "The capital is Paris."
    }
    response = client.post("/eval", json=body)
    assert response.status_code == 200
    assert response.json()["passed"] is True


def test_eval_failing():
    client = TestClient(app)
    body = {
        "prompt": "What is the capital of France?",
        "expect_contains": "Berlin",
        "output": "The capital is Paris."
    }
    response = client.post("/eval", json=body)
    assert response.status_code == 200
    assert response.json()["passed"] is False