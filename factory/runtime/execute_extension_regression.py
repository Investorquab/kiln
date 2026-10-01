"""Execute the extended Tablekeeper regression suite locally.

This is local evidence only. It does not claim BAND Desktop generated the run.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT = ROOT / "factory" / "runs" / "tablekeeper-extension-regression.json"

ATTACKS = [
    ("concurrency", "verification/attacks/concurrency.py"),
    ("idempotency", "verification/attacks/idempotency.py"),
    ("timezone", "verification/attacks/timezone.py"),
    ("invalid_input", "verification/attacks/invalid_input.py"),
    ("cancellation", "verification/attacks/cancellation.py"),
]


def value(output: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}=(.+)$", output, re.MULTILINE)
    if not match:
        raise ValueError(f"missing {key} in attack output")
    return match.group(1).strip()


def parse_attack(name: str, output: str, returncode: int) -> tuple[str, dict]:
    run_id = value(output, "run_id")
    marker = {
        "concurrency": "ATTACK PASSED",
        "idempotency": "IDEMPOTENCY ATTACK PASSED",
        "timezone": "TIMEZONE ATTACK PASSED",
        "invalid_input": "INVALID INPUT ATTACK PASSED",
        "cancellation": "CANCELLATION ATTACK PASSED",
    }[name]
    passed = marker in output
    report = {"name": name, "status": "passed" if passed and returncode == 0 else "failed"}

    if name == "concurrency":
        report.update(
            requests=int(value(output, "requests")),
            created=int(value(output, "created")),
            conflicts=int(value(output, "conflicts")),
            unexpected=int(value(output, "unexpected")),
        )
    elif name == "idempotency":
        report.update(
            replay_statuses=ast.literal_eval(value(output, "replay_statuses")),
            unique_reservation_ids=int(value(output, "unique_reservation_ids")),
            tampered_replay_status=int(value(output, "tampered_replay_status")),
        )
    elif name == "timezone":
        report.update(
            first=int(value(output, "first")),
            equivalent=int(value(output, "equivalent")),
        )
    elif name == "invalid_input":
        report.update(
            status_code=int(value(output, "status")),
            created_records=int(value(output, "created_records")),
        )
    elif name == "cancellation":
        report.update(
            same_key_replay_statuses=ast.literal_eval(value(output, "same_key_replay_statuses")),
            competing_key_statuses=ast.literal_eval(value(output, "competing_key_statuses")),
            missing_reservation_status=int(value(output, "missing_reservation_status")),
        )

    return run_id, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the extended Tablekeeper regression suite")
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    run_id = os.environ.get("KILN_ATTACK_RUN_ID", uuid.uuid4().hex[:12])
    env = os.environ.copy()
    env["KILN_ATTACK_RUN_ID"] = run_id

    attacks = []
    failures = 0
    raw_sections = []

    for name, attack in ATTACKS:
        result = subprocess.run(
            [sys.executable, attack],
            check=False,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        raw_sections.append(f"=== {attack} ===\n{output}")
        try:
            attack_run_id, report = parse_attack(name, output, result.returncode)
        except (ValueError, SyntaxError) as exc:
            print(f"Could not parse {attack}: {exc}", file=sys.stderr)
            failures += 1
            continue

        if attack_run_id != run_id:
            print(f"run_id mismatch in {attack}", file=sys.stderr)
            failures += 1
        if report["status"] != "passed":
            failures += 1
        attacks.append(report)

    failures += len(ATTACKS) - len(attacks)
    report = {
        "run_id": run_id,
        "work_order": "WO-TABLEKEEPER-002",
        "workload": "tablekeeper",
        "stage": "verifier",
        "status": "passed" if failures == 0 else "failed",
        "source": "local executable extension regression",
        "attacks": attacks,
        "summary": {
            "attacks": len(ATTACKS),
            "failures": failures,
            "result": "EXTENSION REGRESSION PASSED" if failures == 0 else "EXTENSION REGRESSION FAILED",
        },
        "note": "Local extension evidence; not a BAND Desktop-generated stage.",
    }

    destination = Path(args.report)
    if not destination.is_absolute():
        destination = ROOT / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"report={destination.relative_to(ROOT)}")
    print(json.dumps(report, indent=2))
    if failures:
        print("\nEXTENSION REGRESSION FAILED", file=sys.stderr)
        print("\n".join(raw_sections), file=sys.stderr)
        return 1

    print("\nEXTENSION REGRESSION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
