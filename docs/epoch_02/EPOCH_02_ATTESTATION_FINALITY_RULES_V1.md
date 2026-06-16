# EPOCH 02 — Attestation Finality Rules v1

## Purpose

Define the constitutional rules governing when an attestation becomes final in Epoch 02.

Finality is not a claim about truth. Finality is the state in which:

- replay can reconstruct every committed field
- all constitutional predicates are satisfied
- no discretionary interpretation is required
- no observer, operator, or kernel can mutate the outcome

Finality is a mechanical conjunction, not a social judgment.

---

## 1. Finality Definition

An attestation is final if and only if:

```text
REPLAY(attestation_payload) == EXACT_MATCH
```

Where `EXACT_MATCH` means replay can reconstruct every committed field of the attestation payload and signature envelope byte-for-byte, using only:

- canonical evidence
- canonical schema
- canonical kernel
- canonical operator set
- canonical surface enum
- canonical replay rules

If any field cannot be reconstructed deterministically:

```text
FINALITY = FALSE
```

Finality is binary.
There is no partial finality.

---

## 2. Finality Is Not Truth

Explicit constitutional invariant:

```text
FINALITY != TRUTH
FINALITY = REPLAY_COMPLETE_DETERMINISM
```

A final attestation is:

- reproducible
- canonical
- hash-stable
- operator-signed
- replay-validated

But it is not a metaphysical claim about correctness.
It is a claim about closure.

---

## 3. Finality Predicates

Finality requires the conjunction of all predicates below.

Replay MUST verify:

### 3.1 Schema Predicate

```text
schema_check(input_bytes) == VALID
```

### 3.2 Evidence Predicate

```text
evidence_root_recomputed == evidence_root_declared
```

### 3.3 Kernel Predicate

```text
kernel_hash_recomputed == kernel_hash_declared
```

### 3.4 Operator Set Predicate

```text
operator_set_hash_recomputed == operator_set_hash_declared
```

### 3.5 Signature Predicate

```text
signature_valid == TRUE
```

### 3.6 Authorization Predicate

```text
signer in operator_keys(epoch)
```

### 3.7 Quorum Predicate

```text
quorum_after_exclusion >= MINIMUM_VALID_OBSERVERS
```

### 3.8 Verdict Surface Predicate

```text
verdict in ALLOWED_VERDICT_ATOMS
```

### 3.9 Taint Predicate

```text
taint_rules_satisfied == TRUE
```

### 3.10 Replay Predicate

```text
replay_reconstructs_all_fields == TRUE
```

Finality is the logical AND of all predicates.

If any predicate fails:

```text
FINALITY = FALSE
```

---

## 4. Finality Construction

Replay MUST reconstruct:

- `evidence_root`
- exclusion set
- quorum size
- valid observer count
- verdict
- canonical attestation payload
- `attestation_hash`
- signature validity
- operator authorization

Replay MUST then compare:

```text
reconstructed_payload_bytes == declared_payload_bytes
```

If mismatch:

```text
FINALITY = FALSE
```

If match:

```text
FINALITY = TRUE
```

---

## 5. Finality Failure Modes

Replay MUST classify finality failure as one of:

### 5.1 FINALITY_SCHEMA_MISMATCH

Schema check cannot be reproduced.

### 5.2 FINALITY_EVIDENCE_MISMATCH

Evidence root cannot be reproduced.

### 5.3 FINALITY_KERNEL_MISMATCH

Kernel hash mismatch.

### 5.4 FINALITY_OPERATOR_SET_MISMATCH

Operator set hash mismatch.

### 5.5 FINALITY_SIGNATURE_INVALID

Signature cryptographically invalid.

### 5.6 FINALITY_UNAUTHORIZED_SIGNER

Signer not in operator set.

### 5.7 FINALITY_QUORUM_COLLAPSE

Valid observers are fewer than `MINIMUM_VALID_OBSERVERS`.

### 5.8 FINALITY_SURFACE_VIOLATION

Verdict or payload surface invalid.

### 5.9 FINALITY_TAINT_VIOLATION

Taint propagation rules violated.

### 5.10 FINALITY_REPLAY_DIVERGENCE

Replay cannot reconstruct committed fields.

All failure modes are fatal for finality.

---

## 6. Finality Immutability

Once an attestation is final:

- it cannot be revoked
- it cannot be amended
- it cannot be reinterpreted
- it cannot be socially overridden

Finality is epoch-sealed.

---

## 7. Finality and Anchoring

Anchoring, including on-chain publication, does not create finality.

Anchoring is only valid if:

```text
attestation.finality == TRUE
```

Anchoring a non-final attestation is constitutionally void.

---

## 8. Finality and Taint

If any observer contributing to the attestation becomes tainted:

- taint propagates
- quorum is recomputed
- evidence is recomputed
- replay must re-evaluate finality

If taint invalidates any predicate:

```text
FINALITY = FALSE
```

Finality is not permanent if taint is discovered later.

---

## 9. Closure Property

This file defines the complete finality rules for Epoch 02.

No additional:

- predicates
- interpretations
- override mechanisms
- social processes
- governance votes

may be introduced at runtime.

Any unclassified behavior defaults to:

```text
FINALITY = FALSE
```

Fail closed, never open.
