# Example Factory Artifact: Adversarial Plan

The adversary derives attacks from the declared guarantees rather than inventing unrelated tests.

| Attack | Target |
|---|---|
| 50 independent concurrent requests for one slot | no double booking |
| Same idempotency key replayed three times | no duplicate side effect |
| Equivalent offset and UTC timestamps | canonical time handling |
| Invalid/failed transaction | no partial commit |

A failing attack is evidence of a broken invariant and becomes input to the Repairer stage.
