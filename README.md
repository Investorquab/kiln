# Kiln

**Kiln is an autonomous software factory that builds software, attacks its own implementation, repairs failures, and independently verifies the result.**

> **Build it. Break it. Prove it.**

## Core loop

**Requirement → Model → Build → Attack → Repair → Verify → Evidence**

## Demonstration workload

Kiln uses a clean-room Tablekeeper-style reservation service to demonstrate:
- concurrency safety
- idempotent retries
- timezone normalization
- invalid-input rejection

The workload is the demonstration. **The factory is the product.**

## Quick start

```powershell
git clone https://github.com/Investorquab/kiln.git
cd kiln
docker compose up --build
```

Open:
- http://localhost:3000 — Kiln interface
- http://localhost:8000/docs — backend API
- http://localhost:8000/health — health check

With the stack running, install the verification runner dependency:

```powershell
python -m pip install -r verification/requirements.txt
python verification/run_all.py
```

Each verification run receives a unique run ID, so repeated runs do not collide with evidence from earlier runs.

The runner fails closed: any unexpected response or failed attack produces a non-zero exit code.

## Factory

The BAND Desktop room uses generic mandates for Architect, Modeler, Builder, Adversary, Repairer, and Verifier. Workload-specific context is passed as task artifacts rather than encoded into the mandates.

See:
- `docs/BAND_ROOM.md`
- `docs/AGENT_HANDOFF.md`
- `docs/SUBMISSION_CHECKLIST.md`
- `docs/FAILURE_POLICY.md`
- `docs/CONTAINER.md`

## Evidence

Do not treat templates as live evidence. Verification reports become evidence only after a real run records commands, implementation revision, observed output, and pass/fail status.
