import os
import pytest
from fastapi.testclient import TestClient
from app.main import app


def setup_function(function):
    os.environ.pop("PROMPTGATE_KEY", None)


def teardown_function(function):
    os.environ.pop("PROMPTGATE_KEY", None)


def test_get_cases():
    client = TestClient(app)
    response = client.get("/cases")
    assert response.status_code == 200
    data = response.json()
    assert "cases" in data
    assert len(data["cases"]) == 2
    assert data["cases"][0]["id"] == "cap-fr"
    assert data["cases"][1]["id"] == "cap-de"


def test_eval_batch():
    client = TestClient(app)
    body = {
        "outputs": {
            "cap-fr": "The capital is Paris.",
            "cap-de": "The capital is London."
        }
    }
    response = client.post("/eval/batch", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["passed_count"] == 1
    assert data["failed_count"] == 1
    assert len(data["results"]) == 2
    assert data["results"][0]["id"] == "cap-fr"
    assert data["results"][0]["passed"] is True
    assert data["results"][1]["id"] == "cap-de"
    assert data["results"][1]["passed"] is False