# BAND runbook

Kiln separates the **factory protocol** from the **agent execution surface**.

The hackathon requires the final submission to show a BAND Desktop room that generated the result. This document is the operational bridge for that run; it does not claim that a live BAND run has already happened.

## Room objective

Post the work order as the subject matter. The seats receive generic mandates and produce artifacts through the factory loop:

`Architect -> Modeler -> Builder -> Adversary -> Repairer -> Verifier`

The work order is replaceable. The mandates are not.

## Seat setup

Create one BAND Desktop participant/session per seat:

1. Architect — transform requirements into an implementation plan and identify guarantees.
2. Modeler — identify mutable state, legal transitions, dependencies, and invariants.
3. Builder — implement assigned work and provide executable evidence.
4. Adversary — generate adversarial scenarios against declared guarantees.
5. Repairer — diagnose verified failures, patch the implementation, and add regression coverage.
6. Verifier — independently reproduce critical scenarios and decide whether evidence supports completion.

These mandates remain generic: they name no product, domain, framework, database, or track.

## Work-order message

Give the room the contents of the selected file under `factory/work_orders/`. Do not rewrite the generic seat mandates around the workload.

## Handoff rule

A seat does not hand off “done”. It hands off an artifact with:

- run ID
- work-order ID
- stage
- input artifact references
- output artifact
- commands/evidence used
- status
- unresolved risks

The next seat may act only on an inspectable handoff.

## Failure loop

The normal path is:

`Build -> Attack -> failure -> Repair -> Attack -> Verify`

A failed attack is not a factory failure. It is a factory input for repair. A verification failure blocks completion.

## Evidence

Capture the BAND Desktop room recording, agent messages, stage artifacts, test output, final repository state, and verification result. The repository's deterministic control plane is the state/evidence ledger; BAND is the agent collaboration surface.

## Important limitation

BAND Desktop documentation currently describes Windows as unsupported. If the execution environment cannot run the required BAND Desktop workflow, do not fake the recording or claim a live run. Move the actual room run to a supported environment and preserve the resulting evidence.
