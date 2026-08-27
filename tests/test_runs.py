import os
import json
from pathlib import Path
from fastapi.testclient import TestClient


def setup_function(function):
    os.environ.pop("PROMPTGATE_KEY", None)


def teardown_function(function):
    os.environ.pop("PROMPTGATE_KEY", None)


def test_get_runs(tmp_path, monkeypatch):
    # Override the runs directory for testing
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    runs_log = runs_dir / "eval.jsonl"
    
    # Mock the log module to use the test directory
    import app.log
    original_run_log = app.log.RUN_LOG
    app.log.RUN_LOG = runs_log
    
    try:
        import sys
        sys.path.insert(0, 'E:\\promptgate')
        from app.main import app as app_instance
        client = TestClient(app_instance)
        
        # Perform a batch evaluation to create a log entry
        body = {
            "outputs": {
                "cap-fr": "The capital is Paris.",
                "cap-de": "The capital is Berlin."
            }
        }
        response = client.post("/eval/batch", json=body)
        assert response.status_code == 200
        
        # Get the runs
        response = client.get("/runs")
        assert response.status_code == 200
        data = response.json()
        assert "runs" in data
        assert len(data["runs"]) >= 1
        assert data["runs"][0]["passed_count"] == 2
    finally:
        # Restore the original log path
        app.log.RUN_LOG = original_run_log