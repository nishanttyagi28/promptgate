# PromptGate

A small FastAPI service and CLI that checks saved LLM answers against simple rules, so a prompt or model change that breaks an expected answer can fail a CI job.

[![Test Suite](https://github.com/nishanttyagi28/promptgate/actions/workflows/test.yml/badge.svg)](https://github.com/nishanttyagi28/promptgate/actions/workflows/test.yml)

You write each test case as a prompt plus the text a good answer must contain. Then you give PromptGate the answers your model produced. It reports pass or fail per case, and the CLI exits with status 1 if anything failed. PromptGate doesn't call a model itself. It only judges text you already have.

This is an early personal prototype.

## Install

Python 3.10 or newer.

```bash
git clone https://github.com/nishanttyagi28/promptgate.git
cd promptgate
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install fastapi uvicorn pydantic pytest httpx
```

Run everything from the repository root. (`pip install -e .` doesn't work yet; see Limitations.)

## Quick start

`cases/sample.json` defines two cases, and `cases/sample-outputs.json` holds the model answers, keyed by case ID:

```json
[
  {"id": "cap-fr", "prompt": "Capital of France?", "expect_contains": "Paris"},
  {"id": "cap-de", "prompt": "Capital of Germany?", "expect_contains": "Berlin"}
]
```

```json
{
  "cap-fr": "The capital of France is Paris.",
  "cap-de": "The capital of Germany is London."
}
```

```bash
python -m app.cli --cases cases/sample.json --outputs cases/sample-outputs.json --out results.json
```

```text
Passed: 1, Failed: 1
```

The exit code is 1 because `cap-de` failed. Per-case results are written to `results.json`, and a line is appended to `runs/eval.jsonl`.

## API

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
curl -s http://127.0.0.1:8000/eval -H 'Content-Type: application/json' -d '{
  "prompt": "What is the capital of France?",
  "expect_contains": "Paris",
  "output": "The capital is Paris."
}'
# {"passed":true}
```

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/` | Minimal HTML page to try `/eval` in a browser |
| GET | `/health` | Liveness check |
| GET | `/cases` | List the stored cases (`cases/sample.json` unless a SQLite store exists) |
| POST | `/eval` | Score one answer |
| POST | `/eval/batch` | Score answers (`{"outputs": {id: text}}`) against the stored cases |
| POST | `/eval/compare` | Compare baseline and candidate answers: newly failed, newly passed, unchanged |
| GET | `/runs` | Last 20 lines of `runs/eval.jsonl` |

If the environment variable `PROMPTGATE_KEY` is set, `POST /eval` and `POST /eval/batch` require a matching `x-api-key` header. Other endpoints are not protected.

## Matching rules

`app/eval.py` supports three modes: `contains` (the default), `exact` (after trimming whitespace) and `regex`. The CLI and `/eval` always use `contains`. `/eval/compare` reads a `match` field on each case.

## Layout

```text
app/main.py     FastAPI app
app/eval.py     matching rules and baseline/candidate comparison
app/cli.py      batch command
app/db.py       SQLite case store (path from PROMPTGATE_DB)
app/log.py      JSONL run history
cases/          sample cases, outputs and suites
static/         the HTML page served at /
tests/          pytest suite
```

## Limitations

- No model integration. You supply the outputs. There is a mock provider class, but no real one.
- `POST /cases` returns a 500 on a fresh checkout because the SQLite store isn't initialised first.
- `POST /eval/suite` and `POST /eval/run` currently return a 500 with the bundled suites in `cases/suites/`, because those files use `expect` while the case model expects `expect_contains`.
- The CLI's `--html` flag is accepted but doesn't generate a report yet.
- `pyproject.toml` has no package configuration, so `pip install .` fails. Install the dependencies directly as shown above.
- No login, multi-user support or hosting setup.

## Development

```bash
python -m pytest -q
```

`pytest.ini` sets `--basetemp` to a Windows path from the original machine. On other systems pytest creates a directory with that literal name. Pass `-o addopts=""` to skip it.

## License

No license file has been added to this repository yet.
