# VERIFIER_SPEC_V1 — ALMS Executable Replay Court

## Status

`VERIFIER_SPEC_V1_OPENED`

---

## Purpose

Define the executable verification boundary for ALMS replay.

The verifier is the machine court that enforces `REPLAY_SPEC_V1`, `FIXTURE_SPEC_V1`, and ALMS Core Variant Detector classifications.

A verifier does not decide political legitimacy, legal authority, institutional intent, or narrative correctness.

A verifier decides whether declared evidence recomputes to the same verification state under declared rules.

---

## Core Rule

```text
fixture packet
-> schema validation
-> provenance validation
-> transform policy validation
-> canonical byte recomputation
-> digest comparison
-> receipt verification
-> manifest validation
-> CVD classification
-> replay verdict
-> public verifier report
```

No verifier report is valid unless the replay trace is reproducible.

---

## Inputs

A verifier MUST accept a replay packet or fixture object referencing:

- `REPLAY_SPEC_V1`
- `FIXTURE_SPEC_V1` when civic fixtures are used
- source artifact or source URI
- transform policy declaration
- expected canonical digest
- receipt or receipt URI
- manifest or manifest URI when aggregate state is claimed
- optional witness references

---

## Deterministic Environment Constraints

A verifier run MUST declare:

- verifier implementation name
- verifier implementation version
- operating environment or runtime
- canonicalization toolchain
- parser versions when available
- locale assumptions
- encoding assumptions
- timezone assumptions
- newline behavior
- JSON ordering behavior
- hash implementation

If these are undeclared and material to replay, verdict MUST be `INDETERMINATE` or `TAINTED`.

---

## Canonicalizer Interface

A canonicalizer MUST expose:

```text
canonicalize(input_artifact, transform_policy) -> canonical_bytes
```

The canonicalizer MUST be:

1. deterministic,
2. idempotent,
3. versioned,
4. source-type aware,
5. explicit about normalization behavior.

A canonicalizer MUST NOT silently infer policy.

No implicit transform is admissible.

---

## Receipt Recompute Engine

The verifier MUST recompute the canonical digest from canonical bytes.

Required behavior:

```text
computed_digest = digest(canonical_bytes)
computed_digest == expected_digest ? continue : classify_variant
```

Digest mismatch maps by default to:

```text
CVD: V1_BYTE_VARIANT
Verdict: FAIL
```

unless the mismatch is caused by transform policy divergence, missing source availability, or unstable parser behavior.

---

## Manifest Validator

For aggregate proofs, the verifier MUST validate:

- manifest schema
- leaf list
- leaf ordering rule
- digest method
- aggregation rule
- domain separation rule
- claimed root
- recomputed root

A manifest without a declared aggregation rule is not replay-admissible.

Single-leaf rule:

```text
manifest_root = leaf_digest
```

Multi-leaf rule MUST be explicitly declared.

---

## Witness Validator

Witnesses MAY include:

- GitHub commit SHA
- IPFS CID
- EAS UID
- ENS text/contenthash pointer
- Base transaction hash
- public website pointer

Witnesses route, timestamp, or publish proof objects.

Witnesses MUST NOT replace canonical bytes, receipts, manifests, or recomputation.

If a witness conflicts with canonical bytes but the bytes replay correctly, the verifier MUST return `REVIEW_REQUIRED` rather than silently fail the canonical proof.

---

## Verdict State Machine

### PASS

All required evidence is present and recomputation matches declared verification state.

### FAIL

Recomputation directly contradicts declared verification state.

### INDETERMINATE

Replay cannot complete because required evidence, parser behavior, source availability, or environment constraints are insufficient.

### TAINTED

Replay depends on unauthorized, unstable, undeclared, or policy-divergent transform behavior.

### REVIEW_REQUIRED

Identity, witness, signer, authority, or routing inconsistency exists while canonical bytes remain stable.

### HIGH_RISK_VARIANT

