# EPOCH 02 — Attestation Signing Rules v1

## Purpose

Define the complete, closed-world rules governing:

- signature algorithms
- signature canonicalization
- signature verification
- multi-signature behavior
- operator key rotation
- replay signature validation
- signature admissibility

This file ensures that attestation signatures are:

- deterministic
- replay-verifiable
- cryptographically sound
- operator-bounded
- surface-bounded
- immune to semantic drift

The signature is not a narrative. It is a cryptographic binding between:

- the attestation payload
- the operator's jurisdiction key
- the epoch
- the replay contract

Nothing more.

---

## 1. Canonical Signing Rule

Operators MUST sign exactly the following bytes:

```text
canonical_payload_bytes_without_attestation_hash
```

Where canonicalization is:

```text
JCS / RFC 8785
```

No alternate canonicalization is admissible.
No whitespace normalization is admissible.
No field reordering is admissible.
No compression is admissible.
No binary encoding is admissible.

This ensures:

- deterministic replay
- deterministic `attestation_hash`
- deterministic signature verification

---

## 2. Signature Algorithms

The only permitted signature algorithms in Epoch 02 are:

```text
secp256k1 ECDSA
secp256k1 Schnorr (BIP-340)
```

No RSA.
No Ed25519.
No multisig scripts.
No threshold schemes.
No hybrid signatures.

These may be introduced only in a future epoch.

---

## 3. Signature Envelope Schema

The signature envelope MUST contain exactly:

```json
{
  "attestation_hash": "<sha256>",
  "signature": "<hex>",
  "signer_address": "<hex>",
  "signature_algorithm": "secp256k1_ecdsa | secp256k1_schnorr"
}
```

### 3.1 `attestation_hash`

Must match the hash computed from the canonical payload.

### 3.2 `signature`

Raw hex encoding of the signature bytes.

### 3.3 `signer_address`

The operator's jurisdiction address.

### 3.4 `signature_algorithm`

One of the two allowed algorithms:

```text
secp256k1_ecdsa
secp256k1_schnorr
```

No additional fields are permitted.
No nulls are permitted.
No nested structures are permitted.

---

## 4. Signature Verification Rules

Replay MUST verify:

1. `attestation_hash` correctness by recomputing it from the canonical payload.
2. Signature validity using the declared algorithm.
3. `signer_address` correctness against the recovered public key or verified public key binding.
4. Operator authorization: `signer_address` must be in the epoch's authorized operator set.

If any check fails:

```text
SIGNATURE_INVALID -> REPLAY_REJECTION
```

Replay is the final authority.

---

## 5. Multi-Signature Rules

Epoch 02 permits exactly one signature per attestation.

No multisig.
No threshold signatures.
No signature arrays.
No signature aggregation.

If multiple signatures are present:

```text
MULTISIGNATURE_VIOLATION -> INVALID
```

If zero signatures are present:

```text
UNSIGNED_ATTESTATION -> INVALID
```

---

## 6. Operator Key Rotation

Key rotation is permitted only under the following conditions:

1. Rotation is declared at an epoch boundary.
2. New key is published in the epoch's operator set.
3. Old key is removed.
4. No attestation may be signed with the old key after rotation.

Replay MUST enforce:

```text
attestation.epoch == operator_key.epoch
```

If mismatch:

```text
KEY_EPOCH_MISMATCH -> INVALID
```

---

## 7. Forbidden Signing Behaviors

Operators may NOT:

- sign non-canonical payloads
- sign payloads containing excluded observers as valid observers
- sign payloads containing tainted evidence
- sign payloads with forbidden fields
- sign payloads with `NOT_A_VERDICT` unless schema failure occurred
- sign payloads with mismatched `kernel_hash` or `schema_hash`
- sign payloads from prior epochs
- sign payloads from future epochs
- sign payloads with altered ordering
- sign payloads with altered canonicalization

Any such signature is constitutionally void.

---

## 8. Replay Signature Obligations

Replay MUST:

1. Recompute canonical payload bytes.
2. Recompute `attestation_hash`.
3. Verify signature correctness.
4. Verify signer authorization.
5. Reject any mismatch.
6. Reject any non-canonical envelope.
7. Reject any forbidden fields.
8. Reject any signature drift.

Replay MUST NOT:

- infer missing fields
- normalize payloads
- repair signatures
- accept equivalent encodings
- accept alternate canonicalization

Replay is the final arbiter.

---

## 9. Closure Property

This file defines the complete attestation signing rules for Epoch 02.

No additional:

- algorithms
- envelope fields
- signature formats
- key types
- signing semantics

may be introduced at runtime.

Any unclassified signing behavior defaults to:

```text
SIGNATURE_INVALID -> REPLAY_REJECTION
```

Fail closed, never open.
