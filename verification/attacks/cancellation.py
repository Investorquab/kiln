"""Adversarial cancellation scenarios for the Tablekeeper extension."""
from concurrent.futures import ThreadPoolExecutor
import os
import uuid

import httpx

BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")
RUN_ID = os.environ.get("KILN_ATTACK_RUN_ID", uuid.uuid4().hex[:12])


def create_reservation() -> str:
    response = httpx.post(
        f"{BASE_URL}/reservations",
        json={
            "resource_id": f"cancel-table-{RUN_ID}",
            "start_at": "2026-09-30T18:00:00+01:00",
            "end_at": "2026-09-30T19:00:00+01:00",
            "guest_name": "Cancellation Attack",
        },
        headers={"Idempotency-Key": f"cancel-create-{RUN_ID}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["id"]


def main() -> int:
    reservation_id = create_reservation()

    def same_key(_: int) -> int:
        return httpx.delete(
            f"{BASE_URL}/reservations/{reservation_id}",
            headers={"Idempotency-Key": f"cancel-replay-{RUN_ID}"},
            timeout=10,
        ).status_code

    with ThreadPoolExecutor(max_workers=20) as pool:
        replay_statuses = list(pool.map(same_key, range(20)))

    replay_passed = replay_statuses == [204] * 20

    second_reservation = create_reservation()

    def competing_key(index: int) -> int:
        return httpx.delete(
            f"{BASE_URL}/reservations/{second_reservation}",
            headers={"Idempotency-Key": f"cancel-compete-{RUN_ID}-{index}"},
            timeout=10,
        ).status_code

    with ThreadPoolExecutor(max_workers=20) as pool:
        competing_statuses = list(pool.map(competing_key, range(20)))

    competing_passed = (
        competing_statuses.count(204) == 1
        and competing_statuses.count(409) == 19
    )

    missing = httpx.delete(
        f"{BASE_URL}/reservations/{uuid.uuid4()}",
        headers={"Idempotency-Key": f"cancel-missing-{RUN_ID}"},
        timeout=10,
    )

    print(f"run_id={RUN_ID}")
    print(f"same_key_replay_statuses={replay_statuses}")
    print(f"competing_key_statuses={competing_statuses}")
    print(f"missing_reservation_status={missing.status_code}")

    passed = replay_passed and competing_passed and missing.status_code == 404
    print(
        "CANCELLATION ATTACK PASSED"
        if passed
        else "CANCELLATION ATTACK FAILED"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
