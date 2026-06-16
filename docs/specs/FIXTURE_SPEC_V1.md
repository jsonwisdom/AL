# FIXTURE_SPEC_V1 — ALMS Civic Fixture Substrate

## Status

`FIXTURE_SPEC_V1_OPENED`

---

## Purpose

Define the minimal unit of civic memory that can be independently replayed under ALMS.

A fixture is a structured evidence object that binds a public source, provenance declaration, transform policy, canonical bytes, receipt, and replay conditions into one admissible civic verification unit.

This specification is source-format neutral.

A fixture may originate from CSV, JSON, Markdown, PDF, image, media, webpage, official portal export, or other declared public artifact.

---

## Core Rule

```text
No provenance declaration, no fixture.
No canonical bytes, no receipt.
No receipt, no replay.
No replay, no civic memory.
```

A fixture is not merely a file.

A fixture is a replay-admissible evidence unit.

---

## Core Invariants

1. A fixture is the minimal unit of civic memory that can be independently replayed.
2. Fixture identity is content-addressed, not location-addressed.
3. Fixture provenance MUST be declared before replay.
4. Fixture canonicalization MUST reference a deterministic transform policy.
5. Fixture receipts MUST bind to canonical bytes, not summaries.
6. Fixture drift MUST classify through ALMS Core Variant Detector classes.
7. Witness layers MAY publish, timestamp, or route fixtures, but MUST NOT replace replay.

---

## Fixture Qualification

A civic artifact qualifies as a fixture only if it declares:

- source identity,
- source retrieval method,
- retrieval timestamp,
- source type,
- transform policy,
- canonicalization method,
- digest method,
- expected canonical digest,
- receipt location or embedded receipt,
- replay conditions.

Derived summaries, commentary, screenshots without source declaration, platform posts, or narrative claims are not fixtures by themselves.

They MAY become derived artifacts linked to fixtures.

---

## Fixture Identity and Versioning

A fixture ID SHOULD be derived from stable semantic scope plus canonical digest.

Recommended form:

```text
fixture:<jurisdiction>:<domain>:<source_slug>:<date_or_version>:sha256:<digest>
```

Example:

```text
fixture:mn:budget:mmb-forecast:2026-02:sha256:<digest>
```

Fixture identity is content-addressed.

If canonical bytes change, the fixture version changes.

Location changes do not change fixture identity unless source identity or canonical bytes change.

---

## Fixture Object

A fixture SHOULD be represented as JSON:

```json
{
  "fixture_spec": "FIXTURE_SPEC_V1",
  "fixture_id": "fixture:mn:budget:mmb-forecast:2026-02:sha256:<digest>",
  "jurisdiction": "mn",
  "domain": "budget",
  "source": {
    "title": "string",
    "uri": "string",
    "publisher": "string",
    "retrieved_at": "ISO-8601 timestamp",
    "retrieval_method": "manual | scripted | api | archive | other",
    "source_type": "csv | json | markdown | pdf | image | media | webpage | other"
  },
  "transform": {
    "policy_id": "string",
    "policy_hash": "sha256:<hex>",
    "canonicalization_method": "string",
    "toolchain": ["string"],
    "notes": "string|null"
  },
  "canonical": {
    "digest_method": "sha256",
    "digest": "sha256:<hex>",
    "byte_length": 0,
    "uri": "string|null"
  },
  "receipt": {
    "receipt_spec": "ALMS_RECEIPT_V1",
    "uri": "string|null",
    "digest": "sha256:<hex>|null"
  },
  "replay": {
    "replay_spec": "REPLAY_SPEC_V1",
    "required_inputs": ["source", "transform_policy", "canonical_digest", "receipt"],
    "expected_verdict": "PASS"
  },
  "witness": {
    "required_for_verification": false,
    "items": []
  }
}
```

---

## Provenance Requirements

A fixture provenance declaration MUST include:

- source URI or archive URI,
- publisher or originating body,
- retrieval timestamp,
- retrieval method,
- operator identity or attestor,
- source type,
- any source access constraints,
- any known source volatility.

A fixture with missing provenance is not replay-admissible.

---

## Canonicalization Rules

Fixture canonicalization MUST be deterministic, versioned, and reproducible.

For JSON and CSV fixtures, policies MUST declare ordering, encoding, newline handling, quoting behavior, and whitespace normalization.

For PDF fixtures, policies MUST declare parser, parser version when available, layout mode, page boundary handling, encoding behavior, footnote policy, table extraction assumptions, and any stitching rules.

For image or media fixtures, policies MUST declare whether the canonical bytes are raw file bytes, normalized metadata-stripped bytes, frame extracts, transcript extracts, or derived hashes.

No implicit transform is admissible.

---

## Receipt Emission

A fixture receipt MUST bind:

- fixture ID,
- source identity,
- transform policy ID,
- canonical digest,
- operator identity,
- repository path or publication path,
- creation timestamp,
- optional witness references.

A receipt MUST NOT bind only to narrative summary text unless the summary itself is the declared fixture.

---

## Replay Conditions

A fixture is replayable when an independent operator can obtain or reconstruct:

1. declared source artifact,
2. declared transform policy,
3. declared canonicalization toolchain,
4. declared digest method,
5. declared receipt,
6. declared manifest or fixture index if applicable.

If any of these are missing, replay MUST return `INDETERMINATE` unless contradiction is directly observable.

---

## Drift Classification

Fixture-level divergence maps to ALMS Core Variant Detector classes:

| CVD Class | Fixture Drift Meaning | Default Verdict |
|---|---|---|
| V1 — BYTE_VARIANT | canonical bytes differ | FAIL |
| V2 — TRANSFORM_VARIANT | transform policy or toolchain differs | TAINTED or INDETERMINATE |
| V3 — PROVENANCE_VARIANT | source lineage, receipt ancestry, or manifest continuity breaks | FAIL |
| V4 — IDENTITY_VARIANT | identity, signer, ENS, attestor, or witness relationship changes while bytes remain stable | REVIEW_REQUIRED |
| V5 — SEMANTIC_VARIANT | meaning, legal effect, policy posture, numeric claim, or operational instruction materially diverges | HIGH_RISK_VARIANT |

---

## Admissibility Failures

A fixture is not replay-admissible if:

- source identity is missing,
- provenance is undeclared,
- transform policy is missing,
- canonical bytes cannot be reproduced,
- digest method is undeclared,
- receipt lineage is broken,
- manifest rule is missing for aggregate fixtures,
- witness is falsely treated as the truth boundary,
- narrative summary is substituted for canonical evidence.

---

## Governance Hooks

Fixture class changes MAY be reviewed under Jay's Pincer Movement governance model:

Side A:
Institutions, publishers, agencies, or official sources emit records.

Side B:
Independent operators, agents, auditors, and public verifiers replay canonical evidence.

Fixture governance MUST NOT retroactively mutate prior fixture identity.

Updates MUST create new fixture versions or new derived artifacts.

Replay stability takes priority over narrative continuity.

---

## Minnesota Fixture Rule

Minnesota is designated as the first civic replay fixture class:

```text
STATE_FIXTURE_001 = Minnesota
```

Minnesota fixtures SHOULD prioritize:

- state budgets,
- official forecasts,
- legislative records,
- statutes,
- audit reports,
- public finance documents,
- agency-published evidence objects.

The Minnesota success condition is not onchain adoption.

The success condition is reproducible civic replay from public records to canonical proofs.

---

## Final Rule

A fixture is civic memory only when it can be replayed.

A record seen once is transparency.

A record independently recomputed is verification.

Verify > narrative.
