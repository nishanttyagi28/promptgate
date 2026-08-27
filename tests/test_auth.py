import os
import pytest
from fastapi.testclient import TestClient


def test_missing_api_key_eval():
    os.environ["PROMPTGATE_KEY"] = "test_key_123"
    from app.main import app
    client = TestClient(app)
    body = {"prompt": "What is the capital of France?", "expect_contains": "Paris", "output": "The capital of France is Paris."}
    response = client.post("/eval", json=body)
    assert response.status_code == 401


def test_correct_api_key_eval():
    os.environ["PROMPTGATE_KEY"] = "test_key_123"
    from app.main import app
    client = TestClient(app)
    body = {"prompt": "What is the capital of France?", "expect_contains": "Paris", "output": "The capital of France is Paris."}
    response = client.post("/eval", json=body, headers={"x-api-key": "test_key_123"})
    assert response.status_code == 200


def test_missing_api_key_eval_batch():
    os.environ["PROMPTGATE_KEY"] = "test_key_123"
    from app.main import app
    client = TestClient(app)
    body = {"outputs": {"cap-france": "The capital of France is Paris."}}
    response = client.post("/eval/batch", json=body)
    assert response.status_code == 401


def test_correct_api_key_eval_batch():
    os.environ["PROMPTGATE_KEY"] = "test_key_123"
    from app.main import app
    client = TestClient(app)
    body = {"outputs": {"cap-france": "The capital of France is Paris."}}
    response = client.post("/eval/batch", json=body, headers={"x-api-key": "test_key_123"})
    assert response.status_code == 200


def teardown_function():
    os.environ.pop("PROMPTGATE_KEY", None)