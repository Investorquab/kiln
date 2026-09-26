# Kiln Demo Script

## Input
Give Kiln a clean-room Tablekeeper requirement: reservations must not double-book a resource, retries must be safe, and timestamps must be handled consistently.

## Factory run
Architect → Modeler → Builder → Adversary → Repairer → Verifier.

## Evidence to show
- The generated plan and invariants.
- The implementation commit.
- An adversarial attack that targets the critical invariant.
- A failure and the resulting repair, when one occurs.
- A final independent verification report.

The demo should show the factory process, not only the finished reservation UI.