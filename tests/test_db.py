import os
import tempfile
import pytest
import sqlite3
from pathlib import Path
from datetime import datetime

# Set up a temporary database for testing
@pytest.fixture
def temp_db_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        os.environ["PROMPTGATE_DB"] = str(db_path)
        yield db_path
        if "PROMPTGATE_DB" in os.environ:
            del os.environ["PROMPTGATE_DB"]


def test_init_db(temp_db_path):
    from app.db import init_db, get_db_path
    
    init_db()
    assert temp_db_path.exists()
    
    conn = sqlite3.connect(str(temp_db_path))
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "cases" in tables
        assert "runs" in tables
    finally:
        conn.close()


def test_insert_and_get_cases(temp_db_path):
    from app.db import init_db, insert_case, get_all_cases
    
    init_db()
    
    # Insert a case
    case_id = insert_case(
        prompt="Test prompt",
        expect="Test expect",
        match="exact",
        suite="test_suite",
        tags_json='["tag1", "tag2"]'
    )
    
    cases = get_all_cases()
    assert len(cases) == 1
    assert cases[0]["id"] == case_id
    assert cases[0]["prompt"] == "Test prompt"
    assert cases[0]["expect"] == "Test expect"
    assert cases[0]["match"] == "exact"
    assert cases[0]["suite"] == "test_suite"
    assert cases[0]["tags_json"] == '["tag1", "tag2"]'


def test_insert_multiple_cases(temp_db_path):
    from app.db import init_db, insert_case, get_all_cases
    
    init_db()
    
    # Insert multiple cases
    case_id1 = insert_case(prompt="Prompt 1", expect="Expect 1")
    case_id2 = insert_case(prompt="Prompt 2", expect="Expect 2")
    
    cases = get_all_cases()
    assert len(cases) == 2
    assert cases[0]["id"] == case_id1
    assert cases[1]["id"] == case_id2


def test_insert_and_get_runs(temp_db_path):
    from app.db import init_db, insert_run, get_recent_runs
    import json
    
    init_db()
    
    # Insert a run
    payload = {"test": "data"}
    run_id = insert_run(
        ts=datetime.now().isoformat(),
        passed_count=5,
        failed_count=2,
        payload_json=json.dumps(payload)
    )
    
    runs = get_recent_runs()
    assert len(runs) == 1
    assert runs[0]["id"] == run_id
    assert runs[0]["passed_count"] == 5
    assert runs[0]["failed_count"] == 2
    assert json.loads(runs[0]["payload_json"]) == payload


def test_get_recent_runs_limit(temp_db_path):
    from app.db import init_db, insert_run, get_recent_runs
    import json
    
    init_db()
    
    # Insert multiple runs
    for i in range(5):
        insert_run(
            ts=datetime.now().isoformat(),
            passed_count=i,
            failed_count=0,
            payload_json=json.dumps({"index": i})
        )
    
    runs = get_recent_runs(limit=3)
    assert len(runs) == 3


def test_db_path_from_env(temp_db_path):
    from app.db import get_db_path
    
    assert get_db_path() == temp_db_path
