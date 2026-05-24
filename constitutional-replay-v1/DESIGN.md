# DESIGN.md — constitutional-replay-v1

Formal design surface for the constitutional replay kernel.

## Kernel Rule

```text
If it cannot replay locally, it does not count.
```

## Core Doctrine

```text
No witness, no claim.
No receipt, no ratification.
No replay, no settlement.
```

## Semantic Authority

Local replay is semantic authority.

Base witness infrastructure is public commitment visibility only.

## v0.1 Architecture

v0.1 establishes:

- deterministic canonicalization
- SHA-256 receipt binding
- frozen policy interpreter model
- refusal-first replay
- local batch construction
- static visualization only

v0.1 explicitly excludes:

- Base RPC dependence
- hosted replay
- network replay
- live clocks
- entropy
- probabilistic interpretation
- semantic mutation via witness layers

## Frozen Interpreter Law

Each receipt binds:

```json
{
  "policy_hash": "sha256:...",
  "policy_version": "policy.v1",
  "interpreter_hash": "sha256:...",
  "replay_engine_version": "replay.v1"
}
```

Rule:

```text
Same receipt + same policy + same interpreter = same verdict forever.
```

## Replay Order

1. Load receipt.
2. Canonicalize.
3. Recompute hash.
4. Resolve local policy.
5. Verify interpreter hash.
6. Re-run deterministic interpreter.
7. Compare original and replay verdict.
8. Emit replay result.

## Merkle Law

```text
Merkle proof proves inclusion.
Local replay proves meaning.
```

Batch roots support discovery and witness.

Replay remains the semantic gate.

## Failure Philosophy

The system must fail closed.

Allowed:

- explicit refusal
- explicit replay divergence
- explicit missing policy
- explicit hash mismatch

Forbidden:

- silent fallback
- auto-upgrading interpreters
- heuristic reconstruction
- witness overriding replay

## Dashboard Boundary

Dashboards may display replay outputs.

Dashboards must not become replay authority.

## Base Boundary

```text
Base can witness the forest.
Replay proves the path.
```

## Final Goal

Portable economic memory that survives:

- infrastructure loss
- hosted service failure
- explorer shutdown
- operator disappearance
- chain witness loss

through sovereign deterministic replay.
