# Agent Handoff Contract

Every Kiln stage produces a small artifact that the next stage can inspect.

## Required handoff fields
- stage
- task
- inputs
- outputs
- changed files
- tests/checks run
- evidence
- open failures
- next action

An agent must not report a successful handoff without evidence. A downstream stage should be able to reproduce the important claim from the artifact alone.

## Seat order
Architect → Modeler → Builder → Adversary → Repairer → Verifier

The mandates remain generic; workload-specific details belong in the task/artifact payload, not in the seat mandate.
