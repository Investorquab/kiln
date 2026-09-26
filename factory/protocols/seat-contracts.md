# Kiln Seat Contracts

These are task contracts for the generic seats. A task supplies workload-specific context; the seat mandate stays generic.

## Architect
Input: requirement.
Output: implementation plan, risks, mutable-state inventory, required evidence.

## Modeler
Input: requirement and plan.
Output: state model, transitions, invariants, executable-check suggestions.

## Builder
Input: approved plan and model.
Output: implementation, tests, changed-file list, test evidence.

## Adversary
Input: invariants and implementation.
Output: attack cases, commands, observed results, failures.

## Repairer
Input: reproducible failure.
Output: root cause, minimal patch, regression test, rerun evidence.

## Verifier
Input: implementation, invariants, attack evidence.
Output: independent verification result with explicit pass/fail per critical invariant.
