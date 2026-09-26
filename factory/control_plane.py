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


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def path(run_id: str) -> Path:
    return RUNS / f"{run_id}.json"


def load(run_id: str) -> dict:
    p = path(run_id)
    if not p.exists():
        raise SystemExit(f"run not found: {run_id}")
    return json.loads(p.read_text(encoding="utf-8"))


def save(run: dict) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    path(run["run_id"]).write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")


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


def record(run: dict, stage_name: str, status: str, artifact: str) -> None:
    if status not in VALID_STATUSES - {"pending"}:
        raise SystemExit(f"invalid completion status: {status}")
    if not allowed(run, stage_name):
        raise SystemExit(f"stage {stage_name} is not currently allowed")
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

    if stage_name == "verifier" and status == "passed":
        run["status"] = "proved"
    elif status == "failed":
        run["status"] = "repair_required"
    else:
        run["status"] = "running"
    save(run)


def show(run: dict) -> None:
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
