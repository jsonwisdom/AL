# NY-004 Precedent Summary v1

## Purpose

Distill the NY-004 membrane event into a canonical precedent for future ALMS halts, lift contracts, restoration attempts, and restoration rejections.

This document is a precedent summary.
It does not lift the NY-004 halt.
It does not restore jurisdiction.
It does not verify NY-004.

---

## Precedent Name

```text
NY-004_UNVERIFIED_INPUT_RESTORATION_REJECTION_PRECEDENT
```

---

## Binding Case File

- **Issue:** #132
- **Detection record:** https://github.com/jsonwisdom/AL/issues/132
- **Halt receipt:** `_truth/receipts/NY_ALMS_HALT_001.md`
- **Lift contract:** `_truth/receipts/NY_004_LIFT_CONDITIONS_V1.md`
- **Restoration rejection:** `_truth/receipts/NY_004_RESTORATION_REJECTION_V1.md`
- **Constitutional timeline:** `_truth/receipts/NY_004_CONSTITUTIONAL_TIMELINE_V1.md`

---

## Holding

```text
A referenced claim does not become admissible evidence until the underlying artifact is committed, inspectable, hash-verifiable, and replay-admissible.
```

A structurally valid restoration receipt cannot restore jurisdiction if the evidence it certifies is absent.

---

## Rule

```text
REFERENCE != EVIDENCE
STRUCTURE != AUTHORITY
INTENT != AUTHORITY
RESTORATION != VALID WITHOUT ARTIFACT
UNVERIFIABLE != FALSE
UNVERIFIABLE = OUTSIDE_JURISDICTION
```

---

## Facts

1. README and methodology documents referenced NY-004 as a locked 6/62 NOAA GSOD 2024 climate receipt.
2. Repository inspection did not locate the concrete NY-004 artifact.
3. Issue #132 was opened to pin the verification gap.
4. `NY_ALMS_HALT_001.md` formalized the halt.
5. `NY_004_LIFT_CONDITIONS_V1.md` defined the lift predicates.
6. A restoration receipt was proposed referencing `_truth/bigquery/ny004_noaa_gsod_join.csv`.
7. Repository inspection returned `NOT_FOUND` for that artifact.
8. `NY_004_RESTORATION_REJECTION_V1.md` rejected restoration.
9. `NY_004_CONSTITUTIONAL_TIMELINE_V1.md` indexed the complete jurisprudence chain.

---

## Constitutional Basis

This precedent rests on:

1. **Input-side membrane**
   - Missing evidence halts dependent claims.

2. **Replay supremacy**
   - Documentation, summaries, issues, and operator statements cannot substitute for replay-verifiable artifacts.

3. **Negative-space doctrine**
   - Absence is recorded as absence, not converted into interpretation.

4. **No ghost promotion**
   - Referenced claims cannot advance to verified status without committed evidence.

5. **No ghost restoration**
   - Halted jurisdiction cannot resume based on a restoration statement that references absent evidence.

---

## Operational Consequence

Future ALMS restoration attempts MUST satisfy this precedent before jurisdiction may resume.

A future restoration attempt MUST include:

```text
DIRECT_ARTIFACT_FOUND
AND ARTIFACT_PATH_DECLARED
AND ARTIFACT_HASH_VERIFIED
AND CHAIN_LINKAGE_VERIFIED
AND REQUIRED_ENUMERATION_VERIFIED
AND NO_FORBIDDEN_CLAIMS_VERIFIED
AND REPLAY_ADMISSIBILITY_VERIFIED
```

If any predicate fails:

```text
RESTORATION_REJECTED
HALT_REMAINS_ACTIVE
```

---

## Current NY-004 Status

```text
NY-004:        HALT
NY-007B:       BLOCKED
NY-010:        BLOCKED
NY-011S:       BLOCKED
ALMS_RUN_002:  BLOCKED
```

The halt remains active until all predicates in `_truth/receipts/NY_004_LIFT_CONDITIONS_V1.md` pass.

---

## Citation Form

Future artifacts may cite this precedent as:

```text
NY-004_UNVERIFIED_INPUT_RESTORATION_REJECTION_PRECEDENT
```

or:

```text
_truth/receipts/NY_004_PRECEDENT_SUMMARY_V1.md
```

---

## Closure Statement

This precedent establishes that ALMS records failed restoration attempts as first-class constitutional events.

The system refused to restore authority without evidence.

Fail closed, never open.
