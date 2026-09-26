# Evidence Protocol

Every claimed verification result should be traceable to an actual run.

## Minimum record

- run ID
- implementation revision
- exact command
- scenario ID
- observed output
- pass/fail result
- relevant concurrency count and response classes
- idempotency reservation IDs
- independent verifier result

## Evidence lifecycle

Scenario -> Execute -> Observe -> Record -> Diagnose/Repair -> Re-run -> Independently Verify

Templates and example artifacts describe evidence shape; they are not evidence by themselves. Failed attacks remain part of development history and must go through the repair policy.