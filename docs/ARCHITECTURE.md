# Kiln Architecture

Kiln separates the generic software-factory process from the demonstration workload.

1. Architect — turns requirements into an implementation plan and identifies guarantees.
2. Modeler — identifies mutable state, legal transitions, dependencies, and invariants.
3. Builder — implements assigned work and provides evidence.
4. Adversary — generates scenarios intended to break declared invariants.
5. Repairer — diagnoses verified failures, makes the smallest corrective change, and adds regression coverage.
6. Verifier — independently reproduces relevant scenarios and reports evidence.

The first workload is a reservation system. Its central guarantee is that conflicting reservations cannot both be committed for the same resource and time window, including under concurrency and retries.

Factory mandates remain workload-agnostic.
