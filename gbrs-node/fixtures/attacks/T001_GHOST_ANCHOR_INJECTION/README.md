# T001_GHOST_ANCHOR_INJECTION

## Purpose

This fixture tests whether a GBRS verifier detects an out-of-band ENS routing mutation that is not backed by a canonical receipt.

## Attack

The canonical truth surface projects `example.eth` to:

```text
ipfs://canonical-dashboard-cid
```

The live ENS state has been mutated to:

```text
ipfs://ghost-anchor-cid
```

No canonical receipt authorizes the mutated contenthash.

## Expected Verdict

```text
DIVERGENT
```

## Required Action

A compliant verifier MUST mark the live ENS record as a Ghost Anchor and require rollback-visible reconciliation.

## Core Rule

```text
No receipt -> no lineage -> no projection -> no route.
```
