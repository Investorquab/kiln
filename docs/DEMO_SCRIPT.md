# Kiln Demo Script

## Core message

> Kiln is an autonomous software factory. It takes a software requirement, turns it into an implementation model, builds the result, attacks the implementation, repairs failures, and independently verifies the final result.

The reservation service is the workload. Kiln is the product.

## 1. Show the factory

Show the repository and BAND Desktop room.

Show the six seats:

- Architect
- Modeler
- Builder
- Adversary
- Repairer
- Verifier

Explain that these are separate responsibilities and that the handoffs happen through the BAND room.

## 2. Show the workload

Open `factory/work_orders/tablekeeper.json`.

Explain that Tablekeeper is workload input and that the generic mandates do not contain Tablekeeper-specific instructions.

Show the guarantees:

- no overlapping bookings for one resource;
- safe idempotent retries;
- consistent timezone handling;
- invalid input leaves no state.

## 3. Show the factory run

Show the real BAND run ledger and room activity.

Narrate:

> The Architect turns the requirement into a plan. The Modeler turns the plan into invariants. The Builder implements those invariants. The Adversary then tries to break them.

Show the actual handoffs and inspectable artifacts.

## 4. Show the failure

Do not skip the failure.

Show:

- failing attack;
- violated invariant;
- reproduction;
- Adversary artifact.

Narrate:

> This failure is intentional evidence that the factory does not accept an implementation just because the public tests are green.

## 5. Show the repair

Show the Reviewer/Repairer seat and its own repair commit.

Show:

- root cause;
- smallest sound correction;
- regression coverage;
- repair artifact.

The Repairer must be the owner of this stage.

## 6. Show the retest

The Investigator/Adversary reruns the failed scenario against the repaired implementation.

Then show the extension regression:

- concurrency;
- idempotency;
- timezone;
- invalid input;
- cancellation.

## 7. Show independent verification

Show the Integrator/Verifier independently reproducing the important guarantees.

Narrate:

> The Verifier is separate from the agent that performed the attack. The final proof requires independent reproduction.

Show the passing verifier artifact and the control-plane status.

## 8. Show clean runtime

Show:

- fresh no-cache build;
- internal runtime network;
- resource limits;
- healthy services;
- blocked outbound network;
- adversarial results.

## 9. Close

> The important output is not just working code. It is working code with a traceable chain of planning, attack, repair, retest, and independent proof.

## Recording rules

- Keep BAND Desktop visible whenever showing agent collaboration.
- Capture actual room events.
- Do not present local evidence as BAND evidence.
- Keep relevant restart/provider operational evidence visible.
- Do not manufacture a clean transcript by hiding failed attempts.
