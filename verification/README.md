# Verification

The verification layer is intentionally independent from the application implementation.

## Live run

Start the stack first, then run:

```powershell
python verification/run_all.py
```

The runner fails closed: any unexpected response or failed attack returns a non-zero exit code.

## Evidence rule

Files under `verification/reports/` are evidence only when generated from an actual run. Templates and examples explicitly say when they have not been executed.
