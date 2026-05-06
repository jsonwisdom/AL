# MINNESOTA_FIXTURE_CORPUS_V1 — ALMS First Civic Replay Corpus

## Status

`MINNESOTA_FIXTURE_CORPUS_V1_OPENED`

---

## Purpose

Define the first public civic replay corpus for ALMS.

Minnesota is designated:

```text
STATE_FIXTURE_001 = Minnesota
```

This corpus provides the first replay-admissible public fixture set used to validate:

- `REPLAY_SPEC_V1`
- `FIXTURE_SPEC_V1`
- `VERIFIER_SPEC_V1`
- `CVD_OUTPUT_SCHEMA_V1`
- ALMS Core Variant Detector classifications

The corpus is not a political position.

It is a deterministic civic replay test surface.

---

## Corpus Objectives

1. Prove replay equivalence over real public records.
2. Prove fixture admissibility rules.
3. Prove verifier determinism.
4. Prove CVD classification behavior.
5. Establish the first public civic replay case law layer.

---

## Initial Fixture Classes

### Budget Fixtures

Target examples:

- Minnesota Management and Budget forecasts
- appropriations tables
- spending summaries
- fiscal notes
- agency budget reports

---

### Legislative Fixtures

Target examples:

- bills
- amendments
- statutes
- session laws
- committee reports
- vote records

---

### Audit Fixtures

Target examples:

- Office of the Legislative Auditor reports
- state audit reports
- procurement findings
- compliance reports

---

### Agency Fixtures

Target examples:

- agency-published PDFs
- CSV exports
- dashboards with downloadable evidence
- machine-readable datasets

---

## Corpus Rules

Every fixture MUST:

- declare provenance,
- declare transform policy,
- declare canonicalization method,
- declare digest method,
- emit a receipt,
- emit or reference a replay packet,
- produce a verifier report,
- produce a `CVD_OUTPUT_SCHEMA_V1` opinion.

No raw upload alone qualifies as a corpus fixture.

---

## Corpus Directory Layout

Recommended structure:

```text
_truth/fixtures/state/mn/
  budgets/
  legislation/
  audits/
  agencies/

_truth/replay/mn/
_truth/receipts/mn/
_truth/cvd/mn/
_truth/manifests/mn/

policies/mn/

schemas/
```

---

## Example Fixture Flow

```text
Minnesota source record
-> retrieval declaration
-> transform policy
-> canonical bytes
-> digest
-> receipt
-> replay packet
-> verifier run
-> CVD output
-> public civic memory artifact
```

---

## Required Provenance Fields

Every Minnesota fixture SHOULD declare:

- source title
- originating agency/body
- source URI
- retrieval timestamp
- retrieval method
- source type
- transform policy ID
- canonicalization toolchain
- operator identity
- repository path

---

## Canonicalization Targets

### JSON / CSV

Initial target:

```text
UTF-8
stable newline behavior
stable ordering
jq -cS where applicable
```

---

### PDF

PDF fixtures MUST declare:

- parser/toolchain
- parser version when available
- layout mode
- page-boundary policy
- encoding behavior
- table extraction assumptions
- footnote policy
- stitching rules

No implicit PDF transform is admissible.

---

## Initial Replay Targets

The first replay targets SHOULD include:

1. One clean PASS fixture
2. One transform-tainted fixture
3. One provenance-break fixture
4. One semantic drift fixture
5. One identity/witness drift fixture

This ensures all core verdict states are exercised.

---

## Corpus Test Goals

The Minnesota corpus SHOULD prove:

- deterministic replay,
- replay equivalence across independent operators,
- stable canonicalization,
- stable manifest aggregation,
- CVD variant detection,
- public report reproducibility.

---

## Public Opinion Layer

Every verifier run SHOULD emit:

```text
fixture
-> replay trace
-> CVD output
-> public opinion artifact
```

The public opinion artifact becomes machine-verifiable civic memory.

---

## Drift Monitoring

Minnesota fixtures MAY be replayed periodically to detect:

- source drift
- transform drift
- provenance breaks
- witness inconsistency
- semantic/policy changes

Detected divergence MUST emit new CVD reports.

Prior reports MUST remain replayable.

---

## Governance Rule

Minnesota fixture governance follows Jay's Pincer Movement:

Side A:
Institutions publish records.

Side B:
Independent operators replay records.

Replay equivalence is the convergence boundary.

Narrative agreement is not required.

---

## Success Condition

Minnesota succeeds as `STATE_FIXTURE_001` only when:

- independent operators replay the same fixtures,
- independent verifiers emit equivalent verdicts,
- CVD reports remain reproducible,
- provenance continuity survives over time.

Publication alone is insufficient.

Replay equivalence is required.

---

## Final Rule

Minnesota is not the first ALMS state because it is onchain.

Minnesota is the first ALMS state because its public records are stable enough to support deterministic civic replay.

Verify > narrative.
