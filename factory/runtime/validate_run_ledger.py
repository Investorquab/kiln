"""Validate a concrete Kiln run ledger and its referenced evidence artifacts.

The validator is provenance-oriented: every completed stage must point to an
existing artifact, every evidence event must match the stage attempt, and a
proved run must have a passing verifier artifact. It does not claim that the
run came from BAND Desktop.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGES = ["architect", "modeler", "builder", "adversary", "repairer", "verifier"]


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"invalid JSON artifact: {path}") from exc


def artifact_path(value: str) -> Path:
    candidate = Path(value)
    return candidate if candidate.is_absolute() else ROOT / candidate


def validate(run_id: str) -> None:
    ledger_path = ROOT / "factory" / "runs" / f"{run_id}.json"
    if not ledger_path.is_file():
        raise SystemExit(f"run ledger not found: {ledger_path}")

    run = load_json(ledger_path)
    if run.get("run_id") != run_id:
        raise SystemExit("ledger run_id does not match requested run")

    stages = run.get("stages")
    if not isinstance(stages, list) or [s.get("name") for s in stages] != STAGES:
        raise SystemExit("ledger stage sequence is invalid")

    evidence = run.get("evidence")
    if not isinstance(evidence, list):
        raise SystemExit("ledger evidence must be a list")

    events_by_stage = {stage: [] for stage in STAGES}
    for event in evidence:
        stage = event.get("stage")
        if stage not in events_by_stage:
            raise SystemExit(f"evidence references unknown stage: {stage}")
        events_by_stage[stage].append(event)

    for stage in stages:
        name = stage["name"]
        events = events_by_stage[name]
        if stage["status"] == "pending":
            if events:
                raise SystemExit(f"pending stage has evidence: {name}")
            continue

        artifact = stage.get("artifact")
        if not artifact:
            raise SystemExit(f"completed stage has no artifact: {name}")
        if not artifact_path(artifact).is_file():
            raise SystemExit(f"stage artifact missing: {artifact}")

        if not events:
            raise SystemExit(f"completed stage has no evidence event: {name}")
        latest = max(events, key=lambda event: event["attempt"])
        if latest["artifact"] != artifact:
            raise SystemExit(f"latest evidence does not point to stage artifact: {name}")
        if latest["status"] != stage["status"]:
            raise SystemExit(f"stage/evidence status mismatch: {name}")
        if latest["attempt"] != stage["attempt"]:
            raise SystemExit(f"stage/evidence attempt mismatch: {name}")

    if run.get("status") == "proved":
        verifier = next(stage for stage in stages if stage["name"] == "verifier")
        if verifier["status"] != "passed":
            raise SystemExit("proved run does not have a passed verifier")
        document = load_json(artifact_path(verifier["artifact"]))
        if document.get("status") != "passed":
            raise SystemExit("verifier artifact is not passing")
        summary = document.get("summary", {})
        if summary.get("failures") != 0:
            raise SystemExit("verifier artifact contains failures")
        if not document.get("run_id"):
            raise SystemExit("verifier artifact is missing its verification run_id")

    print("RUN LEDGER VALIDATION PASSED")
    print(f"factory_run_id={run_id}")
    print(f"status={run['status']}")
    print(f"stages={sum(stage['status'] != 'pending' for stage in stages)}/6 completed")
    print(f"evidence_events={len(evidence)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a concrete Kiln run ledger")
    parser.add_argument("run_id")
    args = parser.parse_args()
    validate(args.run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