Semantic, legal, policy, numeric, or operational drift is detected and requires downstream review.

---

## CVD Hooks

The verifier MUST expose drift classification hooks:

| CVD Class | Trigger | Default Verdict |
|---|---|---|
| V1_BYTE_VARIANT | canonical bytes or digest differ | FAIL |
| V2_TRANSFORM_VARIANT | transform policy/toolchain differs | TAINTED or INDETERMINATE |
| V3_PROVENANCE_VARIANT | receipt/manifest/source lineage breaks | FAIL |
| V4_IDENTITY_VARIANT | signer/ENS/attestor/witness identity differs | REVIEW_REQUIRED |
| V5_SEMANTIC_VARIANT | material meaning, policy, numeric, or legal drift detected | HIGH_RISK_VARIANT |

The verifier MUST distinguish detection from interpretation.

It classifies divergence.

It does not adjudicate institutional meaning.

---

## CLI Boundary

A reference verifier SHOULD expose:

```text
alms-verify fixture.json
alms-verify replay-packet.json
alms-verify --source source.pdf --policy policy.json --receipt receipt.json
```

Expected exit codes:

| Code | Meaning |
|---|---|
| 0 | PASS |
| 1 | FAIL |
| 2 | INDETERMINATE |
| 3 | TAINTED |
| 4 | REVIEW_REQUIRED |
| 5 | HIGH_RISK_VARIANT |
| 64 | invalid verifier input |
| 70 | verifier internal error |

---

## Library Boundary

A verifier library SHOULD expose:

```text
validate_schema(packet) -> validation_result
load_source(packet) -> source_artifact
canonicalize(source_artifact, transform_policy) -> canonical_bytes
compute_digest(canonical_bytes) -> digest
verify_receipt(packet, digest) -> receipt_result
verify_manifest(packet) -> manifest_result
classify_variant(results) -> cvd_class
emit_report(results) -> verifier_report
```

---

## Public Verifier Report

Every verifier run SHOULD emit a public JSON report.

Minimum fields:

```json
{
  "verifier_spec": "VERIFIER_SPEC_V1",
  "verifier_version": "string",
  "run_id": "string",
  "run_at": "ISO-8601 timestamp",
  "input_ref": "string",
  "fixture_id": "string|null",
  "replay_spec": "REPLAY_SPEC_V1",
  "fixture_spec": "FIXTURE_SPEC_V1|null",
  "computed_digest": "sha256:<hex>|null",
  "expected_digest": "sha256:<hex>|null",
  "manifest_root": "sha256:<hex>|null",
  "cvd_class": "NONE|V1_BYTE_VARIANT|V2_TRANSFORM_VARIANT|V3_PROVENANCE_VARIANT|V4_IDENTITY_VARIANT|V5_SEMANTIC_VARIANT",
  "verdict": "PASS|FAIL|INDETERMINATE|TAINTED|REVIEW_REQUIRED|HIGH_RISK_VARIANT",
  "trace": [],
  "errors": [],
  "witnesses_checked": []
}
```

---

## Failure Taxonomy

A verifier MUST fail closed when:

- schema is invalid,
- source is missing,
- transform policy is missing,
- canonicalization method is undeclared,
- digest method is undeclared,
- receipt lineage is broken,
- manifest aggregation rule is missing,
- witness is falsely treated as proof,
- environment constraints materially affect replay.

Failing closed does not always mean `FAIL`.

If contradiction is not directly observable, verdict SHOULD be `INDETERMINATE`.

---

## Security Rules

A verifier MUST NOT:

- execute untrusted code from fixture packets,
- fetch private secrets,
- depend on hidden API keys for proof,
- treat platform account status as evidence truth,
- mutate source artifacts during replay,
- silently normalize evidence without declared policy.

---

## Final Rule

The verifier is not the author of truth.

The verifier is the court of replay equivalence.

No reproducible verifier trace, no public proof.

Verify > narrative.
