import sqlite3
import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

# Database schema
SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS cases (
        id TEXT PRIMARY KEY,
        prompt TEXT NOT NULL,
        expect TEXT NOT NULL,
        match TEXT,
        suite TEXT,
        tags_json TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        passed_count INTEGER NOT NULL,
        failed_count INTEGER NOT NULL,
        payload_json TEXT NOT NULL
    );
    """
]


def get_db_path() -> Path:
    """Get the SQLite database path from environment or use default."""
    db_path = os.environ.get("PROMPTGATE_DB")
    if db_path:
        return Path(db_path)
    return Path(__file__).parent.parent / "data" / "promptgate.db"


def init_db() -> None:
    """Initialize the database with schema."""
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        for statement in SCHEMA:
            cursor.execute(statement)
        conn.commit()
    finally:
        conn.close()


def insert_case(
    prompt: str,
    expect: str,
    match: Optional[str] = None,
    suite: Optional[str] = None,
    tags_json: Optional[str] = None
) -> str:
    """Insert a new case into the database."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        case_id = f"case_{cursor.execute("SELECT COUNT(*) FROM cases").fetchone()[0] + 1}"
        
        cursor.execute(
            """
            INSERT INTO cases (id, prompt, expect, match, suite, tags_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (case_id, prompt, expect, match, suite, tags_json)
        )
        conn.commit()
        return case_id
    finally:
        conn.close()


def get_all_cases() -> List[Dict[str, Any]]:
    """Get all cases from the database."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, prompt, expect, match, suite, tags_json FROM cases")
        rows = cursor.fetchall()
        
        cases = []
        for row in rows:
            cases.append({
                "id": row[0],
                "prompt": row[1],
                "expect": row[2],
                "match": row[3],
                "suite": row[4],
                "tags_json": row[5]
            })
        return cases
    finally:
        conn.close()


def insert_run(ts: str, passed_count: int, failed_count: int, payload_json: str) -> int:
    """Insert a new run record."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO runs (ts, passed_count, failed_count, payload_json)
            VALUES (?, ?, ?, ?)
            """,
            (ts, passed_count, failed_count, payload_json)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_recent_runs(limit: int = 20) -> List[Dict[str, Any]]:
    """Get recent runs from the database."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, ts, passed_count, failed_count, payload_json
            FROM runs
            ORDER BY ts DESC
            LIMIT ?
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        
        runs = []
        for row in rows:
            runs.append({
                "id": row[0],
                "ts": row[1],
                "passed_count": row[2],
                "failed_count": row[3],
                "payload_json": row[4]
            })
        return runs
    finally:
        conn.close()