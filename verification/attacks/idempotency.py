"""Replay attack for the reservation idempotency invariant."""
import os
import httpx

BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")
PAYLOAD = {"resource_id":"idempotency-table","start_at":"2026-09-27T18:00:00+01:00","end_at":"2026-09-27T19:00:00+01:00","guest_name":"Replay Test"}
KEY = "replay-attack-1"

def main() -> int:
    responses = [httpx.post(f"{BASE_URL}/reservations", json=PAYLOAD, headers={"Idempotency-Key": KEY}, timeout=10) for _ in range(3)]
    ids = {response.json().get("id") for response in responses}
    statuses = [response.status_code for response in responses]
    print(f"statuses={statuses}")
    print(f"unique_reservation_ids={len(ids)}")
    passed = statuses == [201, 201, 201] and len(ids) == 1
    print("IDEMPOTENCY ATTACK PASSED" if passed else "IDEMPOTENCY ATTACK FAILED")
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
