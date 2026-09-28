"""Validate Kiln factory artifacts before they enter the evidence chain."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(relative: str) -> dict:
    with (ROOT / relative).open(encoding="utf-8") as handle:
        return json.load(handle)


def check_keys(name: str, document: dict, keys: tuple[str, ...]) -> list[str]:
    return [f"{name}: missing {key}" for key in keys if key not in document]


def check_stage_shape(name: str, document: dict) -> list[str]:
    errors: list[str] = []
    stages = document.get("stages")
    if not isinstance(stages, list) or not stages:
        return [f"{name}: stages must be a non-empty list"]
    for index, item in enumerate(stages):
        if not isinstance(item, dict):
            errors.append(f"{name}: stage {index} must be an object")
            continue
        errors.extend(
            check_keys(
                f"{name} stage {index}",
                item,
                ("name", "status", "artifact", "attempt"),
            )
        )
    return errors


def main() -> int:
    errors: list[str] = []

    extension_work_order = load("factory/work_orders/tablekeeper-cancellation.json")
    errors.extend(
        check_keys(
            "extension work order",
            extension_work_order,
            ("work_order_id", "workload", "requirement", "acceptance", "evidence_required"),
        )
    )
    if extension_work_order.get("work_order_id") != "WO-TABLEKEEPER-002":
        errors.append("extension work order: unexpected work_order_id")
    if not isinstance(extension_work_order.get("acceptance"), list) or not extension_work_order["acceptance"]:
        errors.append("extension work order: acceptance must be a non-empty list")

    work_order = load("factory/work_orders/tablekeeper.json")
    errors.extend(
        check_keys(
            "work order",
            work_order,
            ("work_order_id", "workload", "requirement", "acceptance"),
        )
    )
    if not isinstance(work_order.get("acceptance"), list) or not work_order["acceptance"]:
        errors.append("work order: acceptance must be a non-empty list")

    handoff = load("factory/artifacts/example-handoff.json")
    errors.extend(
        check_keys(
            "handoff",
            handoff,
            (
                "stage",
                "task",
                "inputs",
                "outputs",
                "changed_files",
                "tests",
                "evidence",
                "open_failures",
                "next_action",
            ),
        )
    )

    verification = load("factory/artifacts/example-verification.json")
    errors.extend(
        check_keys(
            "verification",
            verification,
            ("run_id", "stage", "status", "invariants"),
        )
    )

    local_report = load("factory/runs/tablekeeper-local-verification.json")
    errors.extend(
        check_keys(
            "local verification report",
            local_report,
            ("run_id", "work_order", "stage", "status", "attacks", "summary"),
        )
    )
    if local_report.get("stage") != "verifier":
        errors.append("local verification report: stage must be verifier")
    if not isinstance(local_report.get("attacks"), list) or len(local_report["attacks"]) != 4:
        errors.append("local verification report: expected four attack results")
    if local_report.get("source") != "local executable verification":
        errors.append("local verification report: source must identify executable local verification")
    attack_names = [item.get("name") for item in local_report.get("attacks", []) if isinstance(item, dict)]
    if attack_names != ["concurrency", "idempotency", "timezone", "invalid_input"]:
        errors.append("local verification report: attack order/names are invalid")
    if any(item.get("status") != "passed" for item in local_report.get("attacks", []) if isinstance(item, dict)):
        errors.append("local verification report: every attack must pass")
    summary = local_report.get("summary", {})
    errors.extend(
        check_keys(
            "local verification summary",
            summary,
            ("attacks", "failures", "result"),
        )
    )
    if summary.get("failures") != 0 or summary.get("result") != "VERIFICATION BATCH PASSED":
        errors.append("local verification report: recorded result is not a passing batch")

    extension_regression = load("factory/artifacts/tablekeeper-cancellation-local-regression.json")
    errors.extend(
        check_keys(
            "extension local regression",
            extension_regression,
            ("run_id", "work_order", "stage", "status", "attacks", "summary", "note"),
        )
    )
    if extension_regression.get("work_order") != "WO-TABLEKEEPER-002":
        errors.append("extension local regression: wrong work order")
    if extension_regression.get("stage") != "verifier":
        errors.append("extension local regression: stage must be verifier")
    if extension_regression.get("source") != "local executable extension regression":
        errors.append("extension local regression: source is invalid")
    extension_attacks = extension_regression.get("attacks")
    if not isinstance(extension_attacks, list) or len(extension_attacks) != 5:
        errors.append("extension local regression: expected five attack results")
    expected_extension_attacks = ["concurrency", "idempotency", "timezone", "invalid_input", "cancellation"]
    if [item.get("name") for item in extension_attacks if isinstance(item, dict)] != expected_extension_attacks:
        errors.append("extension local regression: attack order/names are invalid")
    if any(item.get("status") != "passed" for item in extension_attacks if isinstance(item, dict)):
        errors.append("extension local regression: every attack must pass")
    extension_summary = extension_regression.get("summary", {})
    errors.extend(
        check_keys(
            "extension regression summary",
            extension_summary,
            ("attacks", "failures", "result"),
        )
    )
    if extension_summary.get("failures") != 0 or extension_summary.get("result") != "EXTENSION REGRESSION PASSED":
        errors.append("extension local regression: recorded result is not a passing batch")

    run = load("factory/artifacts/run-template.json")
    errors.extend(
        check_keys(
            "run template",
            run,
            (
                "run_id",
                "work_order",
                "requirement",
                "created_at",
                "updated_at",
                "status",
                "stages",
                "evidence",
            ),
        )
    )
    errors.extend(check_stage_shape("run template", run))

    if errors:
        print("ARTIFACT VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("ARTIFACT VALIDATION PASSED")
    print("work_order=valid")
    print("handoff=valid")
    print("verification=valid")
    print("local_verification=valid")
    print("run_template=valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
