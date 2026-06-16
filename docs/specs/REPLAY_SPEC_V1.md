# REPLAY_SPEC_V1 — ALMS Deterministic Replay Contract

## Status

`REPLAY_SPEC_V1_OPENED`

---

## Purpose

Define the minimal replay contract for ALMS verification.

This specification establishes how a public artifact becomes replay-admissible through canonicalization, hashing, receipt formation, manifest binding, and independent recomputation.

The replay contract is not a political claim, platform claim, or legal ruling.

It is a machine-verifiable boundary for determining replay equivalence.

---

## Core Rule

```text
source artifact
-> transform policy
-> canonical bytes
-> cryptographic digest
-> receipt
-> manifest / Merkle binding
-> verifier recomputation
-> replay verdict
```

A claim is not replay-admissible until independent recomputation can reproduce the same verification state from the same declared evidence.

---

## Replay Inputs

A replay packet SHOULD declare:

```json
{
  "spec": "REPLAY_SPEC_V1",
  "artifact_id": "string",
  "source_uri": "string",
  "source_type": "csv | json | markdown | pdf | image | media | other",
  "transform_policy_id": "string",
  "transform_policy_hash": "sha256:<hex>",
  "canonicalization_method": "string",
  "digest_method": "sha256 | keccak256 | sha256+keccak256",
  "expected_digest": "<hex>",
  "receipt_uri": "string",
  "manifest_uri": "string|null",
  "witness_uri": "string|null"
}
```

---

## Canonicalization Requirements

A canonicalization method MUST be:

1. deterministic,
2. versioned,
3. reproducible by an independent operator,
4. byte-preserving after normalization,
5. explicit about whitespace, ordering, encoding, page boundaries, and parser assumptions.

For JSON objects, ALMS MAY use deterministic sorted compact JSON such as:

```text
jq -cS
```

For PDFs, ALMS MUST declare the extraction policy, parser, layout mode, encoding behavior, and any page-boundary rules.

---

## Digest Requirements

Digest outputs MUST bind to canonical bytes, not narrative summaries.

Accepted digest forms:

```text
sha256:<64 lowercase hex chars>
keccak256:<64 lowercase hex chars>
```

A digest mismatch produces a replay failure unless the packet is explicitly classified as transform-tainted or indeterminate.

---

## Receipt Requirements

A receipt SHOULD include:

```json
{
  "receipt_spec": "ALMS_RECEIPT_V1",
  "artifact_id": "string",
  "source_uri": "string",
  "transform_policy_id": "string",
  "canonical_digest": "sha256:<hex>",
  "created_at": "ISO-8601 timestamp",
  "operator_identity": "string",
  "repo": "jsonwisdom/AL",
  "commit": "git commit sha|null",
  "witness": {
    "type": "none | EAS | ENS | BaseTx | IPFS | other",
    "uri": "string|null",
    "required_for_verification": false
  }
}
```

Witnesses are external publication or timestamp surfaces.

They are not the truth boundary.

---

## Manifest / Merkle Binding

A manifest binds one or more receipts into a larger verification state.

For a single-leaf checkpoint:

```text
manifest_root = leaf_digest
```

For multi-leaf checkpoints, the manifest MUST declare the tree rule, leaf ordering rule, and domain separation rule.

A manifest without a declared aggregation rule is not replay-admissible.

---

## Replay Verdicts

### PASS

Observed replay state equals canonical verification state.

### FAIL

Observed replay state contradicts canonical verification state.

### INDETERMINATE

Replay cannot complete because evidence, parser behavior, source availability, or transform environment is insufficient.

### TAINTED

Replay completes only through an unstable, unauthorized, or policy-divergent transform boundary.

### REVIEW_REQUIRED

Replay surfaces identity, authority, or witness inconsistency that does not by itself invalidate canonical bytes.

### HIGH_RISK_VARIANT

Replay detects semantic or policy-level divergence requiring downstream human, institutional, or court review.

---

## Boundary Conditions

ALMS replay does not determine:

- political legitimacy,
- legal admissibility in a court,
- moral authority,
- institutional intent,
- or factual truth beyond declared evidence.

ALMS replay determines whether the declared evidence recomputes to the same verification state under the declared transform policy.

---

## Identity Rule

Identity resolves discovery.

Replay resolves truth.

ENS, Base, EAS, GitHub profiles, platform accounts, and public websites MAY route users to proof objects.

They MUST NOT replace canonical bytes, receipts, manifests, and independent recomputation.

---

## Final Rule

No replay, no proof.

No canonical bytes, no replay.

No declared transform policy, no admissibility.

Verify > narrative.
