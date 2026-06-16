# CONTRIBUTING.md — constitutional-replay-v1

Contribution rules for the constitutional replay kernel.

## First Rule

```text
If it cannot replay locally, it does not count.
```

## Required Reading

Before contributing:

- `BUILD_MATRIX.md`
- `docs/LOCAL_REPLAY_PROTOCOL.md`
- `docs/BASE_NAVIGATION.md`
- `docs/MERKLE_VERIFICATION_EXAMPLES.md`

## v0.1 Contribution Constraints

Forbidden:

- network replay
- Base RPC dependence
- live clocks in replay
- random IDs in replay
- floats
- free-text refusal reasons
- non-`sha256:` canonical replay hashes

## Replay Law

All semantic claims must replay locally.

A passing explorer view is not sufficient.

A passing Base witness is not sufficient.

## Interpreter Law

Interpreters are frozen by version.

Changes require:

- new version
- new interpreter hash
- new vectors
- migration documentation

No silent mutation.

## Required Test Surface

Every replay-impacting contribution must include:

- updated golden vectors if behavior changes
- deterministic replay proof
- refusal-path coverage
- canonicalization stability

## Required Failure Behavior

Contributions must preserve explicit failures:

- HASH_MISMATCH
- POLICY_UNAVAILABLE
- INTERPRETER_HASH_MISMATCH
- REPLAY_DIVERGENCE
- UNHANDLED_REFUSAL

Silent fallback behavior is forbidden.

## Dashboard Boundary

UI and dashboards are visualization layers only.

They must not become semantic authority.

## Base Boundary

Allowed future Base witness roles:

- transaction existence
- Merkle root existence
- event existence
- attestation existence

Forbidden:

- Base proving semantic meaning
- Base overriding replay
- Base repairing missing receipts

## Final Rule

Every accepted contribution must strengthen deterministic replay sovereignty.
