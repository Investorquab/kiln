"""Boundary attack: reject malformed time input without creating state."""
import os
import uuid

import httpx

BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")
RUN_ID = os.environ.get("KILN_ATTACK_RUN_ID", uuid.uuid4().hex[:12])
KEY = f"invalid-time-{RUN_ID}"


def main() -> int:
    payload = {
        "resource_id": f"invalid-input-table-{RUN_ID}",
        "start_at": "2026-09-29T18:00:00",
        "end_at": "2026-09-29T19:00:00",
        "guest_name": "Invalid Input",
    }
    response = httpx.post(
        f"{BASE_URL}/reservations",
        json=payload,
        headers={"Idempotency-Key": KEY},
        timeout=10,
    )
    after = httpx.get(f"{BASE_URL}/reservations", timeout=10)
    records = [
        item for item in after.json()
        if item["idempotency_key"] == KEY
    ]
    passed = response.status_code == 422 and not records
    print(f"run_id={RUN_ID}")
    print(f"status={response.status_code}")
    print(f"created_records={len(records)}")
    print("INVALID INPUT ATTACK PASSED" if passed else "INVALID INPUT ATTACK FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
