# Evidence Protocol

Every claimed success should point to an artifact that can be inspected.

Minimum evidence:
- exact command or runner
- implementation revision
- scenario identifier
- observed output
- pass/fail result

For concurrency-sensitive claims, include the request count and every non-success class. For idempotency claims, include the number of unique committed IDs. For independent verification, record the verifier stage separately from the builder's test result.
