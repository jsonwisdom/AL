# CVD_OUTPUT_SCHEMA_V1 — ALMS Public Drift Opinion Schema

## Status

`CVD_OUTPUT_SCHEMA_V1_OPENED`

---

## Purpose

Define the public output artifact for ALMS Core Variant Detector findings.

A CVD output is the machine-readable and human-readable civic drift opinion emitted by a verifier after replay.

It converts verifier results into a stable public accountability artifact that can be rendered, indexed, searched, cited, and independently audited.

The CVD output does not decide political legitimacy, legal authority, institutional intent, or narrative meaning.

It records replay divergence and classifies it under deterministic ALMS variant classes.

---

## Core Rule

```text
one verifier run
-> one replay trace
-> one CVD output
-> one public opinion artifact
```

No private verdicts.

No unbounded narrative fields.

No hidden evidence.

No drift claim without replay trace.

---

## Relationship to Other Specs

`CVD_OUTPUT_SCHEMA_V1` consumes outputs from:

- `REPLAY_SPEC_V1`
- `FIXTURE_SPEC_V1`
- `VERIFIER_SPEC_V1`

It produces:

- public verifier reports
- registry entries
- UI-renderable drift opinions
- voice/search-indexable civic memory records

---

## Required Invariants

1. One report MUST correspond to one verifier run.
2. Report JSON MUST be deterministic and canonically serializable.
3. Report fields MUST be bounded.
4. Report MUST include verifier version and spec references.
5. Report MUST include fixture ID when a fixture is used.
6. Report MUST include canonical vs observed comparison when available.
7. Report MUST distinguish detection from interpretation.
8. Report MUST preserve replay trace references.
9. Report MUST be hashable as a standalone civic memory artifact.

---

## Top-Level Schema

A CVD output SHOULD be represented as JSON:

```json
{
  "schema": "CVD_OUTPUT_SCHEMA_V1",
  "schema_version": "1.0.0",
  "report_id": "cvd:<run_id>:sha256:<digest>",
  "run": {
    "run_id": "string",
    "run_at": "ISO-8601 timestamp",
    "verifier_spec": "VERIFIER_SPEC_V1",
    "verifier_name": "string",
    "verifier_version": "string",
    "environment_ref": "string|null"
  },
  "subject": {
    "fixture_id": "string|null",
    "artifact_id": "string|null",
    "jurisdiction": "string|null",
    "domain": "string|null",
    "source_uri": "string|null",
    "source_type": "string|null"
  },
  "specs": {
    "replay_spec": "REPLAY_SPEC_V1",
    "fixture_spec": "FIXTURE_SPEC_V1|null",
    "transform_policy_id": "string|null",
    "transform_policy_hash": "sha256:<hex>|null"
  },
  "verdict": {
    "state": "PASS|FAIL|INDETERMINATE|TAINTED|REVIEW_REQUIRED|HIGH_RISK_VARIANT",
    "cvd_class": "NONE|V1_BYTE_VARIANT|V2_TRANSFORM_VARIANT|V3_PROVENANCE_VARIANT|V4_IDENTITY_VARIANT|V5_SEMANTIC_VARIANT",
    "confidence": "DECLARED|COMPUTED|PARTIAL|UNDETERMINED",
    "summary": "bounded string"
  },
  "comparison": {
    "expected_digest": "sha256:<hex>|keccak256:<hex>|null",
    "computed_digest": "sha256:<hex>|keccak256:<hex>|null",
    "expected_manifest_root": "sha256:<hex>|keccak256:<hex>|null",
    "computed_manifest_root": "sha256:<hex>|keccak256:<hex>|null",
    "match": true
  },
  "evidence_graph": {
    "nodes": [],
    "edges": []
  },
  "replay_trace": [],
  "diff": {
    "available": false,
    "type": "none|byte|text|json|table|semantic|other",
    "uri": "string|null",
    "summary": "bounded string|null"
  },
  "provenance_chain": [],
  "witnesses": [],
  "errors": [],
  "human_readable": {
    "title": "string",
    "finding": "bounded string",
    "operator_note": "bounded string|null"
  },
  "hash": {
    "canonicalization": "jq -cS or declared canonical method",
    "digest": "sha256:<hex>|null"
  }
}
```

---

## Verdict Field Rules

The `verdict.state` field MUST be one of:

