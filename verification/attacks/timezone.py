"""Timezone-equivalence attack for canonical interval handling."""
import os
import httpx

BASE_URL = os.environ.get("KILN_BASE_URL", "http://localhost:8000")

def main() -> int:
    first = {"resource_id":"timezone-table","start_at":"2026-09-28T18:00:00+01:00","end_at":"2026-09-28T19:00:00+01:00","guest_name":"Timezone A"}
    equivalent = {"resource_id":"timezone-table","start_at":"2026-09-28T17:00:00Z","end_at":"2026-09-28T18:00:00Z","guest_name":"Timezone B"}
    r1 = httpx.post(f"{BASE_URL}/reservations", json=first, headers={"Idempotency-Key":"tz-a"}, timeout=10)
    r2 = httpx.post(f"{BASE_URL}/reservations", json=equivalent, headers={"Idempotency-Key":"tz-b"}, timeout=10)
    print(f"first={r1.status_code}")
    print(f"equivalent={r2.status_code}")
    passed = r1.status_code == 201 and r2.status_code == 409
    print("TIMEZONE ATTACK PASSED" if passed else "TIMEZONE ATTACK FAILED")
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
