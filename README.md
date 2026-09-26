# Kiln

**Kiln is an autonomous software factory that builds software, attacks its own implementation, repairs failures, and independently verifies the result.**

> Build it. Break it. Prove it.

## What Kiln actually is

Kiln is the **factory**, not the Tablekeeper reservation product. The hackathon workload is supplied to the factory as a work order. Kiln turns that requirement into a plan, model, implementation, adversarial test run, repair cycle, and independent verification.

For the current demonstration, the workload is a clean-room Tablekeeper-style reservation service.

## Factory loop

Requirement -> Model -> Build -> Attack -> Repair -> Verify -> Evidence

BAND Desktop provides the multi-agent collaboration surface. Kiln defines the generic mandates, workload contracts, handoff rules, deterministic run state, verification harness, and evidence protocol.

See `docs/FACTORY_ARCHITECTURE.md`.

## Quick start

    git clone https://github.com/Investorquab/kiln.git
    cd kiln
    docker compose up --build

Open http://localhost:3000 for the Kiln interface, http://localhost:8000/docs for the API, and http://localhost:8000/health for health.

Verification:

    python -m pip install -r verification/requirements.txt
    python factory/runtime/validate.py
    python verification/run_all.py

Factory control-plane example:

    python factory/control_plane.py init "Build the Tablekeeper workload"
    python factory/control_plane.py status <run-id>

The final demonstration must show the BAND Desktop room that generated the solution. The repository does not pretend a live BAND run has happened until we actually perform and record one.
