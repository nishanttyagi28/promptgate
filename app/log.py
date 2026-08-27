import json
from pathlib import Path

RUN_DIR = Path("runs")
RUN_DIR.mkdir(exist_ok=True)
RUN_LOG = RUN_DIR / "eval.jsonl"


def append_run(data: dict):
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")