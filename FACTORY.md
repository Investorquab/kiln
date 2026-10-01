# Kiln Factory

Kiln is an autonomous software factory built in BAND Desktop. The factory plans work, models requirements and invariants, implements the requested software, attacks the implementation, repairs verified failures, and independently verifies the result.

## Factory seats

- Architect — implementation planning and decomposition
- Modeler — state, invariants, contracts, and executable acceptance reasoning
- Builder — implementation and focused tests
- Adversary — independent failure discovery and adversarial reproduction
- Repairer — root-cause diagnosis, correction, and regression coverage
- Verifier — independent final reproduction and acceptance verification

## Operating rule

The room task/specification defines what is being built. Seat mandates define how each seat works and remain domain-agnostic.

## Official workload

The factory is being used to build the Tablekeeper track from the official Dark Factory specification. The result repository is organized as a sequential set of complete services:

- stage-1 — reservations HTTP API
- stage-2 — browser booking product and combined tables
- stage-3 — policies, history, and recurring reservations
- stage-4 — seating replanning and recurring amendments

## Evidence

The authoritative factory evidence is the BAND room history, Git history, stage artifacts, and independent harness results. Local rehearsals must never be represented as BAND-generated evidence.

## Final documentation

Before submission this document will record the actual seat setup, harness/model versions, design decisions and reasons, failed attempts, measured time/model usage/cost where available, and recovery procedures observed during the official run.
