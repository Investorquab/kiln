"""Run the final repository integrity checks before submission.

This audit checks static repository contracts only. It does not claim a live
BAND run, clean-container execution, or independent runtime proof.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PYTHON_FILES = [
    "factory/control_plane.py",
    "factory/runtime/validate.py",
    "factory/runtime/validate_run_ledger.py",
    "factory/runtime/execute_local_verification.py",
    "factory/runtime/execute_extension_regression.py",
    "factory/runtime/init_extension_run.py",
    "factory/runtime/audit_submission.py",
    "verification/attacks/concurrency.py",
    "verification/attacks/idempotency.py",
    "verification/attacks/timezone.py",
    "verification/attacks/invalid_input.py",
    "verification/attacks/cancellation.py",
    "app/backend/app/main.py",
]

JSON_FILES = [
    "factory/work_orders/tablekeeper.json",
    "factory/work_orders/tablekeeper-cancellation.json",
    "factory/artifacts/tablekeeper-cancellation-architect-plan.json",
    "factory/artifacts/tablekeeper-cancellation-invariant-model.json",
    "factory/artifacts/tablekeeper-cancellation-build-handoff.json",
    "factory/artifacts/tablekeeper-cancellation-local-regression.json",
]

def main() -> int:
    failures: list[str] = []

    for relative in PYTHON_FILES:
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing Python file: {relative}")
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as exc:
            failures.append(f"Python syntax failure: {relative}: {exc}")

    for relative in JSON_FILES:
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing JSON file: {relative}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"JSON failure: {relative}: {exc}")

    work_order = json.loads((ROOT / "factory/work_orders/tablekeeper.json").read_text(encoding="utf-8"))
    extension = json.loads((ROOT / "factory/work_orders/tablekeeper-cancellation.json").read_text(encoding="utf-8"))
    if work_order.get("work_order_id") != "WO-TABLEKEEPER-001":
        failures.append("base work order ID is invalid")
    if extension.get("work_order_id") != "WO-TABLEKEEPER-002":
        failures.append("extension work order ID is invalid")

    local_extension = json.loads(
        (ROOT / "factory/artifacts/tablekeeper-cancellation-local-regression.json").read_text(encoding="utf-8")
    )
    if local_extension.get("status") != "passed":
        failures.append("extension local regression artifact is not passing")
    if local_extension.get("source") != "local executable extension regression":
        failures.append("extension local regression is incorrectly attributed")
    attacks = local_extension.get("attacks", [])
    expected = ["concurrency", "idempotency", "timezone", "invalid_input", "cancellation"]
    if [item.get("name") for item in attacks] != expected:
        failures.append("extension regression attack order is invalid")
    if local_extension.get("summary", {}).get("failures") != 0:
        failures.append("extension regression records failures")

    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    if "internal: true" not in compose:
        failures.append("Compose network is not internal")
    if compose.count('cpus: "1.0"') < 3:
        failures.append("Compose CPU caps are incomplete")
    if compose.count("mem_limit: 512m") < 3:
        failures.append("Compose memory caps are incomplete")

    if failures:
        print("REPOSITORY INTEGRITY FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("REPOSITORY INTEGRITY PASSED")
    print(f"python_files={len(PYTHON_FILES)}")
    print(f"json_files={len(JSON_FILES)}")
    print("extension_regression_contract=passed")
    print("compose_contract=passed")
    print("band_run_claim=not_checked")
    print("runtime_execution=not_checked")
    return 0
