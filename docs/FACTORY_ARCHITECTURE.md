# Kiln Factory Architecture

Kiln is split into two layers.

## Control plane

The control plane owns the rules of a factory run: work order, ordered stages, artifact handoffs, stage state, evidence references, and failure boundaries. `factory/control_plane.py` is a small deterministic local implementation of those rules.

## Agent execution plane

BAND Desktop is the collaboration and execution surface for the coding agents. The six generic seats are Architect, Modeler, Builder, Adversary, Repairer, and Verifier.

Agents produce artifacts. They do not redefine stage order or declare independent verification merely because they say a task passed.

## Factory contract

Work Order -> Architect -> Modeler -> Builder -> Adversary -> Repairer -> Verifier -> PROVED

A failure goes through the repair path. It is not erased.

## Workload boundary

Tablekeeper lives under `factory/workloads/` because it is a workload supplied to Kiln.

**Kiln = factory. Tablekeeper = product the factory is asked to build.**

The same contract can consume a different workload, including Pocketful, without changing the generic mandates.
