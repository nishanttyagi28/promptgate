import json
import pytest
from pathlib import Path
from app.cli import main


def test_cli_success(tmp_path, monkeypatch):
    cases_file = tmp_path / "cases.json"
    outputs_file = tmp_path / "outputs.json"
    results_file = tmp_path / "results.json"
    
    cases_file.write_text('[{"id":"cap-fr","prompt":"Capital of France?","expect_contains":"Paris"}]')
    outputs_file.write_text('{"cap-fr":"The capital is Paris."}')
    
    def mock_args():
        class Args:
            cases = str(cases_file)
            outputs = str(outputs_file)
            out = str(results_file)
        return Args()
    
    monkeypatch.setattr("app.cli.argparse.ArgumentParser.parse_args", lambda _: mock_args())
    
    exit_code = main()
    assert exit_code == 0
    
    assert results_file.exists()
    with results_file.open() as f:
        results = json.load(f)
    assert results["passed_count"] == 1
    assert results["failed_count"] == 0


def test_cli_failure(tmp_path, monkeypatch):
    cases_file = tmp_path / "cases.json"
    outputs_file = tmp_path / "outputs.json"
    results_file = tmp_path / "results.json"
    
    cases_file.write_text('[{"id":"cap-fr","prompt":"Capital of France?","expect_contains":"Paris"}]')
    outputs_file.write_text('{"cap-fr":"The capital is London."}')
    
    def mock_args():
        class Args:
            cases = str(cases_file)
            outputs = str(outputs_file)
            out = str(results_file)
        return Args()
    
    monkeypatch.setattr("app.cli.argparse.ArgumentParser.parse_args", lambda _: mock_args())
    
    exit_code = main()
    assert exit_code == 1
    
    assert results_file.exists()
    with results_file.open() as f:
        results = json.load(f)
    assert results["passed_count"] == 0
    assert results["failed_count"] == 1