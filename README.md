# Kiln

Kiln is an autonomous software factory that turns software requirements into working software, attacks its own implementation, repairs verified failures, and independently verifies the result.

## Core loop

`Requirement → Model → Build → Attack → Repair → Verify → Evidence`

The first demonstration workload is a clean-room reservation system inspired by Tablekeeper. The workload is deliberately separate from Kiln's generic factory mandates.

## Repository layout

- `app/` — demonstration application
- `factory/` — generic factory contracts and agent mandates
- `verification/` — invariant and adversarial verification
- `docs/` — architecture and build notes
