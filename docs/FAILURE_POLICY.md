# Failure Policy

Kiln treats an adversarial failure as useful evidence, not as something to hide.

When an attack fails:
1. Preserve the failure output.
2. Map it to an invariant.
3. Give the reproducible scenario to Repairer.
4. Apply the smallest sound fix.
5. Add regression coverage.
6. Re-run the original attack.
7. Give the result to Verifier for an independent check.

A green-looking dashboard must never replace the underlying evidence.
