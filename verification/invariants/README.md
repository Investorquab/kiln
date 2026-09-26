# Invariants

Declared system guarantees become executable verification targets.

Initial reservation workload targets:
- no conflicting reservations can commit;
- retries do not create duplicate reservations;
- a failed operation does not partially consume a reservation;
- time comparisons use one canonical representation.
