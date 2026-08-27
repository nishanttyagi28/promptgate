# PromptGate

A small tool that checks whether an AI answer matches what you asked for.

You write a question and a rule (for example: “the answer must mention Paris”).
You paste the model’s answer.
PromptGate says **pass** or **fail**.

It does **not** talk to ChatGPT, Ollama, or any AI model.
It only judges text you already have.

This repo is an early prototype by [Nishant Tyagi](https://github.com/nishanttyagi28).
It is useful as a demo and a starting point for freelance work.
It is **not** a finished product and will not be built into a large production SaaS unless real clients appear.

---

## The business problem (plain language)

Companies now put AI into apps, support bots, and internal tools.

Three things keep breaking:

1. **The prompt changes** and nobody notices the answers got worse.
2. **The model vendor changes** (or the model version) and old answers no longer match.
3. **The coding agent says “done”** but nobody ran a real check.

Software teams already have unit tests for code.
They almost never have the same thing for prompts.

That gap costs money: bad answers in front of customers, extra manual review, and arguments about whether “it works.”

---

## The idea / vision

Treat a prompt like a contract.

- Freeze a small set of example questions.
- Freeze what a good answer must contain (a word, an exact sentence, or a pattern).
- After every prompt edit or model change, run the same examples.
- If something fails, CI can fail. No guessing.

Long-term (only if someone pays for it):

- A folder of prompt cases per client
- A button or command that scores a batch of model outputs
- A short report: passed / failed / cost later if a model is wired in
- Optional private API key so only the client’s app can call it

Not the vision: another ChatGPT clone, another multi-tenant cloud, another “AI gateway” like promptgate.dev.

---

## What this software does today

| You give | You get |
|----------|---------|
| A case (question + rule) and a model answer | `{ "passed": true/false }` |
| A batch of answers keyed by case id | Counts + per-case results |
| A CLI run | `results.json`, a log line in `runs/eval.jsonl`, exit code 1 if anything failed |

Rules a case can use:

- **contains** — answer must include this text (default)
- **exact** — answer must match exactly
- **regex** — answer must match a pattern

Optional: set environment variable `PROMPTGATE_KEY`. Then write endpoints require header `x-api-key`.

---

## What is already built

Working on Windows with Python 3.14.

- HTTP API (FastAPI)
  - `GET /health` — is the server up
  - `GET /cases` — sample questions
  - `POST /eval` — score one answer
  - `POST /eval/batch` — score many
  - `GET /runs` — recent log lines
- Command line: `python -m app.cli ...`
- Sample cases under `cases/`
- Automated tests: **16 passed** last run (only FastAPI / Python 3.14 warnings)

This is enough to show a client: “here is how we freeze a prompt and fail the build when the answer drifts.”

---

## What is not built (do not sell these yet)

- No live call to any LLM
- No website / dashboard
- No login, teams, or billing
- No Docker / cloud deploy pack
- No multi-tenant SaaS
- No “enterprise ready” scale
- No comparison against other products named PromptGate

If this never becomes freelance work, it stays a portfolio prototype. That is an acceptable outcome.

---

## Who this is for

- A founder who wants prompt checks in CI before they hire a big vendor
- A freelancer who delivers LLM features and needs proof the prompts did not regress
- A student / junior engineer showing they can ship a small, honest tool

Not for: replacing LangSmith, PromptLayer, or a full AI gateway.

---

## How to run (Windows)

Need Python 3.11+ (`C:\Python314\python.exe` on the original machine).

```powershell
cd E:\promptgate
C:\Python314\python.exe -m pip install fastapi uvicorn pydantic pytest httpx
Tests:
PowerShellC:\Python314\python.exe -m pytest -q --tb=short --basetemp=E:\promptgate\.pytest-tmp
Score a batch from files:
PowerShellC:\Python314\python.exe -m app.cli --cases cases\sample.json --outputs cases\sample-outputs.json --out results.json
Start the API:
PowerShellC:\Python314\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
Open: http://127.0.0.1:8000/health

Example
Request to POST /eval:
JSON{
  "prompt": "What is the capital of France?",
  "expect_contains": "Paris",
  "output": "The capital is Paris."
}
Response:
JSON{ "passed": true }
If the output had been “The capital is Berlin.” → passed: false.

Project layout
textapp/main.py     API
app/eval.py     pass/fail rules
app/store.py    load cases from JSON
app/cli.py      batch command
app/log.py      JSONL history
cases/          example questions and answers
tests/          automated tests

Freelance / next step
Possible paid slice if a client appears:

Wire their real model outputs into POST /eval/batch
Keep 20–50 golden cases in cases/
Fail their CI when failed_count > 0

Until that request exists, do not grow this into a platform.

License / status
Personal prototype. No company, no SLA, no support promise.