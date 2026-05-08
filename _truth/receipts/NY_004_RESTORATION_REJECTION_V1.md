# NY-004 Restoration Rejection Receipt v1

## Purpose

Formally record the rejection of a proposed NY-004 restoration receipt because the restoration artifact it referenced was not present in the repository.

This receipt confirms that the NY-004 halt remains active.

---

## Bound Membrane Event

- **Issue:** #132
- **Halt receipt:** `_truth/receipts/NY_ALMS_HALT_001.md`
- **Lift contract:** `_truth/receipts/NY_004_LIFT_CONDITIONS_V1.md`
- **Attempted restoration artifact:** `NY-004_RESTORATION_RECEIPT_V1.md`
- **Claimed restored data artifact:** `_truth/bigquery/ny004_noaa_gsod_join.csv`

---

## Attempted Restoration

A proposed restoration receipt asserted that NY-004 jurisdiction could be restored because the NOAA GSOD join artifact was present, hash-pinned, and replay-validated.

The proposed restoration referenced:

```text
_truth/bigquery/ny004_noaa_gsod_join.csv
```

---

## Replay / Repo Inspection Result

Repository inspection for the referenced artifact returned:

```text
NOT_FOUND
```

Therefore the proposed restoration receipt is inadmissible.

---

## Rejection Verdict

```text
VERDICT: RESTORATION_REJECTED
CAUSE: MISSING_RESTORATION_ARTIFACT
SCOPE: NY-004
HALT_STATUS: HALT_REMAINS_ACTIVE
```

The rejection is structural, not narrative.

A structurally valid restoration receipt cannot restore jurisdiction if the evidence it certifies is absent.

---

## Constitutional Basis

### 1. Input-Side Membrane

Referenced artifacts must exist as committed, inspectable, hash-verifiable inputs before restoration can be considered.

### 2. Replay Supremacy

A restoration statement is not authority.
Replay inspection controls admissibility.

### 3. Negative-Space Doctrine

Missing restoration evidence must be recorded as absence, not converted into resumed jurisdiction.

### 4. No Ghost Restoration

A halted chain may not resume based on a claim that evidence exists.
The evidence itself must be present and replay-verifiable.

---

## Active Halt Chain

```text
DETECTION:        Issue #132
FORMALIZATION:    NY_ALMS_HALT_001
LIFT CONTRACT:    NY_004_LIFT_CONDITIONS_V1
RESTORATION:      REJECTED
ENFORCEMENT:      HALT_REMAINS_ACTIVE
```

---

## Downstream Status

```text
NY-004:        HALT
NY-007B:       BLOCKED
NY-010:        BLOCKED
NY-011S:       BLOCKED
ALMS_RUN_002:  BLOCKED
```

No downstream NY climate-economic claim may resume until all lift conditions are satisfied by committed evidence.

---

## Required Condition for Future Restoration

A future restoration receipt may be considered only after:

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

Until then:

```text
HALT_REMAINS_ACTIVE
```

---

## Closure Statement

The system rejected a ghost restoration before it could mutate jurisdiction.

Fail closed, never open.
