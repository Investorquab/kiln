"""Run Kiln's executable Tablekeeper attacks as one repeatable verification batch."""
from __future__ import annotations

import os
import subprocess
import sys
import uuid

ATTACKS = [
    "verification/attacks/concurrency.py",
    "verification/attacks/idempotency.py",
    "verification/attacks/timezone.py",
    "verification/attacks/invalid_input.py",
]


def main() -> int:
    run_id = os.environ.get("KILN_ATTACK_RUN_ID", uuid.uuid4().hex[:12])
    env = os.environ.copy()
    env["KILN_ATTACK_RUN_ID"] = run_id

    failures = 0
    for attack in ATTACKS:
        print(f"\n=== {attack} ===")
        result = subprocess.run([sys.executable, attack], check=False, env=env)
        if result.returncode != 0:
            failures += 1

    print(f"\nrun_id={run_id}")
    print(f"attacks={len(ATTACKS)}")
    print(f"failures={failures}")
    if failures:
        print("VERIFICATION BATCH FAILED")
        return 1
    print("VERIFICATION BATCH PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
