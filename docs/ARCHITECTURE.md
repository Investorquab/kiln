# Kiln Architecture

Kiln separates the software-building loop from the workload used to demonstrate it.

## Agent seats
1. Architect — requirements and implementation plan.
2. Modeler — state, transitions, invariants.
3. Builder — implementation and tests.
4. Adversary — hostile scenarios and executable attacks.
5. Repairer — root-cause diagnosis and regression fixes.
6. Verifier — independent reproduction and evidence review.

Each mandate is generic and workload-agnostic.

## Evidence flow

Requirement → Plan → Model/Invariants → Implementation → Attacks → Repair/Regression → Independent Verification → Evidence

The Tablekeeper reservation service is the first demonstration workload. The factory protocol is the product.
