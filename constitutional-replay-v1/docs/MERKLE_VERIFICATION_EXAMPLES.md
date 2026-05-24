# MERKLE_VERIFICATION_EXAMPLES.md — constitutional-replay-v1

Concrete examples for Merkle inclusion and local replay boundaries.

This document is educational and implementation-guiding.

It is not executable verifier code.

## Core Rule

```text
Merkle proof proves inclusion.
Local replay proves meaning.
```

A valid Merkle proof does not prove that a receipt is semantically valid.

A valid Base witness does not prove that a receipt is semantically valid.

Semantic validity requires local replay.

## Minimal Objects

### Full Receipt

```json
{
  "receipt_version": "receipt.v1",
  "receipt_id": "sha256:receipt001",
  "policy_hash": "sha256:policy001",
  "policy_version": "policy.v1",
  "interpreter_hash": "sha256:interpreter001",
  "replay_engine_version": "replay.v1",
  "action": "transfer_usdc",
  "result": "REFUSAL",
  "refusal_code": "SPEND_LIMIT_EXCEEDED",
  "context_hash": "sha256:context001"
}
```

### Receipt Summary

```json
{
  "receipt_hash": "sha256:receipt001",
  "policy_hash": "sha256:policy001",
  "interpreter_hash": "sha256:interpreter001",
  "result": "REFUSAL",
  "risk_tier": "HIGH",
  "reason_code": "SPEND_LIMIT_EXCEEDED",
  "batch_id": "batch-001"
}
```

The summary supports filtering.

The full receipt supports replay.

## Example Batch

```json
{
  "batch_id": "batch-001",
  "hash_algorithm": "sha256",
  "leaves": [
    "sha256:receipt001",
    "sha256:receipt002",
    "sha256:receipt003"
  ],
  "merkle_root": "sha256:root001"
}
```

## Verification Order

A verifier must perform checks in this order:

1. Load full receipt locally.
2. Canonicalize full receipt.
3. Recompute `receipt_hash` using `sha256:` over canonical bytes.
4. Confirm recomputed hash matches the summary leaf.
5. Verify Merkle inclusion against the batch root.
6. Replay the receipt locally against the policy and interpreter.
7. Report replay status and witness status separately.

## Expected Result Shape

```json
{
  "receipt_hash": "sha256:receipt001",
  "merkle_status": "INCLUDED",
  "replay_status": "REFUSAL_CONFIRMED",
  "witness_status": "NOT_CHECKED",
  "semantic_authority": "LOCAL_REPLAY"
}
```

## Failure Examples

### Case 1 — Merkle Included, Replay Fails

```json
{
  "merkle_status": "INCLUDED",
  "replay_status": "REPLAY_DIVERGENCE",
  "semantic_authority": "LOCAL_REPLAY",
  "final_status": "INVALID_SEMANTIC_RECEIPT"
}
```

Meaning:

- The receipt was included in a batch.
- The batch may even be witnessed on Base later.
- The semantic claim still fails because local replay diverged.

### Case 2 — Replay Succeeds, No Base Witness

```json
{
  "merkle_status": "INCLUDED",
  "replay_status": "REFUSAL_CONFIRMED",
  "witness_status": "NOT_CHECKED",
  "semantic_authority": "LOCAL_REPLAY",
  "final_status": "VALID_LOCAL_REPLAY"
}
```

Meaning:

- The receipt is locally valid.
- It has not yet been checked against Base.
- It still counts for local replay legitimacy.

### Case 3 — Base Witness Exists, Receipt Missing

```json
{
  "merkle_status": "UNOBSERVED",
  "replay_status": "RECEIPT_UNAVAILABLE",
  "witness_status": "BASE_ROOT_CONFIRMED",
  "semantic_authority": "LOCAL_REPLAY",
  "final_status": "INVALID_UNREPLAYABLE"
}
```

Meaning:

- Base confirms a public root existed.
- The local receipt is missing.
- The claim does not count because it cannot replay locally.

## Merkle Forest Rule

```text
Base can witness the forest.
Replay proves the path.
```

A forest marker is useful only when the path from leaf to receipt to replay remains walkable.

## v0.1 Boundary

v0.1 does not require Base.

v0.1 may compute local Merkle roots and proofs.

v0.1 must not claim Base witness status.

## Final Line

Inclusion is not meaning.

Witness is not replay.

Replay is the semantic gate.
