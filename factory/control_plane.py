"""Deterministic control plane for Kiln factory runs.

This module is the factory ledger/gate layer. It does not invoke BAND agents.
Agents produce artifacts; the control plane records and gates those artifacts.
"""
from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "factory" / "runs"
STAGES = ["architect", "modeler", "builder", "adversary", "repairer", "verifier"]
VALID_STATUSES = {"pending", "passed", "failed"}
RUN_STATUSES = {"running", "repair_required", "proved"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def path(run_id: str) -> Path:
    return RUNS / f"{run_id}.json"


def load(run_id: str) -> dict:
    p = path(run_id)
    if not p.exists():
        raise SystemExit(f"run not found: {run_id}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"invalid run ledger: {run_id}") from exc


def save(run: dict) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    path(run["run_id"]).write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")


def validate_run(run: dict) -> None:
    required = (
        "run_id",
        "work_order",
        "requirement",
        "created_at",
        "updated_at",
        "status",
        "stages",
        "evidence",
    )
    missing = [key for key in required if key not in run]
    if missing:
        raise SystemExit(f"run ledger missing keys: {', '.join(missing)}")
    if run["status"] not in RUN_STATUSES:
        raise SystemExit(f"invalid run status: {run['status']}")

    stages = run["stages"]
    if not isinstance(stages, list) or [item.get("name") for item in stages] != STAGES:
        raise SystemExit("run ledger stages must be exactly architect/modeler/builder/adversary/repairer/verifier")

    for item in stages:
        if set(item) != {"name", "status", "artifact", "attempt"}:
            raise SystemExit(f"invalid stage shape: {item.get('name')}")
        if item["status"] not in VALID_STATUSES:
            raise SystemExit(f"invalid stage status: {item['name']}")
        if not isinstance(item["attempt"], int) or item["attempt"] < 0:
            raise SystemExit(f"invalid stage attempt: {item['name']}")
        if item["status"] == "pending" and item["attempt"] != 0:
            raise SystemExit(f"pending stage has non-zero attempt: {item['name']}")
        if item["status"] != "pending" and not item["artifact"]:
            raise SystemExit(f"completed stage has no artifact: {item['name']}")

    if not isinstance(run["evidence"], list):
        raise SystemExit("run ledger evidence must be a list")
    previous_attempts = {stage: 0 for stage in STAGES}
    for event in run["evidence"]:
        required_event = {"event_id", "at", "stage", "status", "artifact", "attempt"}
        if set(event) != required_event:
            raise SystemExit("invalid evidence event shape")
        if event["stage"] not in STAGES or event["status"] not in {"passed", "failed"}:
            raise SystemExit("invalid evidence event stage/status")
        if not isinstance(event["attempt"], int) or event["attempt"] < 1:
            raise SystemExit("invalid evidence attempt")
        previous_attempts[event["stage"]] = max(previous_attempts[event["stage"]], event["attempt"])

    for item in stages:
        if previous_attempts[item["name"]] > item["attempt"]:
            raise SystemExit(f"evidence attempt exceeds stage attempt: {item['name']}")


def init_run(requirement: str, work_order: str = "unspecified") -> dict:
    run = {
        "run_id": uuid.uuid4().hex[:12],
        "work_order": work_order,
        "requirement": requirement,
        "created_at": now(),
        "updated_at": now(),
        "status": "running",
        "stages": [
            {"name": stage, "status": "pending", "artifact": None, "attempt": 0}
            for stage in STAGES
        ],
        "evidence": [],
    }
    save(run)
    return run


def stage(run: dict, name: str) -> dict:
    return next(item for item in run["stages"] if item["name"] == name)


def allowed(run: dict, stage_name: str) -> bool:
    current = stage(run, stage_name)
    if current["status"] == "passed":
        return False
    if stage_name == "architect":
        return True
    if stage_name == "modeler":
        return stage(run, "architect")["status"] == "passed"
    if stage_name == "builder":
        return stage(run, "modeler")["status"] == "passed"
    if stage_name == "adversary":
        return (
            stage(run, "builder")["status"] == "passed"
            and (
                stage(run, "adversary")["status"] == "pending"
                or stage(run, "repairer")["status"] == "passed"
            )
        )
    if stage_name == "repairer":
        return stage(run, "adversary")["status"] == "failed"
    if stage_name == "verifier":
        return stage(run, "adversary")["status"] == "passed"
    return False


def validate_artifact(stage_name: str, artifact: str, status: str) -> None:
    artifact_path = ROOT / artifact
    if not artifact_path.is_file():
        raise SystemExit(f"artifact not found: {artifact}")

    if stage_name == "verifier" and status == "passed":
        try:
            document = json.loads(artifact_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SystemExit(f"verifier artifact must be valid JSON: {artifact}") from exc
        if document.get("status") != "passed":
            raise SystemExit("verifier artifact must declare status=passed")
        summary = document.get("summary", {})
        if summary.get("failures") != 0:
            raise SystemExit("verifier artifact cannot prove a run with failures")


def record(run: dict, stage_name: str, status: str, artifact: str) -> None:
    validate_run(run)
    if status not in VALID_STATUSES - {"pending"}:
        raise SystemExit(f"invalid completion status: {status}")
    if not allowed(run, stage_name):
        raise SystemExit(f"stage {stage_name} is not currently allowed")
    validate_artifact(stage_name, artifact, status)

    item = stage(run, stage_name)
    item["status"] = status
    item["artifact"] = artifact
    item["attempt"] += 1

    event = {
        "event_id": uuid.uuid4().hex[:10],
        "at": now(),
        "stage": stage_name,
        "status": status,
        "artifact": artifact,
        "attempt": item["attempt"],
    }
    run["evidence"].append(event)
    run["updated_at"] = event["at"]

    if stage_name == "adversary" and status == "failed":
        repairer = stage(run, "repairer")
        repairer["status"] = "pending"
        repairer["artifact"] = None

    if stage_name == "verifier" and status == "passed":
        run["status"] = "proved"
    elif status == "failed":
        run["status"] = "repair_required"
    else:
        run["status"] = "running"

    validate_run(run)
    save(run)


def show(run: dict) -> None:
    validate_run(run)
    print(f"run_id={run['run_id']}")
    print(f"work_order={run['work_order']}")
    print(f"status={run['status']}")
    print(f"requirement={run['requirement']}")
    for item in run["stages"]:
        print(
            f"{item['name']}: {item['status']} "
            f"(attempt {item['attempt']}) [{item['artifact'] or '-'}]"
        )
    print(f"evidence_events={len(run['evidence'])}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiln deterministic factory control plane")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("requirement")
    init.add_argument("--work-order", default="unspecified")

    status = sub.add_parser("status")
    status.add_argument("run_id")

    complete = sub.add_parser("complete")
    complete.add_argument("run_id")
    complete.add_argument("stage", choices=STAGES)
    complete.add_argument("artifact")

    fail = sub.add_parser("fail")
    fail.add_argument("run_id")
    fail.add_argument("stage", choices=STAGES)
    fail.add_argument("artifact")

    args = parser.parse_args()

    if args.command == "init":
        print(init_run(args.requirement, args.work_order)["run_id"])
        return 0

    run = load(args.run_id)
    if args.command == "status":
        show(run)
        return 0

    record(
        run,
        args.stage,
        "failed" if args.command == "fail" else "passed",
        args.artifact,
    )
    show(load(args.run_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
