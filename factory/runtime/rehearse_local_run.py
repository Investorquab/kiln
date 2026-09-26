"""Rehearse a complete Kiln factory run against the local Tablekeeper workload.

This is a local control-plane rehearsal. It is not a BAND Desktop execution.
The script runs the real local verifier, records the stage ledger, and stops if
the adversarial batch fails so the Repairer path remains honest.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from factory.control_plane import init_run, load, record  # noqa: E402


WORK_ORDER = "WO-TABLEKEEPER-001"
REQUIREMENT = "Build the Tablekeeper workload"
STATIC_ARTIFACTS = {
    "architect": "factory/artifacts/architect-plan.json",
    "modeler": "factory/artifacts/invariant-model.json",
    "builder": "factory/artifacts/build-handoff.json",
}


def run_verifier(report: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "factory/runtime/execute_local_verification.py",
            "--report",
            str(report),
        ],
        cwd=ROOT,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise SystemExit(f"local verification runner failed to execute: exit {result.returncode}")


def main() -> int:
    run = init_run(REQUIREMENT, WORK_ORDER)
    run_id = run["run_id"]
    print(f"factory_run_id={run_id}")

    for stage_name in ("architect", "modeler", "builder"):
        record(run, stage_name, "passed", STATIC_ARTIFACTS[stage_name])
        run = load(run_id)

    report = ROOT / "factory" / "runs" / f"{run_id}-verification.json"
    run_verifier(report)

    verification = json.loads(report.read_text(encoding="utf-8"))
    adversarial = ROOT / "factory" / "runs" / f"{run_id}-adversarial.json"
    adversarial.write_text(
        json.dumps(
            {
                "stage": "adversary",
                "status": verification["status"],
                "source": "local executable verification rehearsal",
                "work_order": WORK_ORDER,
                "attacks": verification["attacks"],
                "summary": verification["summary"],
                "note": "Local rehearsal evidence; not a BAND Desktop-generated stage.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    if verification["status"] != "passed":
        record(run, "adversary", "failed", str(adversarial.relative_to(ROOT)))
        print("FACTORY REHEARSAL STOPPED: adversary failed; repairer is required.")
        return 1

    record(run, "adversary", "passed", str(adversarial.relative_to(ROOT)))
    run = load(run_id)
    record(run, "verifier", "passed", str(report.relative_to(ROOT)))
    run = load(run_id)

    print(f"verification_run_id={verification['run_id']}")
    print(f"status={run['status']}")
    print(f"ledger=factory/runs/{run_id}.json")
    print("FACTORY REHEARSAL PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
