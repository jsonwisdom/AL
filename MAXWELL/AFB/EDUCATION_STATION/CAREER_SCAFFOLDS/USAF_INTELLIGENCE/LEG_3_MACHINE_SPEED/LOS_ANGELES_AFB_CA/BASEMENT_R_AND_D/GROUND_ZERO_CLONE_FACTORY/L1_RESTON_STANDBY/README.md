# L1 — Reston Standby / Navigator Architecture

## Mission
Provide a fail-closed standby continuity layer for Leg 3 Machine Speed prototyping.

## Boundary
- R&D architecture only
- `creates_truth: false`
- no claim of a real Reston facility, fiber route, network access, military authority, or operational deployment
- no classified or controlled material
- no identity, credential, or human cloning

## Function
L1 preserves the minimum information required to reconstruct approved research artifacts after loss of a primary working node.

The standby layer manages:
- canonical artifact manifests
- content hashes and version receipts
- source and license metadata
- dependency and lineage maps
- abstract primary/secondary/tertiary transport routes
- recovery order and validation gates
- conflict preservation and correction logs

## Navigator
Navigator is a non-executing architecture role. It selects an eligible recovery path from observed manifests and route health declarations. It cannot declare ownership, authenticity, authority, or successful recovery without verifier receipts.

## Redundancy Doctrine
A copy is not continuity until identity, bytes, rights, lineage, and replay have all been checked.

Standby remains `HELD` until an explicit recovery exercise is authorized and reproduced.
