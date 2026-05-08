# Claim Spec v0

A Claim is epistemic state.

It records an assertion as immutable, content-addressed state. It does not claim to record the world.

## Fields

- `id`: SHA-256 content hash of canonical claim payload.
- `body`: The assertion text.
- `asserted_at`: Unix timestamp.
- `asserted_by`: Actor key id or demo identity.
- `uncertainty`: Number from `0.0` to `1.0`.
- `tags`: Optional list of short strings.
- `source_refs`: Optional external references or source labels.
- `branch`: Branch name, default `main`.

## Rule

Claims store state.

Transforms store epistemic motion.

The ledger records transformations, not the world.
