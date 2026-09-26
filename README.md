# Kiln

**Kiln is an autonomous software factory that builds software, attacks its own implementation, repairs failures, and independently verifies the result.**

Core loop:

**Requirement → Model → Build → Attack → Repair → Verify → Evidence**

## Demonstration workload

Kiln currently uses a clean-room Tablekeeper-style reservation service to demonstrate concurrency, idempotency, timezone, and transactional correctness.

## Local backend

```powershell
docker compose up --build
```

Backend health:

```powershell
curl http://localhost:8000/health
```

## Verification

With the backend running and Python dependencies available:

```powershell
python verification/run_all.py
```

The verification harness is deliberately adversarial. It sends independent concurrent requests and replay scenarios against the live service.

## Factory structure

- `factory/mandates/` — generic agent mandates
- `factory/protocols/` — stage contracts
- `factory/schemas/` — machine-readable artifact schemas
- `factory/artifacts/` — example planning and attack artifacts
- `verification/` — executable attacks and reports
- `app/backend/` — demonstration workload

See `docs/DEMO.md` for the intended hackathon walkthrough.
