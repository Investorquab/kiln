# Tablekeeper Work Order

## Goal

Build a clean-room reservation product in the style of a familiar restaurant reservation service. The implementation must be independently authored and must not copy proprietary source code, assets, or implementation details.

## Required guarantees

1. A resource cannot be double-booked for overlapping intervals.
2. Concurrent requests must not create conflicting reservations.
3. Repeating a request with the same idempotency key must not create a second reservation.
4. Reusing an idempotency key for different request data must be rejected.
5. Equivalent timezone representations must refer to the same instant.
6. Invalid timestamps must be rejected without creating state.

## Factory instruction

Treat this as workload input, not an agent mandate. The factory should derive the plan, invariants and attacks, build the workload, attack it, repair reproducible failures, independently verify the guarantees, and preserve run evidence.
