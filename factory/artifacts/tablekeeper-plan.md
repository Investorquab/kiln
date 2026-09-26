# Example Factory Artifact: Tablekeeper Plan

## Requirement
Build a clean-room reservation service that prevents double-booking, safely handles retries, and treats equivalent timestamps consistently.

## Mutable state
- Reservation records
- Resource occupancy
- Idempotency keys

## Critical guarantees
- No overlapping committed reservations for one resource.
- Replaying an idempotency key does not create another record.
- Equivalent timestamps resolve to the same instants.
- Failed operations do not partially commit.

## Build decomposition
1. API contract and validation.
2. Transactional persistence.
3. Resource-scoped serialization.
4. Executable invariant tests.
5. Adversarial attack harness.
6. Independent verification and evidence.
