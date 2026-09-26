from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from app.main import app, _idempotency, _store


client = TestClient(app)


def setup_function() -> None:
    _store.clear()
    _idempotency.clear()


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
    second = client.post("/reservations", json={**payload(), "guest_name": "Second"}, headers={"Idempotency-Key": "b"})

    assert first.status_code == 201
    assert second.status_code == 409


def test_retry_with_same_idempotency_key_returns_same_reservation():
    first = client.post("/reservations", json=payload(), headers={"Idempotency-Key": "retry-1"})
    retry = client.post("/reservations", json={**payload(), "guest_name": "Changed"}, headers={"Idempotency-Key": "retry-1"})

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
