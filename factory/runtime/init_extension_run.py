"""Initialize a Kiln factory ledger for the Tablekeeper cancellation extension.

This only creates the deterministic control-plane ledger. It does not execute
BAND agents or manufacture stage evidence.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK_ORDER = ROOT / "factory" / "work_orders" / "tablekeeper-cancellation.json"


def main() -> int:
    work_order = json.loads(WORK_ORDER.read_text(encoding="utf-8"))
    requirement = work_order["requirement"]
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "factory" / "control_plane.py"),
            "init",
            requirement,
            "--work-order",
            work_order["work_order_id"],
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    run_id = result.stdout.strip().splitlines()[-1]
    print(f"extension_run_id={run_id}")
    print("status=running")
    print("work_order=WO-TABLEKEEPER-002")
    print("No stage evidence has been recorded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
