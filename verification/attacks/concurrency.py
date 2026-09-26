"""Adversarial concurrency scenario for the reservation workload."""
from concurrent.futures import ThreadPoolExecutor
import os
import uuid

import httpx

BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")
WORKERS = int(os.environ.get("KILN_ATTACK_WORKERS", "50"))
RUN_ID = os.environ.get("KILN_ATTACK_RUN_ID", uuid.uuid4().hex[:12])

PAYLOAD = {
    "resource_id": f"attack-table-{RUN_ID}",
    "start_at": "2026-09-26T18:00:00+01:00",
    "end_at": "2026-09-26T19:00:00+01:00",
    "guest_name": "Adversarial Test",
}


def attempt(index: int) -> int:
    response = httpx.post(
        f"{BASE_URL}/reservations",
        json=PAYLOAD,
        headers={"Idempotency-Key": f"attack-{RUN_ID}-{index}"},
        timeout=10,
    )
    return response.status_code


def main() -> int:
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        statuses = list(pool.map(attempt, range(WORKERS)))

    winners = statuses.count(201)
    conflicts = statuses.count(409)
    unexpected = WORKERS - winners - conflicts

    print(f"run_id={RUN_ID}")
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
