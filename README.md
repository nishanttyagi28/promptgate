# PromptGate

A small tool that checks whether an AI answer matches what you asked for.

You write a question and a rule (for example: "the answer must mention Paris").
You paste the model's answer.
PromptGate says **pass** or **fail**.

It does **not** talk to ChatGPT, Ollama, or any AI model. It only judges text you already have.

This repo is an early prototype by [Nishant Tyagi](https://github.com/nishanttyagi28). It is a demo and a possible freelance starting point. It is **not** a finished product and will not become a large SaaS unless real clients appear.

## The business problem

Companies put AI into apps, support bots, and internal tools. Three things keep breaking:

1. The prompt changes and nobody notices the answers got worse.
2. The model or vendor changes and old answers no longer match.
3. A coding agent says "done" but nobody ran a real check.

Teams already unit-test code. They almost never test prompts the same way. That gap means bad customer-facing answers, extra manual review, and arguments about whether the feature works.

## Vision

Treat a prompt like a contract.

- Freeze a small set of example questions.
- Freeze what a good answer must contain (a phrase, an exact sentence, or a pattern).
- After every prompt or model change, run the same examples.
- If a case fails, the command can exit non-zero so CI can fail.

Only if someone pays: per-client case folders, a batch report, optional API key, later a model hook for cost. Not in scope: a ChatGPT clone, multi-tenant cloud, or an AI gateway like promptgate.dev.

## What it does today

| You give | You get |
| --- | --- |
| One case (question + rule) and a model answer | {"passed": true} or false |
| A batch of answers keyed by case id | Per-case results and counts |
| A CLI run | results.json, a line in runs/eval.jsonl, exit code 1 if anything failed |

Match rules: **contains** (default), **exact**, **regex**.

If environment variable PROMPTGATE_KEY is set, POST /eval and POST /eval/batch require header x-api-key.

## Already built

Windows + Python 3.14.

- GET /health — server up
- GET /cases — sample questions
- POST /eval — score one answer
- POST /eval/batch — score many
- GET /runs — recent log lines
- CLI: python -m app.cli
- Fixtures in cases/
- Tests: 16 passed on last run (FastAPI / Python 3.14 warnings only)

Enough to show a client how to freeze a prompt and fail a build when the answer drifts.

## Not built — do not sell these

- No live LLM call
- No dashboard or login
- No billing, teams, or Docker pack
- No multi-tenant SaaS
- No enterprise scale

If freelance work never appears, this stays a portfolio prototype.

## Who it is for

Founders who want prompt checks before hiring a big vendor. Freelancers who ship LLM features and need regression proof. Engineers showing a small honest tool.

Not a replacement for LangSmith, PromptLayer, or a full AI gateway.

## How to run (Windows)

Python 3.11+ (C:\Python314\python.exe on the original machine).

Install:

~~~powershell
cd E:\promptgate
C:\Python314\python.exe -m pip install fastapi uvicorn pydantic pytest httpx
~~~

Tests:

~~~powershell
C:\Python314\python.exe -m pytest -q --tb=short --basetemp=E:\promptgate\.pytest-tmp
~~~

Score a batch:

~~~powershell
C:\Python314\python.exe -m app.cli --cases cases\sample.json --outputs cases\sample-outputs.json --out results.json
~~~

Start the API:

~~~powershell
C:\Python314\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
~~~

Then open http://127.0.0.1:8000/health

## Example

POST /eval

~~~json
{
  "prompt": "What is the capital of France?",
  "expect_contains": "Paris",
  "output": "The capital is Paris."
}
~~~

~~~json
{ "passed": true }
~~~

If the output is "The capital is Berlin." the result is passed: false.

## Layout

~~~text
app/main.py      API
app/eval.py      pass/fail rules
app/store.py     load cases from JSON
app/cli.py       batch command
app/log.py       JSONL history
cases/           example questions and answers
tests/           automated tests
~~~

## Freelance next step

If a client appears: wire their model outputs into POST /eval/batch, keep 20-50 golden cases in cases/, fail CI when failed_count > 0. Until that request exists, do not grow this into a platform.

## Status

Personal prototype. No company, no SLA, no support promise.