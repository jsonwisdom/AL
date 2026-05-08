# NY-004 Lift Conditions v1

## Purpose

Define the formal admissibility contract required to lift the NY ALMS halt recorded in:

```text
_truth/receipts/NY_ALMS_HALT_001.md
```

This document does not lift the halt.
It defines the conditions under which the halt may be lifted.

---

## Bound Gap

- **Issue:** #132
- **Halt receipt:** `_truth/receipts/NY_ALMS_HALT_001.md`
- **Halt verdict:** `HALT`
- **Halt reason:** `UNVERIFIED_INPUT`
- **Scope:** `TRANSITIVE_FROM_NY_004`

---

## Jurisdictional Rule

```text
UNVERIFIABLE != FALSE
UNVERIFIABLE = OUTSIDE_JURISDICTION
```

The NY-004 claim may re-enter jurisdiction only when the missing artifact becomes committed, inspectable, hash-verifiable, and replay-admissible.

---

## Required Artifact

A concrete NY-004 artifact MUST be committed before the halt may lift.

The artifact SHOULD follow existing NY ALMS conventions under `_truth/bigquery/` unless a new path is explicitly declared.

The artifact MUST NOT exist only as a README row, methodology row, issue comment, conversation, or summary.

---

## Required Fields / Evidence

The NY-004 artifact MUST include:

1. `receipt_id` or equivalent stable identifier for NY-004.
2. `previous_receipt_hash` linking to the prior NY receipt, preferably NY-003.
3. `source_data_hash` for the GSOD 2024 source extract or content-addressed source reference.
4. `coverage_counties_observed = 6`.
5. `coverage_counties_total = 62`.
6. Exact FIPS enumeration of the 6 observed counties.
7. Station identifiers mapped to each observed county.
8. Observation counts per station or county.
9. Date range / calendar-year coverage for the GSOD 2024 observations.
10. Explicit declaration of the 56 counties without GSOD 2024 station-derived observation in this receipt.
11. Receipt hash or deterministic digest of the NY-004 artifact.

---

## Prohibited Fields / Claims

The NY-004 artifact MUST NOT contain:

- `confidence`
- `risk_score`
- `trust_score`
- imputed climate values
- interpolated climate values
- statewide climate validation
- statewide risk atlas or hazard map
- causality, health impact, disaster, or economic-loss attribution
- PRISM or ERA5 comparison unless separately committed and hash-verified
- any claim that uncovered counties have measured station-derived GSOD data

---

## Required Checks

The halt may be lifted only if all checks pass:

```text
NY-004_DIRECT_ARTIFACT_FOUND
AND NY-004_ARTIFACT_PATH_DECLARED
AND NY-004_HASH_VERIFIED
AND NY-004_PREVIOUS_RECEIPT_HASH_VERIFIED
AND NY-004_6_COUNTY_ENUMERATION_VERIFIED
AND NY-004_FIPS_MATCH_NY_001_SCAFFOLD
AND NY-004_STATION_IDS_PRESENT
AND NY-004_OBSERVATION_COUNTS_PRESENT
AND NY-004_DATE_RANGE_PRESENT
AND NY-004_56_COUNTY_ABSENCE_DECLARED
AND NY-004_NO_IMPUTATION_VERIFIED
AND NY-004_NO_INTERPOLATION_VERIFIED
AND NY-004_NO_STATEWIDE_CLAIM_VERIFIED
AND NY-004_METHODOLOGY_DOC_UPDATED_WITH_PATH_AND_HASH
```

If any check fails:

```text
HALT_REMAINS_ACTIVE
```

---

## Downstream Unblock Rule

Only after this lift contract is satisfied may the following nodes be reconsidered:

```text
NY-007B
NY-010
NY-011S
ALMS_RUN_002
```

Satisfying this contract does not automatically verify downstream nodes.
It only removes the NY-004 missing-artifact halt.

Each downstream node must still be independently replay-verified.

---

## Closure Property

This file defines the complete NY-004 halt lift contract.

No undocumented artifact, summary, issue comment, operator statement, or methodology row may lift the halt.

Any unclassified lift attempt defaults to:

```text
HALT_REMAINS_ACTIVE
```

Fail closed, never open.
