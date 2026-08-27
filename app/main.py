import json
import os
from fastapi import FastAPI, HTTPException, Header, Request
from .config import APP_NAME
from .models import PromptCase
from .eval import run_case
from .store import load_cases
from .log import append_run
from pathlib import Path

app = FastAPI(title=APP_NAME)


def verify_api_key(request: Request):
    x_api_key = request.headers.get("x-api-key")
    if os.environ.get("PROMPTGATE_KEY") and request.url.path in ["/eval", "/eval/batch"]:
        if not x_api_key or x_api_key != os.environ["PROMPTGATE_KEY"]:
            raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": APP_NAME}


@app.get("/cases")
async def get_cases():
    cases = load_cases(str(Path(__file__).parent.parent / "cases" / "sample.json"))
    return {"cases": cases}


@app.get("/runs")
async def get_runs():
    from .log import RUN_LOG
    if not RUN_LOG.exists():
        return {"runs": []}
    with RUN_LOG.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    runs = []
    for line in lines[-20:]:  # Last 20 lines
        try:
            runs.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return {"runs": runs}


@app.post("/eval")
async def eval_endpoint(body: dict, request: Request):
    verify_api_key(request)
    prompt = body.get("prompt", "")
    expect_contains = body.get("expect_contains", "")
    output = body.get("output", "")
    
    case = PromptCase(id="adhoc", prompt=prompt, expect_contains=expect_contains)
    result = run_case(case, output)
    return result


@app.post("/eval/batch")
async def eval_batch(body: dict, request: Request):
    verify_api_key(request)
    outputs = body.get("outputs", {})
    cases = load_cases(str(Path(__file__).parent.parent / "cases" / "sample.json"))
    
    results = []
    for case_data in cases:
        case_id = case_data["id"]
        output = outputs.get(case_id, "")
        case = PromptCase(**case_data)
        result = run_case(case, output)
        results.append({"id": case_id, "passed": result["passed"]})
    
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count
    
    # Log the run
    append_run({
        "results": results,
        "passed_count": passed_count,
        "failed_count": failed_count
    })
    
    return {
        "results": results,
        "passed_count": passed_count,
        "failed_count": failed_count
    }
