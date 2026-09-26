# Verification

Kiln treats verification as an executable stage rather than a screenshot.

## Local sequence

    docker compose up --build

In a second terminal:

    python -m pip install -r verification/requirements.txt
    python factory/runtime/validate.py
    python verification/run_all.py

The final run contains four attack stages: concurrency, idempotency, timezone equivalence, and invalid-input rejection.

Do not copy expected results into a submission as observed evidence. Record the exact command, implementation revision, run ID, observed output, pass/fail status, and independent verifier result. If an attack fails, preserve the failure and follow the repair policy.