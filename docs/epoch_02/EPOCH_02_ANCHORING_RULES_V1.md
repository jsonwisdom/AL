# EPOCH 02 — Anchoring Rules v1

## Purpose

Define the constitutional rules governing anchoring of attestations in Epoch 02.

Anchoring is not a source of legitimacy.
Anchoring is a publication mechanism for a state that is already legitimate because replay has validated it.

Anchoring records finality.
Anchoring does not produce finality.

---

## 1. Anchoring Definition

Anchoring is the act of publishing a final, replay-validated attestation to an external commitment surface, including blockchain, content-addressed storage, or another immutable medium.

Anchoring MUST satisfy:

```text
ANCHORING = PUBLIC_COMMITMENT_TO_FINALITY
```

Anchoring is subordinate to replay.
Anchoring cannot override replay.
Anchoring cannot create legitimacy.

---

## 2. Anchor Eligibility Predicate

An attestation is eligible for anchoring only if all of the following predicates are TRUE:

### 2.1 Finality Predicate

```text
attestation.finality == TRUE
```

### 2.2 Attestation Hash Predicate

```text
attestation_hash == REPLAY_RECOMPUTED_HASH
```

### 2.3 Signature Predicate

```text
signature_valid == TRUE
```

### 2.4 Authorization Predicate

```text
signer_authorized == TRUE
```

### 2.5 Evidence Predicate

```text
evidence_root == REPLAY_RECOMPUTED_ROOT
```

### 2.6 Operator Set Predicate

```text
operator_set_hash == REPLAY_RECOMPUTED_OPERATOR_SET_HASH
```

### 2.7 Epoch Predicate

```text
attestation.epoch == CURRENT_DECLARED_EPOCH
```

### 2.8 Surface Predicate

```text
verdict_surface in ALLOWED_SURFACE_ENUM
```

### 2.9 Taint Predicate

```text
taint_rules_satisfied == TRUE
```

If any predicate fails:

```text
ANCHOR_ELIGIBLE = FALSE
```

A non-final attestation may not be anchored.

If anchored anyway, the anchor is constitutionally void.

---

## 3. Anchor Payload Schema

The anchor payload MUST contain exactly:

```json
{
  "attestation_hash": "<sha256>",
  "evidence_root": "<sha256>",
  "kernel_hash": "<sha256>",
  "schema_hash": "<sha256>",
  "operator_set_hash": "<sha256>",
  "epoch": "<uint32>",
  "surface_version": "<uint32>",
  "anchor_hash": "<sha256>"
}
```

### 3.1 `anchor_hash`

Self-referential integrity anchor:

```text
anchor_hash = sha256(canonical_anchor_payload_bytes_without_anchor_hash)
```

Canonicalization MUST use JCS / RFC 8785.

No additional fields are permitted.
No nulls are permitted.
No nested structures are permitted.

---

## 4. Anchor Hash Construction

Replay MUST recompute:

```text
anchor_hash_recomputed == anchor_hash_declared
```

If mismatch:

```text
ANCHOR_INVALID -> REPLAY_REJECTION
```

---

## 5. Permitted Anchor Targets

Anchors may be published to:

- blockchain transactions
- content-addressed storage, including IPFS or Arweave
- append-only logs
- immutable distributed ledgers

Anchors may not be published to:

- mutable storage
- operator-controlled databases
- systems without immutability guarantees
- systems without public verifiability

Anchoring MUST NOT introduce new semantics.

---

## 6. Replay Validation of Anchors

Replay MUST validate:

1. canonical anchor payload
2. `anchor_hash` correctness
3. `attestation_hash` correctness
4. `evidence_root` correctness
5. `kernel_hash` correctness
6. `schema_hash` correctness
7. `operator_set_hash` correctness
8. epoch correctness
9. `surface_version` correctness
10. finality correctness

If any mismatch:

```text
ANCHOR_INVALID -> REPLAY_REJECTION
```

Replay is the final authority.

---

## 7. Epoch Binding

Anchors are epoch-scoped:

```text
anchor.epoch == attestation.epoch
```

Anchors cannot:

- reference future epochs
- reference past epochs
- be reused across epochs

Replay MUST enforce epoch binding.

---

## 8. Taint-After-Anchor Behavior

Anchoring does not immunize an attestation from taint discovered later.

If taint is discovered after anchoring:

1. replay recomputes taint
2. replay recomputes exclusion
3. replay recomputes quorum
4. replay recomputes finality

If finality collapses:

```text
ANCHOR_RETROACTIVELY_INVALID
```

Anchors are not authoritative.
Replay is authoritative.

---

## 9. Invalid Anchor Classifications

Replay MUST classify invalid anchors as one of:

### 9.1 ANCHOR_NON_FINAL

Attestation was not final.

### 9.2 ANCHOR_HASH_MISMATCH

`anchor_hash` mismatch.

### 9.3 ANCHOR_ATTESTATION_HASH_MISMATCH

`attestation_hash` mismatch.

### 9.4 ANCHOR_EVIDENCE_MISMATCH

`evidence_root` mismatch.

### 9.5 ANCHOR_OPERATOR_SET_MISMATCH

`operator_set_hash` mismatch.

### 9.6 ANCHOR_EPOCH_MISMATCH

Epoch mismatch.

### 9.7 ANCHOR_SURFACE_VIOLATION

`surface_version` mismatch.

### 9.8 ANCHOR_TAINT_VIOLATION

Taint rules violated.

### 9.9 ANCHOR_REPLAY_DIVERGENCE

Replay cannot reconstruct anchor payload.

All invalid anchors are constitutionally void.

---

## 10. Closure Property

This file defines the complete anchoring rules for Epoch 02.

No additional:

- anchor fields
- anchor semantics
- anchor targets
- anchor override mechanisms
- social anchoring processes

may be introduced at runtime.

Any unclassified anchoring behavior defaults to:

```text
ANCHOR_INVALID
```

Fail closed, never open.
