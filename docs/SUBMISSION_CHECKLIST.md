# Hackathon Submission Checklist

This checklist separates repository/runtime evidence from evidence that must come from the actual BAND Desktop run.

## Factory

- [x] Public GitHub repository: `Investorquab/kiln`.
- [x] At least six distinct generic agent-seat mandates: Architect, Modeler, Builder, Adversary, Repairer, Verifier.
- [x] Generic mandates remain workload-agnostic.
- [x] Tablekeeper is workload input, not an agent mandate.
- [x] Control plane records ordered stages, attempts, artifacts, and evidence events.
- [x] Failure -> repair -> retest -> verifier path exists in the control plane.
- [x] Multiple meaningful repository stages/commits exist.
- [ ] Actual BAND Desktop run for extension is complete and recorded.

## Tablekeeper workload

- [x] Reservation service exists.
- [x] Concurrency attack is executable.
- [x] Idempotency attack is executable.
- [x] Timezone attack is executable.
- [x] Invalid-input/no-state-change behavior is executable.
- [x] Clean-container resource caps are published.
- [x] Clean-container network isolation is published.
- [x] Clean-container verification evidence exists.
- [x] Cancellation extension and five-attack local regression exist.

## BAND-generated evidence still required

These boxes must only be checked from the real BAND Desktop room. Local rehearsal results cannot substitute for them.

- [ ] Architect stage recorded for run `57a2073a77b3`.
- [ ] Modeler stage recorded.
- [ ] Builder stage recorded.
- [ ] Real Adversary failure recorded.
- [ ] Repairer-owned repair commit and repair report recorded.
- [ ] Fresh Adversary post-repair retest recorded.
- [ ] Independent Verifier result recorded.
- [ ] Control-plane ledger reaches `proved`.
- [ ] BAND Desktop room recording/export preserved.

## Recording

The final recording should visibly establish:

1. BAND Desktop room and distinct agent seats.
2. Generic mandates/roles.
3. Requirement entering the factory.
4. Architect -> Modeler -> Builder handoffs.
5. Adversary finding a concrete failure.
6. Repairer making the repair.
7. Adversary retesting the repair.
8. Independent Verifier reproducing the guarantees.
9. Final run ledger reaching `proved`.
10. Resulting Tablekeeper service and verification output.

If an agent restarts or a provider session changes, keep the operational evidence rather than rewriting the story.

## Runtime proof

Final runtime evidence should show:

- fresh no-cache build;
- clean startup;
- database healthy;
- backend running;
- frontend running;
- outbound network blocked;
- CPU/memory limits applied;
- service-to-service communication;
- 50 concurrent conflicting bookings produce 1 creation, 49 conflicts, 0 unexpected;
- stable idempotency replay and rejected tampered replay;
- consistent timezone handling;
- invalid input rejected without creating state.

These runtime results are repository/runtime evidence, not proof that BAND generated the run.

## Extension proof

The cancellation extension adds:

- active -> cancelled transition;
- cancellation idempotency;
- different-reservation key rejection;
- missing reservation rejection;
- replacement booking after cancellation;
- regression of the original guarantees.

The local extension regression is explicitly local evidence.

## Final gate

Before submission:

- [ ] BAND room recording is complete and readable.
- [ ] Public repository points at the intended final commit.
- [ ] No secrets or provider credentials are committed.
- [ ] Clean-container startup has been rerun from a fresh checkout.
- [ ] Final factory ledger passes provenance validation.
- [ ] Independent verifier artifact is passing.
- [ ] README points judges to factory model, runtime contract, and evidence.
- [ ] Demo video shows both factory process and resulting service.
