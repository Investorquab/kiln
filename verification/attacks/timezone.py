"""Timezone-equivalence attack for canonical interval handling."""
import os
import uuid

import httpx

BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")
RUN_ID = os.environ.get("KILN_ATTACK_RUN_ID", uuid.uuid4().hex[:12])


def main() -> int:
    resource = f"timezone-table-{RUN_ID}"
    first = {
        "resource_id": resource,
        "start_at": "2026-09-28T18:00:00+01:00",
        "end_at": "2026-09-28T19:00:00+01:00",
        "guest_name": "Timezone A",
    }
    equivalent = {
        "resource_id": resource,
        "start_at": "2026-09-28T17:00:00Z",
        "end_at": "2026-09-28T18:00:00Z",
        "guest_name": "Timezone B",
    }
    r1 = httpx.post(
        f"{BASE_URL}/reservations",
        json=first,
        headers={"Idempotency-Key": f"tz-a-{RUN_ID}"},
        timeout=10,
    )
    r2 = httpx.post(
        f"{BASE_URL}/reservations",
        json=equivalent,
        headers={"Idempotency-Key": f"tz-b-{RUN_ID}"},
        timeout=10,
    )
    print(f"run_id={RUN_ID}")
    print(f"first={r1.status_code}")
    print(f"equivalent={r2.status_code}")
    passed = r1.status_code == 201 and r2.status_code == 409
    print("TIMEZONE ATTACK PASSED" if passed else "TIMEZONE ATTACK FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
