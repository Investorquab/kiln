# BAND Desktop Room Plan

Kiln is intended to be demonstrated as a multi-seat software factory in BAND Desktop.

## Required seats

Use at least three distinct coding-agent seats. Kiln defines six generic seats:

1. Architect
2. Modeler
3. Builder
4. Adversary
5. Repairer
6. Verifier

The mandates live in `factory/mandates/` and are deliberately workload-agnostic.

## Handoff sequence

Architect → Modeler → Builder → Adversary → Repairer → Verifier

Each handoff should attach the relevant artifact or evidence. The next seat should work from the artifact rather than relying on an informal chat summary.

## Demonstration rule

The final recording must visibly show the BAND Desktop room that generated the solution. The repo alone is not the factory demonstration.

## Important

This file describes Kiln's room contract; it does not claim that BAND Desktop has been configured or that a live agent run has succeeded. Those claims require an actual room run.