- `PASS`
- `FAIL`
- `INDETERMINATE`
- `TAINTED`
- `REVIEW_REQUIRED`
- `HIGH_RISK_VARIANT`

The `verdict.cvd_class` field MUST be one of:

- `NONE`
- `V1_BYTE_VARIANT`
- `V2_TRANSFORM_VARIANT`
- `V3_PROVENANCE_VARIANT`
- `V4_IDENTITY_VARIANT`
- `V5_SEMANTIC_VARIANT`

A `PASS` verdict SHOULD use:

```json
{
  "cvd_class": "NONE"
}
```

---

## Evidence Graph

The evidence graph records the replay relationship between objects.

Recommended node types:

- `source_artifact`
- `transform_policy`
- `canonical_bytes`
- `digest`
- `receipt`
- `manifest`
- `witness`
- `fixture`
- `verifier_run`
- `cvd_report`

Recommended edge types:

- `retrieved_from`
- `canonicalized_by`
- `hashes_to`
- `bound_by_receipt`
- `included_in_manifest`
- `witnessed_by`
- `verified_by`
- `classified_as`

Graph order MUST be deterministic.

---

## Replay Trace

The replay trace records ordered verifier steps.

Each step SHOULD include:

```json
{
  "step": 1,
  "name": "schema_validation",
  "status": "PASS|FAIL|SKIPPED|INDETERMINATE",
  "input_ref": "string|null",
  "output_ref": "string|null",
  "message": "bounded string|null"
}
```

Trace steps MUST be ordered by execution sequence.

A report without a replay trace is not a public CVD opinion.

---

## Diff Rules

A diff MAY be embedded only when bounded and safe.

Large diffs SHOULD be referenced by URI and digest.

Diffs MUST distinguish:

- byte difference,
- text difference,
- JSON structural difference,
- table/numeric difference,
- semantic/policy-level difference.

Semantic diff output MUST be treated as detection support, not final interpretation.

---

## Provenance Chain

The provenance chain SHOULD list source-to-report custody:

```json
{
  "type": "source|retrieval|transform|receipt|manifest|witness|report",
  "ref": "string",
  "digest": "sha256:<hex>|null",
  "timestamp": "ISO-8601 timestamp|null",
  "actor": "string|null"
}
```

Missing provenance MUST downgrade the verdict to `INDETERMINATE`, `TAINTED`, or `FAIL` depending on observed contradiction.

---

## Rendering Rules

A CVD output MAY render to:

- JSON
- Markdown
- HTML
- public verifier UI
- voice/search summaries
- registry index rows

All renderings MUST preserve:

- report ID,
- fixture ID when present,
- verdict state,
- CVD class,
- verifier version,
- canonical digest comparison,
- replay trace reference.

A rendered view MUST NOT omit a non-PASS verdict.

---

## Canonicalization and Hashing

A CVD report SHOULD be hashable as its own civic memory artifact.

Recommended canonicalization:

```text
jq -cS
```

The report hash MUST exclude its own `hash.digest` field or set that field to `null` before hashing.

Self-referential report hashing is forbidden.

---

## Versioning

This schema follows semantic versioning.

`CVD_OUTPUT_SCHEMA_V1` is tied to:

- `REPLAY_SPEC_V1`
- `FIXTURE_SPEC_V1`
- `VERIFIER_SPEC_V1`

Breaking changes MUST create a new schema version.

Prior reports MUST remain replayable under the schema version they declare.

---

## Failure Conditions

A CVD output is invalid if:

- schema version is missing,
- verifier run ID is missing,
- verdict state is missing,
- CVD class is missing,
- replay trace is missing,
- digest comparison is omitted when applicable,
- report hash is self-referential,
- unbounded narrative replaces evidence fields,
- private evidence is required to verify a public claim.

---

## Minnesota #001 Use

Minnesota fixture reports SHOULD use this schema for the first civic replay case law layer.

The target report form:

```text
MN public record fixture
-> verifier run
-> CVD output
-> public opinion artifact
-> registry/search/UI entry
```

The Minnesota success condition is not publication alone.

The success condition is a reproducible public drift opinion generated from replayable civic evidence.

---

## Final Rule

A verifier verdict becomes civic memory only when it is published as a deterministic CVD output.

Private conclusions do not create public proof.

No trace, no opinion.

Verify > narrative.
