# Kiln Demo Script

## 1. Introduce the factory
Show the BAND Desktop room and the generic seats.

## 2. Give the factory a clean-room requirement
Build a reservation service where a resource cannot be double-booked, retries are safe, and equivalent timestamps are handled consistently.

## 3. Show the planning handoff
Architect produces a plan. Modeler converts the plan into explicit invariants.

## 4. Show implementation
Builder implements the workload and tests.

## 5. Attack the implementation
Adversary runs the concurrency, idempotency, timezone, and boundary attacks.

## 6. Repair
If an attack fails, Repairer identifies the root cause, patches it, and adds regression coverage.

## 7. Independently verify
Verifier reruns the critical scenarios and records explicit evidence.

## 8. End on proof
Show the final report and the running workload. Do not claim a pass until the live run produced the evidence.
