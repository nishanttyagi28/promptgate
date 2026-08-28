import argparse
import json
from pathlib import Path
from .store import load_cases
from .eval import run_case
from .models import PromptCase
from .log import append_run

def main():
    parser = argparse.ArgumentParser(description="PromptGate CLI")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--cases", required=True, help="Path to cases JSON file")
    parser.add_argument("--outputs", required=True, help="Path to outputs JSON file")
    parser.add_argument("--out", required=True, help="Path to results JSON file")
    args = parser.parse_args()
    
    cases = load_cases(args.cases)
    with open(args.outputs, 'r') as f:
        outputs = json.load(f)
    
    results = []
    for case_data in cases:
        case_id = case_data["id"]
        output = outputs.get(case_id, "")
        case = PromptCase(**case_data)
        result = run_case(case, output)
        results.append({"id": case_id, **result})
    
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count
    
    print(f"Passed: {passed_count}, Failed: {failed_count}")
    
    with open(args.outputs, 'w') as f:
        json.dump(outputs, f, indent=2)
    
    with open(args.out, 'w') as f:
        json.dump({
            "results": results,
            "passed_count": passed_count,
            "failed_count": failed_count
        }, f, indent=2)
    
    # Log the run
    append_run({
        "cases": args.cases,
        "outputs": args.outputs,
        "results": results,
        "passed_count": passed_count,
        "failed_count": failed_count
    })
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())