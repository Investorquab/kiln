# Kiln

**Kiln is an autonomous software factory that builds software, attacks its own implementation, repairs failures, and independently verifies the result.**

> Build it. Break it. Prove it.

## What Kiln actually is

Kiln is the **factory**, not the Tablekeeper reservation product. A clean-room workload arrives as a work order. Kiln turns that requirement into a plan, model, implementation, adversarial test run, repair cycle, and independent verification.

For the current demonstration, the workload is a clean-room Tablekeeper-style reservation service.

The hackathon asks for the factory, the run that produced the result, and the result. citeturn0search0

## Factory floor

```
WORK ORDER
    ↓
ARCHITECT → MODEL
    ↓
BUILDER
    ↓
ATTACK CELL
    ↓ failure
REPAIRER ──────────┐
    ↑              │
    └── ATTACK ────┘
                   ↓ pass
               VERIFIER
                   ↓
                PROVED
```

The control plane is deterministic and evidence-aware. It records stage status, attempts, artifacts, and evidence events. It does **not** pretend to invoke BAND agents; BAND Desktop is the agent collaboration/execution surface.

This separation follows a pattern visible in current software-factory implementations: orchestration owns lifecycle and gates, coding workers produce changes, and an independent verifier owns completion. citeturn0search1turn0search4

## Repository arrangement

- `factory/work_orders/` — replaceable workload input
- `factory/mandates/` — generic agent-seat contracts
- `factory/schemas/` — machine-readable contracts
- `factory/control_plane.py` — deterministic run ledger and gates
- `factory/runs/` — run evidence ledger
- `factory/runtime/` — artifact validation
- `factory/protocols/` — handoff/evidence rules
- `verification/attacks/` — adversarial workload checks
- `app/` — current product output
- `docs/` — factory, BAND, container, and submission operating docs

The structure intentionally separates product truth/work orders from execution and verification, a pattern also used by other factory designs.

## Quick start

    git clone https://github.com/Investorquab/kiln.git
    cd kiln
    docker compose up --build

Open http://localhost:3000 for the factory-floor interface, http://localhost:8000/docs for the API, and http://localhost:8000/health for health.

Verification:

    python -m pip install -r verification/requirements.txt
    python factory/runtime/validate.py
    python verification/run_all.py

## Control-plane demo

Create a run from the Tablekeeper work order:

    python factory/control_plane.py init "Build the Tablekeeper workload" --work-order WO-TABLEKEEPER-001

Then inspect it:

    python factory/control_plane.py status <run-id>

Record stage evidence only when the corresponding agent has actually produced it:

    python factory/control_plane.py complete <run-id> architect artifacts/architect-plan.json
    python factory/control_plane.py complete <run-id> modeler artifacts/invariant-model.json
    python factory/control_plane.py complete <run-id> builder artifacts/build-handoff.json

A failed attack enters the repair loop:

    python factory/control_plane.py fail <run-id> adversary artifacts/adversarial-report.json
    python factory/control_plane.py complete <run-id> repairer artifacts/repair-report.json
    python factory/control_plane.py complete <run-id> adversary artifacts/adversarial-retest.json
    python factory/control_plane.py complete <run-id> verifier artifacts/independent-verification.json

Only the verifier's passed artifact closes the run as `proved`.

## BAND execution

See `docs/BAND_RUNBOOK.md` for the actual room/seat workflow and `docs/FACTORY_FLOOR.md` for the factory model.

The repository does not claim a live BAND run until one has actually been performed and recorded. The final submission needs the BAND Desktop room recording that generated the solution.
