# NY-004 Constitutional Timeline v1

## Purpose

Trace the complete NY-004 membrane event from initial evidence gap detection through halt, lift contract, attempted restoration, replay refusal, and restoration rejection.

This timeline is a factual index of committed artifacts and bound issue records.
It does not restore jurisdiction.
It records the current halted state.

---

## Active Status

```text
HALT: ACTIVE
RESTORATION: REJECTED
JURISDICTION: SUSPENDED_FOR_NY_004
DOWNSTREAM: BLOCKED
CAUSE: MISSING_RESTORATION_ARTIFACT
```

---

## Timeline

### 1. Detection

**Artifact:** Issue #132

```text
NY-004 receipt artifact missing: block ALMS_RUN_002 until 6/62 GSOD claim is verifiable
```

**Record:** https://github.com/jsonwisdom/AL/issues/132

**Finding:** NY-004 was referenced in README and methodology docs, but no concrete hash-pinned, county-enumerated NY-004 receipt artifact was found in the repo inspection.

**Constitutional result:** Referenced claim remained outside jurisdiction until evidence exists.

---

### 2. Halt Formalization

**Artifact:** `_truth/receipts/NY_ALMS_HALT_001.md`

**Commit:** `a594a1d98e40f76a060413f5618a788c3a0aada6`

**Verdict:**

```text
VERDICT: HALT
REASON: UNVERIFIED_INPUT
SCOPE: TRANSITIVE_FROM_NY_004
```

**Constitutional result:** Downstream NY climate-economic nodes blocked.

---

### 3. Lift Contract

**Artifact:** `_truth/receipts/NY_004_LIFT_CONDITIONS_V1.md`

**Commit:** `314148f95ad67e992377d45266d56ca125a00a71`

**Rule:**

```text
UNVERIFIABLE != FALSE
UNVERIFIABLE = OUTSIDE_JURISDICTION
```

**Constitutional result:** Restoration conditions defined without lifting the halt.

---

### 4. Restoration Attempt

**Attempted artifact:** `NY-004_RESTORATION_RECEIPT_V1.md`

**Claimed restored data artifact:**

```text
_truth/bigquery/ny004_noaa_gsod_join.csv
```

**Claim:** NY-004 jurisdiction could be restored because the NOAA GSOD join artifact was present, hash-pinned, and replay-validated.

**Constitutional result:** Attempt required repo/replay inspection before admission.

---

### 5. Replay / Repo Inspection

**Inspection target:** `_truth/bigquery/ny004_noaa_gsod_join.csv`

**Observed result:**

```text
NOT_FOUND
```

**Constitutional result:** Restoration evidence absent. Restoration receipt inadmissible.

---

### 6. Restoration Rejection

**Artifact:** `_truth/receipts/NY_004_RESTORATION_REJECTION_V1.md`

**Commit:** `33acbc1843877e96985fb399c51f0a680ecb2784`

**Verdict:**

```text
VERDICT: RESTORATION_REJECTED
CAUSE: MISSING_RESTORATION_ARTIFACT
SCOPE: NY-004
HALT_STATUS: HALT_REMAINS_ACTIVE
```

**Constitutional result:** Jurisdiction remains suspended. Downstream nodes remain blocked.

---

## Dependency Graph

```text
NY-001:        VERIFIED
NY-003:        VERIFIED
NY-004:        HALT
NY-007B:       BLOCKED
NY-010:        BLOCKED
NY-011S:       BLOCKED
ALMS_RUN_002:  BLOCKED
```

---

## Current Lift Requirements

The halt remains active until all predicates in `_truth/receipts/NY_004_LIFT_CONDITIONS_V1.md` are satisfied, including:

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

---

## Constitutional Principle Demonstrated

```text
STRUCTURE != AUTHORITY
INTENT != AUTHORITY
REFERENCE != EVIDENCE
RESTORATION != VALID WITHOUT ARTIFACT
```

Only replay-verifiable evidence can restore jurisdiction.

---

## Closure Statement

The NY-004 membrane event currently terminates in a lawful halt:

```text
DETECTION -> HALT -> LIFT CONTRACT -> RESTORATION ATTEMPT -> REPLAY REFUSAL -> RESTORATION REJECTION
```

The system refused to restore authority without evidence.

Fail closed, never open.
