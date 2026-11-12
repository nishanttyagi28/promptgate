import json
import os
from pathlib import Path


def _run_dir() -> Path:
    override = os.environ.get("PROMPTGATE_RUN_DIR")
    if override:
        return Path(override)
    if os.environ.get("VERCEL"):
        return Path("/tmp/promptgate-runs")
    return Path("runs")


RUN_DIR = _run_dir()
RUN_LOG = RUN_DIR / "eval.jsonl"


def _ensure_run_dir() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)


try:
    _ensure_run_dir()
except OSError:
    pass


def append_run(data: dict):
    _ensure_run_dir()
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
