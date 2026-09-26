# Kiln Factory Loop

1. Specify — convert requirements into an implementation plan and explicit guarantees.
2. Model — represent state, transitions, dependencies, and invariants.
3. Build — implement the approved slice with tests and evidence.
4. Attack — derive adversarial scenarios from the invariants and execute them.
5. Diagnose/Repair — isolate failures, patch the implementation, and add regression coverage.
6. Verify — independently reproduce the critical scenarios and confirm the guarantees.
7. Prove — preserve machine-readable evidence showing what was checked and what passed.

A stage cannot claim success merely because an earlier stage produced an artifact. Later stages must consume and verify that artifact.