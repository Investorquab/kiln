"""Adversarial concurrency scenarios for the reservation workload.

Run against a live Kiln backend. The attack harness deliberately sends
independent idempotency keys to the same resource and time window.
"""
from concurrent.futures import ThreadPoolExecutor
import os
import sys

import httpx


BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")
WORKERS = int(os.environ.get("KILN_ATTACK_WORKERS", "50"))


PAYLOAD = {
    "resource_id": "attack-table",
    "start_at": "2026-09-26T18:00:00+01:00",
    "end_at": "2026-09-26T19:00:00+01:00",
    "guest_name": "Adversarial Test",
}


def attempt(index: int) -> int:
    response = httpx.post(
        f"{BASE_URL}/reservations",
        json=PAYLOAD,
        headers={"Idempotency-Key": f"attack-{index}"},
        timeout=10,
    )
    return response.status_code


def main() -> int:
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        statuses = list(pool.map(attempt, range(WORKERS)))

    winners = statuses.count(201)
    conflicts = statuses.count(409)
    unexpected = WORKERS - winners - conflicts

    print(f"requests={WORKERS}")
    print(f"created={winners}")
    print(f"conflicts={conflicts}")
    print(f"unexpected={unexpected}")

    if winners != 1 or conflicts != WORKERS - 1 or unexpected:
        print("ATTACK FAILED: reservation invariant violated")
        return 1

    print("ATTACK PASSED: exactly one reservation committed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
