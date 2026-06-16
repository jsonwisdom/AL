# NY ALMS HALT RECEIPT — 001

## Purpose

Formalize the constitutional halt caused by the missing concrete NY-004 receipt artifact.

This receipt binds the public gap record to a replay-chain halt condition.

---

## Canonical Gap Record

- **Issue:** #132
- **Title:** NY-004 receipt artifact missing: block ALMS_RUN_002 until 6/62 GSOD claim is verifiable
- **URL:** https://github.com/jsonwisdom/AL/issues/132

Issue #132 is the canonical public record of the NY-004 evidence gap.

---

## Halt Verdict

```text
VERDICT: HALT
REASON: UNVERIFIED_INPUT
SCOPE: TRANSITIVE_FROM_NY_004
```

The halt is structural, not narrative.

NY-004 is referenced by methodology and README, but the concrete hash-pinned, county-enumerated receipt artifact was not found in the repository at the time of inspection.

A referenced claim is not evidence until the underlying artifact is committed and hash-verifiable.

---

## Dependency Graph

```text
NY-001:  62/62  VERIFIED  <- county FIPS scaffold, hash-pinned
NY-003:  62/62  VERIFIED  <- ACS income, hash-pinned
NY-004:   6/62  HALT      <- referenced claim, direct artifact missing
NY-007B:  4/62  BLOCKED   <- depends on NY-004 station set
NY-010:   4/62  BLOCKED   <- depends on NY-004 station set
NY-011S:  4/62  BLOCKED   <- depends on NY-004 station set
ALMS_RUN_002:      BLOCKED <- depends on verified NY-004
```

All downstream nodes are blocked until NY-004 becomes replay-verifiable.

---

## Constitutional Authority

This halt is authorized by the following principles:

1. **Input-side membrane**
   - Referenced claims must resolve to committed, inspectable artifacts.
   - Missing input artifacts halt dependent replay.

2. **Replay supremacy**
   - Documentation cannot substitute for replay-verifiable evidence.
   - Methodology tables and README summaries are pointers, not receipts.

3. **Negative-space doctrine**
   - Absence must be recorded, not filled.
   - Missing receipt evidence is a halt condition, not an invitation to infer.

4. **No ghost promotion**
   - A claim may not advance from reference to verified state without a hash-pinned artifact.

---

## Required Conditions to Lift Halt

The halt may be lifted only when all conditions are satisfied:

```text
NY-004_DIRECT_ARTIFACT_FOUND
AND NY-004_HASH_VERIFIED
AND NY-004_6_COUNTY_ENUMERATION_VERIFIED
AND NY-004_STATION_IDS_VERIFIED
AND NY-004_OBSERVATION_COUNTS_VERIFIED
AND NY-004_56_COUNTY_ABSENCE_DECLARED
AND NY-004_NO_IMPUTATION_VERIFIED
AND NY-004_NO_STATEWIDE_CLAIM_VERIFIED
AND NY-004_CHAIN_LINKAGE_VERIFIED
```

---

## Required NY-004 Artifact Properties

The NY-004 artifact must include:

1. Hash-pinned GSOD 2024 source data or content-addressed source reference.
2. County enumeration: exactly which 6 counties have station data, listed by FIPS.
3. Station identifiers and observation counts per county.
4. Date range / coverage window.
5. Explicit sparsity declaration: 56 of 62 counties have no GSOD 2024 station-derived climate observation in this receipt.
6. No imputation, interpolation, or filled values for uncovered counties.
7. No statewide climate validation or risk claim.
8. Receipt hash.
9. Chain linkage to prior NY receipt, ideally `previous_receipt_hash` referencing NY-003.
10. Path consistency with existing `_truth/bigquery/` conventions if applicable.

---

## Enforcement

Until the halt is lifted:

```text
NO_ALMS_RUN_002
NO_POSITIVE_NY_DATA_BOUNDARY
NO_DOWNSTREAM_NY_CLIMATE_CLAIM_PROMOTION
NO_STATEWIDE_CLIMATE_VALIDATION_CLAIM
```

---

## Closure Statement

The membrane event is complete:

```text
DETECTION: Issue #132
FORMALIZATION: NY_ALMS_HALT_001
ENFORCEMENT: Downstream nodes blocked
```

The system refused to hallucinate.

Fail closed, never open.
