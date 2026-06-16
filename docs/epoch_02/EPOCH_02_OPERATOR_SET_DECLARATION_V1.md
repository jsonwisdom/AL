# EPOCH 02 — Operator Set Declaration v1

## Purpose

Define the canonical, closed-world, replay-verifiable rules for declaring the operator set for a given epoch.

This file closes the gap between:

- cryptographic validity: a signature verifies
- constitutional authorization: the signer is allowed to sign

A signature is only valid if its signer exists in the epoch-bound operator set.

---

## 1. Canonical Serialization

All operator set declarations MUST be serialized using JCS / RFC 8785.

No alternate serialization is admissible.

This guarantees:

- deterministic bytes
- deterministic hashing
- deterministic replay validation

---

## 2. Operator Set Schema

The operator set declaration MUST contain exactly:

```json
{
  "epoch": "<uint32>",
  "operator_keys": [
    {
      "address": "<hex>",
      "algorithm": "secp256k1_ecdsa | secp256k1_schnorr"
    }
  ],
  "operator_set_hash": "<sha256>"
}
```

### Field Semantics

#### `epoch`

Epoch number this operator set applies to.

#### `operator_keys`

Closed list of authorized operators for this epoch.

Each entry contains exactly:

- `address`: jurisdiction / signer address
- `algorithm`: one of the allowed signature algorithms in `EPOCH_02_ATTESTATION_SIGNING_RULES_V1.md`

#### `operator_set_hash`

SHA-256 of the canonical operator set bytes excluding this field.

No additional fields are permitted.
No nulls are permitted.
No nested structures are permitted beyond the array of key objects.

---

## 3. Operator Set Hash Construction

```text
operator_set_hash = sha256(canonical_operator_set_bytes_without_operator_set_hash)
```

Replay MUST recompute this and require exact equality.

If mismatch:

```text
OPERATOR_SET_HASH_MISMATCH -> HALT
```

---

## 4. Authorization Invariant

A signature is constitutionally valid only if its signer exists in the epoch-bound operator set.

Formally, for an attestation with:

- `attestation.epoch = E`
- `signature.signer_address = A`
- `signature.signature_algorithm = ALG`

The signature is authorized iff:

1. There exists an entry in `operator_keys` such that:
   - `entry.address == A`
   - `entry.algorithm == ALG`
2. The operator set's `epoch == E`.
3. The `operator_set_hash` is valid.

If any condition fails:

```text
UNAUTHORIZED_OPERATOR -> SIGNATURE_INVALID
```

---

## 5. Epoch Binding

Operator sets are epoch-scoped:

- one operator set per epoch
- no mid-epoch changes
- no retroactive edits
- no forward-dated sets

Replay MUST enforce:

```text
attestation.epoch == operator_set.epoch
```

If mismatch:

```text
KEY_EPOCH_MISMATCH -> INVALID
```

---

## 6. Key Rotation

Key rotation is only allowed between epochs:

- new epoch -> new operator set declaration
- new `operator_set_hash`
- old keys may be removed
- new keys may be added
- overlap allowed only if entries are byte-identical

No mid-epoch rotation is permitted.

---

## 7. Revocation

Revocation is epoch-bounded:

- To revoke an operator, remove its key from `operator_keys` in the next epoch's operator set.
- No mid-epoch revocation is permitted.
- Replay MUST reject any attestation signed by a key not present in the operator set for that attestation's epoch.

---

## 8. Replay Validation

Replay MUST:

1. Canonicalize the operator set using JCS / RFC 8785.
2. Recompute `operator_set_hash`.
3. Verify `operator_set_hash` matches the declared value.
4. Select the operator set whose epoch matches the attestation's epoch.
5. Verify that `signer_address` and `signature_algorithm` appear in `operator_keys`.
6. Reject any signature from undeclared or mismatched operators.

Replay MUST NOT:

- infer missing operators
- accept equivalent encodings
- accept alternate algorithms
- accept cross-epoch reuse of keys

---

## 9. Closure Property

This file defines the complete operator authority membrane for Epoch 02.

No additional:

- operator fields
- key types
- authorization semantics
- rotation mechanisms
- revocation semantics

may be introduced at runtime.

Any unclassified operator behavior defaults to:

```text
UNAUTHORIZED_OPERATOR -> SIGNATURE_INVALID
```

Fail closed, never open.
