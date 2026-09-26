"""Run Kiln's executable Tablekeeper attacks as one verification batch."""
from __future__ import annotations

import subprocess
import sys

ATTACKS = [
    "verification/attacks/concurrency.py",
    "verification/attacks/idempotency.py",
    "verification/attacks/timezone.py",
]


def main() -> int:
    failures = 0
    for attack in ATTACKS:
        print(f"\n=== {attack} ===")
        result = subprocess.run([sys.executable, attack], check=False)
        if result.returncode != 0:
            failures += 1

    print(f"\nattacks={len(ATTACKS)}")
    print(f"failures={failures}")
    if failures:
        print("VERIFICATION BATCH FAILED")
        return 1
    print("VERIFICATION BATCH PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
