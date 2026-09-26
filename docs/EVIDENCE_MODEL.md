# Kiln Evidence Model

Kiln treats the run ledger as the control-plane record and stage artifacts as the evidence payload.

## Provenance chain

A concrete run should be traceable as:

`factory run ID → stage → stage artifact → evidence event → verification run ID`

The ledger records:

- the work order and requirement;
- ordered stage state;
- artifact path for each completed stage;
- attempt number;
- timestamped evidence events.

The verifier artifact additionally carries the identifier of the executable verification run.

## Local rehearsal

`factory/runtime/rehearse_local_run.py` creates a concrete local ledger and executes the real Tablekeeper attack suite.

`factory/runtime/validate_run_ledger.py <run-id>` verifies that:

1. every completed stage has a real artifact;
2. every completed stage has a matching evidence event;
3. evidence points to the artifact recorded by the stage;
4. stage attempts match the latest evidence event;
5. a `proved` run has a passing verifier artifact with a verification run ID.

These checks establish repository-level evidence integrity. They do **not** establish that BAND Desktop generated the run.

## BAND evidence

The eventual submission must add the actual BAND Desktop room recording and stage messages/artifacts from the real agent run. Local rehearsal evidence must remain clearly labeled as local.
