import json
import os
from fastapi import FastAPI, HTTPException, Header, Request
from .config import APP_NAME
from .models import PromptCase
from .eval import run_case, load_suite, compare_outputs
from .store import load_cases, load_cases_from_db_or_file
from .log import append_run
from .db import insert_case
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
    cases = load_cases_from_db_or_file()
    return {"cases": cases}


@app.post("/cases")
async def post_case(body: dict, request: Request):
    verify_api_key(request)
    prompt = body.get("prompt", "")
    expect = body.get("expect", "")
    match = body.get("match")
    suite = body.get("suite")
    tags_json = body.get("tags_json")
    
    if not prompt or not expect:
        raise HTTPException(status_code=400, detail="prompt and expect are required")
    
    case_id = insert_case(prompt, expect, match, suite, tags_json)
    return {"id": case_id, "prompt": prompt, "expect": expect, "match": match, "suite": suite, "tags_json": tags_json}


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
    cases = load_cases_from_db_or_file()
    
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


@app.post("/eval/suite")
async def eval_suite(body: dict, request: Request):
    verify_api_key(request)
    suite = body.get("suite", "")
    outputs = body.get("outputs", {})
    
    if not suite:
        raise HTTPException(status_code=400, detail="suite is required")
    
    try:
        cases = load_suite(suite)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Suite {suite} not found")
    
    results = []
    for case_data in cases:
        case_id = case_data["id"]
        output = outputs.get(case_id, "")
        case = PromptCase(**case_data)
        result = run_case(case, output, case_data.get("match", "contains"))
        results.append({"id": case_id, "passed": result["passed"]})
    
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count
    
    return {
        "results": results,
        "passed_count": passed_count,
        "failed_count": failed_count
    }


@app.get("/report")
async def get_report():
    report_path = Path("reports/last.html")
    if report_path.exists():
        return report_path.read_text()
    else:
        raise HTTPException(status_code=404, detail="Report not found")


@app.post("/eval/compare")
async def eval_compare(body: dict, request: Request):
    verify_api_key(request)
    baseline_outputs = body.get("baseline_outputs", {})
    candidate_outputs = body.get("candidate_outputs", {})
    cases = body.get("cases", [])
    
    if not cases:
        raise HTTPException(status_code=400, detail="cases are required")
    
    comparison = compare_outputs(baseline_outputs, candidate_outputs, cases)
    
    return {
        "newly_failed": comparison["newly_failed"],
        "newly_passed": comparison["newly_passed"],
        "unchanged": comparison["unchanged"],
        "details": comparison["details"]
    }
@app.post("/eval/run")
async def eval_run(body: dict, request: Request):
    verify_api_key(request)
    suite = body.get("suite", "")
    provider_name = body.get("provider", "mock")
    
    if not suite:
        raise HTTPException(status_code=400, detail="suite is required")
    
    try:
        cases = load_suite(suite)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Suite {suite} not found")
    
    # Initialize the provider
    if provider_name == "mock":
        from .providers.mock import MockProvider
        provider = MockProvider()
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider_name}")
    
    results = []
    for case_data in cases:
        case_id = case_data["id"]
        prompt = case_data["prompt"]
        output = provider.generate(prompt)
        case = PromptCase(**case_data)
        result = run_case(case, output, case_data.get("match", "contains"))
        results.append({"id": case_id, "passed": result["passed"]})
    
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count
    
    return {
        "results": results,
        "passed_count": passed_count,
        "failed_count": failed_count
    }
# Serve static files
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")