# Proofs, Not Power

## CIVIC_KERNEL_V1 Federation Doctrine

CIVIC_KERNEL_V1 answers a core constitutional systems question:

> How do many sovereign governance runtimes coordinate without creating a hidden sovereign above them?

The answer is:

> Coordinate over proofs, not power.

## Leaf Runtime

Each state runtime is treated as a constitutional VM with:

- immutable baseline graph
- scoped overlays
- typed deltas
- topology predicates
- sovereignty arbitration
- replay verification
- epoch attestation

A state epoch is valid only when its runtime can be replayed from repo bytes and its Merkle root recomputes.

## Federation Runtime

The federation layer sees only:

- epoch ids
- epoch roots
- attestation metadata
- compact definitions
- compact ledgers

It does not read, rewrite, infer, or mutate state baselines.

## History Layer

FED_EPOCH_GRAPH_V1 is a directed acyclic graph of replay-verified governance states.

Nodes are:

- STATE_EPOCH
- COMPACT_EPOCH
- FEDERATION_EPOCH

Edges are dependency relations only.

No edge may mutate, invalidate, supersede, rebase, or rewrite an ancestor.

## Core Invariant

No state, compact, federation node, or descendant graph element may rewrite an ancestor baseline.

Time is recorded.
Power is not centralized.
Coordination is proven by replay.

## Doctrine

Narrative is not authority.
Replay is authority.

Federation is a proof mesh, not a sovereign super-runtime.
