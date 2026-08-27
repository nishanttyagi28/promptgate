# PromptGate
Windows-first prompt contract gate. Not an LLM. Cases have prompt + expect_contains|exact|regex. You pass model output; you get pass/fail, results.json, runs/eval.jsonl.

## Run
cd E:\promptgate
C:\Python314\python.exe -m pytest -q --tb=short --basetemp=E:\promptgate\.pytest-tmp
C:\Python314\python.exe -m app.cli --cases cases\sample.json --outputs cases\sample-outputs.json --out results.json
C:\Python314\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
If PROMPTGATE_KEY is set, POST /eval and POST /eval/batch need header x-api-key.

## What went wrong building this
1. VS Code opened on E:\ drive root. pip install -e . hit file:///E:/ with no pyproject.toml.
2. Cline: command completion could not be observed; agent still claimed success.
3. Fake counts: 52 tests passed; later 6 passed in 1.48s while terminal still showed 4 passed in 1.48s.
4. Bash on PowerShell 5.1: ls -la, &&, echo >> file. Cline loop-killed after 5 identical run_commands.
5. New-Item 0-byte store.py / test_batch.py marked SUCCESS; pytest still collected 4 tests.
6. venv pip on 3.14: ImportError urllib3 from pip._vendor. Agent retried pip install -U pip until abort.
7. Cline profile PowerShell 7 spawned C:"Program Files"\PowerShell\7\pwsh.exe ENOENT. Machine is PS 5.1.
8. Aggressive terminal reuse + 4s timeout kept a stale 4 passed line.
9. WinError 5 on C:\Users\Admin\AppData\Local\Temp\pytest-of-Admin. Fix --basetemp=E:\promptgate\.pytest-tmp.
10. Auth tests expected 401; app returned 200 unless PROMPTGATE_KEY set before TestClient.
11. Agent said SATISFIED on 2 failed, 11 passed, 3 errors.
12. cmd1 && pytest | Out-File on PS 5.1 wrote an empty .pytest-out.txt.