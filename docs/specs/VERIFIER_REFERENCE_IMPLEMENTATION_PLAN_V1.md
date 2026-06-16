# VERIFIER_REFERENCE_IMPLEMENTATION_PLAN_V1 — ALMS Reference Court Build Plan

## Status

`VERIFIER_REFERENCE_IMPLEMENTATION_PLAN_V1_OPENED`

---

## Purpose

Define the first implementation plan for turning `VERIFIER_SPEC_V1` into an executable ALMS replay court.

This plan does not claim an implementation already exists.

It defines the build target, module boundaries, determinism constraints, output contract, and CI gates required for a reference verifier.

---

## Goal

Build a reproducible verifier that accepts ALMS fixture/replay packets and emits deterministic `CVD_OUTPUT_SCHEMA_V1` reports.

The verifier answers one question:

```text
Does the declared evidence recompute to the declared verification state under declared rules?
```

---

## Required Modules

### 1. Schema Validator

Validates:

- `REPLAY_SPEC_V1` packet shape
- `FIXTURE_SPEC_V1` fixture objects
- `CVD_OUTPUT_SCHEMA_V1` report shape
- required field presence
- bounded field constraints
- declared spec versions

Failure mode:
`INDETERMINATE` or invalid input exit code when no replay can begin.

---

### 2. Source Loader

Loads declared source artifacts from local paths or pre-fetched content-addressed inputs.

Reference verifier rule:

```text
No network calls during replay.
```

Network retrieval may happen during fixture creation, not verifier adjudication.

---

### 3. Transform Policy Loader

Loads declared transform policy and verifies:

- policy ID
- policy hash
- toolchain declaration
- source type compatibility
- canonicalization method

No implicit transform is admissible.

---

### 4. Canonicalizer Engine

Transforms source artifacts into canonical bytes under declared policy.

Required properties:

- deterministic
- idempotent
- versioned
- source-type aware
- explicit about encoding and newline behavior

Initial target methods:

- JSON: sorted compact canonical JSON
- CSV: declared encoding/newline/order policy
- text/Markdown: declared UTF-8 normalization policy
- PDF: declared extraction policy only after parser/toolchain lock

---

### 5. Digest Engine

Computes declared digest over canonical bytes.

Supported initial digest:

```text
sha256
```

Optional future digest:

```text
keccak256
```

Digest mismatch defaults to:

```text
CVD: V1_BYTE_VARIANT
Verdict: FAIL
```

unless transform instability or unavailable evidence requires `TAINTED` or `INDETERMINATE`.

---

### 6. Receipt Recompute Engine

Verifies receipt fields bind to:

- fixture ID
- source identity
- transform policy ID
- canonical digest
- operator identity
- commit or publication path when declared
- optional witness references

A receipt that binds only to narrative summary text is invalid unless the summary itself is the declared fixture.

---

### 7. Manifest Validator

Validates aggregate proof state:

- leaf list
- digest method
- leaf ordering
- aggregation rule
- domain separation
- claimed root
- recomputed root

Single-leaf rule:

```text
manifest_root = leaf_digest
```

A manifest without an aggregation rule is not replay-admissible.

---

### 8. Verdict Engine

Maps module results to ALMS verdicts:

- `PASS`
- `FAIL`
- `INDETERMINATE`
- `TAINTED`
- `REVIEW_REQUIRED`
- `HIGH_RISK_VARIANT`

The verdict engine MUST fail closed.

Failing closed does not always mean `FAIL`.

If contradiction is not directly observable, default to `INDETERMINATE`.

---

### 9. CVD Classifier

Maps drift to CVD classes:

- `V1_BYTE_VARIANT`
- `V2_TRANSFORM_VARIANT`
- `V3_PROVENANCE_VARIANT`
- `V4_IDENTITY_VARIANT`
- `V5_SEMANTIC_VARIANT`

The classifier detects divergence.

It does not interpret political, legal, or institutional meaning.

---

### 10. CVD Output Generator

Emits strict `CVD_OUTPUT_SCHEMA_V1` JSON containing:

- report ID
- run ID
- verifier version
- fixture ID
- digest comparison
- verdict
- CVD class
- replay trace
- evidence graph
- errors
- witnesses checked
- canonical report hash

No trace, no opinion.

---

## Interfaces

### CLI

Reference CLI target:

```text
alms verify <fixture.json>
alms verify <replay-packet.json>
alms verify --source <artifact> --policy <policy.json> --receipt <receipt.json>
```

### Library API

Reference library target:

```text
validate_schema(packet)
load_source(packet)
load_transform_policy(packet)
canonicalize(source, policy)
compute_digest(canonical_bytes)
verify_receipt(packet, digest)
verify_manifest(packet)
classify_variant(results)
emit_cvd_output(results)
```

### Browser/Public Verifier

A browser verifier MAY be supported after CLI determinism is proven.

Browser builds MUST preserve the same canonicalization and digest behavior as CLI verifier.

---

## Determinism Constraints

The reference implementation MUST declare:

- runtime version
- dependency versions
- parser/toolchain versions
- locale assumptions
- timezone assumptions
- encoding assumptions
- newline behavior
- JSON ordering behavior

Reference replay SHOULD avoid network access.

All replay inputs SHOULD be local or content-addressed before verifier execution.

---

## Output Contract

Every completed run MUST emit one `CVD_OUTPUT_SCHEMA_V1` report.

Every report MUST include a replay trace.

Every report SHOULD be canonicalized and hashed with self-hash exclusion:

```text
set hash.digest = null
canonicalize report
sha256 canonical_report
write hash.digest
```

Self-referential hashing is forbidden.

---

## Test Vector Classes

The reference suite SHOULD include:

1. `PASS_VALID_FIXTURE`
2. `FAIL_BYTE_VARIANT`
3. `TAINTED_TRANSFORM_VARIANT`
4. `FAIL_PROVENANCE_VARIANT`
5. `REVIEW_REQUIRED_IDENTITY_VARIANT`
6. `HIGH_RISK_SEMANTIC_VARIANT`
7. `INDETERMINATE_MISSING_SOURCE`
8. `INDETERMINATE_UNDECLARED_POLICY`
9. `INVALID_SCHEMA`
10. `SELF_HASH_REJECTION`

---

## CI Gates

CI SHOULD fail if:

- schema validation breaks,
- canonicalization drifts,
- report hashes are self-referential,
- replay trace is missing,
- verifier output is nondeterministic,
- expected test verdict changes without fixture version change,
- network calls are required during replay,
- PASS is emitted without digest recomputation.

---

## Initial Directory Target

```text
scripts/alms_verify.py
schemas/cvd_output_schema_v1.json
schemas/fixture_spec_v1.json
schemas/replay_packet_v1.json
tests/fixtures/pass_valid_fixture/
tests/fixtures/fail_byte_variant/
tests/fixtures/tainted_transform_variant/
tests/fixtures/fail_provenance_variant/
tests/fixtures/review_required_identity_variant/
tests/fixtures/high_risk_semantic_variant/
tests/fixtures/indeterminate_missing_source/
tests/fixtures/invalid_schema/
```

---

## Final Rule

The reference verifier is not trusted because it exists.

It is trusted only when independent operators can reproduce its verdict from declared inputs.

No reproducible trace, no public proof.

Verify > narrative.
