# Verifier Sealing Statute v1

## Purpose

Define what counts as a valid external verifier seal for Epoch 02 constitutional artifacts.

This statute preserves the separation between:

```text
REPO_LAW
VERIFIER_MEASUREMENT
CONSTITUTIONAL_SEAL
```

The repo may define the law.
The repo may define the measurement procedure.
The repo may not certify its own legitimacy.

---

## 1. Core Rule

```text
THE LAW IS IN THE REPO
THE SEAL IS IN THE MEASUREMENT
```

A constitutional artifact is not sealed merely because it claims a hash.
It is sealed only when a verifier computes the required hash from committed bytes under the declared procedure and records the result in an admissible seal receipt.

---

## 2. Self-Sealing Prohibition

The system MUST NOT:

- compute and declare its own constitutional authority as final
- treat author-supplied hashes as external verification
- accept a hash that was not produced under the declared procedure
- allow a receipt to certify itself without external measurement

```text
SELF_SEALING = INVALID
```

---

## 3. Valid External Verifier

A valid verifier is any independent process or operator that can:

1. fetch the committed artifacts at the declared commit or ref
2. read bytes without mutation
3. apply the declared canonical hashing procedure
4. record the computed hash
5. identify the procedure used
6. identify the artifact set measured
7. record failures without repair or interpretation

The verifier does not become authority.
The verifier reports measurement.
Replay remains authority.

---

## 4. Verifier Seal Receipt Schema

A verifier seal receipt MUST contain exactly the following fields:

```json
{
  "receipt_id": "<string>",
  "receipt_type": "VERIFIER_SEAL",
  "sealed_artifact": "<path>",
  "artifact_set": ["<path>", "..."],
  "commit": "<sha>",
  "hash_procedure": "<string>",
  "computed_hash": "sha256:<hex>",
  "verifier": "<string>",
  "verifier_role": "EXTERNAL_MEASUREMENT",
  "timestamp": "<iso8601>",
  "status": "SEALED"
}
```

No additional fields are permitted in the canonical form unless this statute is versioned.

---

## 5. Required Seal Predicates

A verifier seal is valid only if:

```text
ARTIFACT_SET_PRESENT
AND COMMIT_RESOLVES
AND BYTES_READ_WITHOUT_MUTATION
AND DECLARED_HASH_PROCEDURE_APPLIED
AND COMPUTED_HASH_RECORDED
AND STATUS == SEALED
```

If any predicate fails:

```text
SEAL_INVALID
```

---

## 6. Failure Receipt

If a verifier cannot reproduce the expected constitutional hash, it MUST emit a failure receipt rather than repair the artifact.

Failure receipt status values:

```text
SEAL_REJECTED
ARTIFACT_NOT_FOUND
HASH_PROCEDURE_MISMATCH
BYTE_DIVERGENCE
FORBIDDEN_VALUE_DETECTED
```

Failure receipts are admissible constitutional records.
They do not seal the artifact.

---

## 7. Epoch Inheritance

A verifier seal from a prior epoch may be referenced by a later epoch only as historical evidence.

It does not automatically authorize:

- new enum values
- new artifact fields
- new hash procedures
- new jurisdiction states
- new authority surfaces

Each epoch must declare whether prior seals are:

```text
HISTORICAL_ONLY
REPLAY_REQUIRED
SUPERSEDED
```

---

## 8. Closure Property

This statute defines the Epoch 02 verifier sealing surface.

No seal is valid merely because it appears in the repository.
No seal is valid merely because an operator declares it.
No seal is valid if the measurement procedure is absent or violated.

```text
MEASUREMENT_BEFORE_SEAL
REPLAY_BEFORE_AUTHORITY
FAIL_CLOSED
```

Fail closed, never open.
