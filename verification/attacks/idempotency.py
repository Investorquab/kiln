"""Replay and key-reuse attacks for idempotency semantics."""
import os
import uuid

import httpx

BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")
RUN_ID = os.environ.get("KILN_ATTACK_RUN_ID", uuid.uuid4().hex[:12])

PAYLOAD = {
    "resource_id": f"idempotency-table-{RUN_ID}",
    "start_at": "2026-09-27T18:00:00+01:00",
    "end_at": "2026-09-27T19:00:00+01:00",
    "guest_name": "Replay Test",
}
KEY = f"replay-attack-{RUN_ID}"


def main() -> int:
    responses = [
        httpx.post(
            f"{BASE_URL}/reservations",
            json=PAYLOAD,
            headers={"Idempotency-Key": KEY},
            timeout=10,
        )
        for _ in range(3)
    ]
    statuses = [response.status_code for response in responses]
    ids = {
        response.json().get("id")
        for response in responses
        if response.headers.get("content-type", "").startswith("application/json")
    }

    changed = {**PAYLOAD, "guest_name": "Tampered Replay"}
    tampered = httpx.post(
        f"{BASE_URL}/reservations",
        json=changed,
        headers={"Idempotency-Key": KEY},
        timeout=10,
    )

    print(f"run_id={RUN_ID}")
    print(f"replay_statuses={statuses}")
    print(f"unique_reservation_ids={len(ids)}")
    print(f"tampered_replay_status={tampered.status_code}")

    passed = (
        statuses == [201, 201, 201]
        and len(ids) == 1
        and tampered.status_code == 409
    )
    print("IDEMPOTENCY ATTACK PASSED" if passed else "IDEMPOTENCY ATTACK FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
