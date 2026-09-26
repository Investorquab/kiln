# Kiln factory floor

Kiln is organized as a production line rather than a collection of prompts.

## Production units

| Factory concept | Kiln |
|---|---|
| Work order | `factory/work_orders/*.json` |
| Product truth | workload requirement + acceptance criteria |
| Work station | one generic agent seat |
| Handoff | structured stage artifact |
| Control plane | `factory/control_plane.py` |
| Quality gates | schema validation + deterministic verification |
| Attack cell | `verification/attacks/` |
| Evidence ledger | `factory/runs/<run-id>.json` |
| Product output | `app/` |
| Final authority | Verifier evidence, not agent self-report |

## Run lifecycle

`INTAKE -> SPECIFY -> MODEL -> BUILD -> ATTACK -> REPAIR -> VERIFY -> PROVED`

Each transition has a predecessor and an artifact requirement. The control plane prevents a stage from being marked complete when the preceding stage has no evidence.

## Why this shape

Existing software-factory implementations commonly separate intent/specification, execution work, quality gates, and independent verification. Kiln applies that pattern while keeping the hackathon's generic-seat constraint explicit.

The factory should remain useful if the workload changes from Tablekeeper to another clean-room product. Only the work order should change; the seat mandates and evidence protocol should remain stable.
