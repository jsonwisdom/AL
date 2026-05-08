# EPOCH 02 — Attestation Payload Schema v1

## Purpose

Define the canonical, closed-world schema for the attestation payload — the object that operators sign, verifiers replay, and courts treat as the only admissible representation of an attestation event.

This schema binds together:

- the kernel
- the schema
- the `evidence_root`
- the verdict
- the observer set
- the exclusion set
- the epoch
- the replay contract

The attestation payload is the constitutional envelope. It must be:

- canonical
- replay-derivable
- hash-stable
- surface-bounded
- operator-signable
- court-verifiable

No field may be added, removed, or reinterpreted.

---

## 1. Canonical Serialization

All attestation payloads MUST be serialized using JCS / RFC 8785.

This ensures:

- deterministic field ordering
- deterministic whitespace
- deterministic encoding
- deterministic hashing
- deterministic replay

No alternate serialization is admissible.

---

## 2. Attestation Payload Schema

The payload MUST contain exactly the following fields:

```json
{
  "attestation_hash": "<sha256>",
  "evidence_root": "<sha256>",
  "kernel_hash": "<sha256>",
  "schema_hash": "<sha256>",
  "surface_version": "<uint32>",
  "epoch": "<uint32>",
  "verdict": "<VERDICT_ATOM>",
  "observer_set": ["<observer_id>"],
  "excluded_observers": ["<observer_id>"],
  "quorum_size": "<uint32>",
  "valid_observer_count": "<uint32>",
  "timestamp": "<uint64>"
}
```

### 2.1 Field Definitions

#### `attestation_hash`

Hash of the canonical payload excluding this field.

Self-referential integrity anchor.

#### `evidence_root`

Merkle root defined in `EPOCH_02_EVIDENCE_ROOT_SPEC_V1.md`.

#### `kernel_hash`

Hash of the kernel declared for the epoch.

#### `schema_hash`

Hash of the schema declared for the epoch.

#### `surface_version`

Version of the Allowed Surface Enum.

#### `epoch`

Epoch number.

#### `verdict`

One of:

```text
PASS
FAIL
TAINTED
INDETERMINATE
NOT_A_VERDICT
```

#### `observer_set`

All observers that participated before exclusion.

#### `excluded_observers`

Observers excluded by the rules in `EPOCH_02_OBSERVER_NONCONFORMANCE_RULES_V1.md`.

#### `quorum_size`

Size of the quorum after exclusion.

#### `valid_observer_count`

Number of conforming observers.

#### `timestamp`

Operator-provided timestamp.

The timestamp is not used for replay determinism.

No additional fields are permitted.
No optional fields are permitted.
No nulls are permitted.

---

## 3. Attestation Hash Construction

The `attestation_hash` is computed as:

```text
attestation_hash = sha256(canonical_payload_bytes_without_attestation_hash)
```

Replay MUST recompute this hash and verify equality.

If mismatch:

```text
ATTESTATION_HASH_MISMATCH -> HALT
```

---

## 4. Operator Signing Rules

Operators MUST:

1. Sign the `attestation_hash`.
2. Publish the signature and payload together.
3. Never sign non-canonical payloads.
4. Never sign payloads containing excluded observers as valid observers.
5. Never sign payloads with tainted evidence.
6. Never sign payloads with `NOT_A_VERDICT` unless schema failure occurred.

Operators MAY NOT:

- add metadata
- add annotations
- add comments
- add fields
- reorder fields
- normalize payloads
- compress payloads

Operators are not allowed to interpret.
Operators are not allowed to override replay.

---

## 5. Replay Obligations

Replay MUST:

1. Recompute `evidence_root`.
2. Recompute exclusion.
3. Recompute quorum.
4. Recompute verdict.
5. Recompute canonical payload bytes.
6. Recompute `attestation_hash`.
7. Verify operator signature.
8. Reject any mismatch.

Replay is the final authority.

---

## 6. Forbidden Semantic Classes

The attestation payload may NOT contain:

- trust scores
- confidence metrics
- advisory verdicts
- probabilistic fields
- nested receipts
- observer metadata
- operator metadata
- environment fingerprints
- execution traces
- implementation details

These are permanently outside the constitutional ontology.

---

## 7. Closure Property

This file defines the complete attestation payload schema for Epoch 02.

No additional fields, semantics, or structures may be introduced at runtime.

Any unclassified payload behavior defaults to:

```text
ATTESTATION_INVALID -> REPLAY_REJECTION
```

Fail closed, never open.
