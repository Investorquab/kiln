import os
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.main import app, connection, ensure_schema


pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL is required for integration tests",
)

client = TestClient(app)


def setup_function() -> None:
    ensure_schema()
    with connection() as conn:
        conn.execute("TRUNCATE cancellation_requests, reservations")
        conn.commit()


def payload():
    return {
        "resource_id": "table-1",
        "start_at": "2026-09-26T18:00:00+01:00",
        "end_at": "2026-09-26T19:00:00+01:00",
        "guest_name": "Test Guest",
    }


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_overlapping_reservation_is_rejected():
    first = client.post("/reservations", json=payload(), headers={"Idempotency-Key": "a"})
    second = client.post(
        "/reservations",
        json={**payload(), "guest_name": "Second"},
        headers={"Idempotency-Key": "b"},
    )
    assert first.status_code == 201
    assert second.status_code == 409


def test_retry_with_same_idempotency_key_returns_same_reservation():
    first = client.post("/reservations", json=payload(), headers={"Idempotency-Key": "retry-1"})
    retry = client.post(
        "/reservations",
        json={**payload(), "guest_name": "Changed"},
        headers={"Idempotency-Key": "retry-1"},
    )
    assert first.status_code == 201
    assert retry.status_code == 409


def test_same_idempotency_key_same_payload_is_replay_safe():
    first = client.post("/reservations", json=payload(), headers={"Idempotency-Key": "replay-safe"})
    retry = client.post("/reservations", json=payload(), headers={"Idempotency-Key": "replay-safe"})
    assert first.status_code == 201
    assert retry.status_code == 201
    assert retry.json()["id"] == first.json()["id"]


def test_timezone_equivalent_windows_conflict():
    first = client.post("/reservations", json=payload(), headers={"Idempotency-Key": "tz-a"})
    equivalent = {
        **payload(),
        "start_at": "2026-09-26T17:30:00Z",
        "end_at": "2026-09-26T18:30:00Z",
    }
    second = client.post("/reservations", json=equivalent, headers={"Idempotency-Key": "tz-b"})
    assert first.status_code == 201
    assert second.status_code == 409


def test_naive_timestamp_is_rejected():
    invalid = {
        **payload(),
        "start_at": "2026-09-26T18:00:00",
        "end_at": "2026-09-26T19:00:00",
    }
    response = client.post("/reservations", json=invalid, headers={"Idempotency-Key": "naive-time"})
    assert response.status_code == 422


def test_concurrent_same_slot_has_single_winner():
    def attempt(index: int):
        return client.post(
            "/reservations",
            json=payload(),
            headers={"Idempotency-Key": f"concurrent-{index}"},
        ).status_code

    with ThreadPoolExecutor(max_workers=20) as pool:
        statuses = list(pool.map(attempt, range(20)))

    assert statuses.count(201) == 1
    assert statuses.count(409) == 19


def test_same_idempotency_key_across_resources_is_rejected():
    first = {
        "resource_id": "key-race-a",
        "start_at": "2026-10-01T18:00:00+01:00",
        "end_at": "2026-10-01T19:00:00+01:00",
        "guest_name": "First",
    }
    second = {**first, "resource_id": "key-race-b", "guest_name": "Second"}

    r1 = client.post("/reservations", json=first, headers={"Idempotency-Key": "global-key"})
    r2 = client.post("/reservations", json=second, headers={"Idempotency-Key": "global-key"})

    assert r1.status_code == 201
    assert r2.status_code == 409


def test_cancellation_is_idempotent():
    created = client.post(
        "/reservations",
        json=payload(),
        headers={"Idempotency-Key": "cancel-create"},
    )
    reservation_id = created.json()["id"]

    first = client.delete(
        f"/reservations/{reservation_id}",
        headers={"Idempotency-Key": "cancel-1"},
    )
    retry = client.delete(
        f"/reservations/{reservation_id}",
        headers={"Idempotency-Key": "cancel-1"},
    )

    assert created.status_code == 201
    assert first.status_code == 204
    assert retry.status_code == 204

    with connection() as conn:
        row = conn.execute(
            "SELECT status FROM reservations WHERE id = %s",
            (reservation_id,),
        ).fetchone()
    assert row[0] == "cancelled"


def test_cancellation_key_cannot_target_different_reservation():
    first = client.post(
        "/reservations",
        json=payload(),
        headers={"Idempotency-Key": "cancel-a-create"},
    )
    second_payload = {
        **payload(),
        "resource_id": "table-2",
        "guest_name": "Second Guest",
    }
    second = client.post(
        "/reservations",
        json=second_payload,
        headers={"Idempotency-Key": "cancel-b-create"},
    )

    first_id = first.json()["id"]
    second_id = second.json()["id"]

    cancelled = client.delete(
        f"/reservations/{first_id}",
        headers={"Idempotency-Key": "cancel-same-key"},
    )
    wrong_target = client.delete(
        f"/reservations/{second_id}",
        headers={"Idempotency-Key": "cancel-same-key"},
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert cancelled.status_code == 204
    assert wrong_target.status_code == 409


def test_cancelling_missing_reservation_does_not_create_state():
    import uuid

    missing = client.delete(
        f"/reservations/{uuid.uuid4()}",
        headers={"Idempotency-Key": "cancel-missing"},
    )

    assert missing.status_code == 404
    assert client.get("/reservations").json() == []


def test_cancelled_reservation_no_longer_blocks_new_booking():
    created = client.post(
        "/reservations",
        json=payload(),
        headers={"Idempotency-Key": "cancel-rebook-create"},
    )
    reservation_id = created.json()["id"]

    cancelled = client.delete(
        f"/reservations/{reservation_id}",
        headers={"Idempotency-Key": "cancel-rebook"},
    )
    replacement = client.post(
        "/reservations",
        json=payload(),
        headers={"Idempotency-Key": "replacement-booking"},
    )

    assert created.status_code == 201
    assert cancelled.status_code == 204
    assert replacement.status_code == 201
