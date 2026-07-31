# Historical Research Gate v0.1-θ

**Classification:** Pedagogical admission-design artifact  
**Authority:** false  
**Execution:** design-only  
**Gate 1:** BLOCKED  
**Historical verification:** NOT_PERFORMED  
**Promotion:** BLOCKED

## 1. Purpose

Define a fail-closed process for evaluating whether real historical material could become eligible for later review. This document does not admit evidence, open Gate 1, establish historical truth, or authorize publication.

```text
CAPTURE != ADMISSION
HASH != AUTHENTICATION
PROVENANCE != TRUTH
REVIEW_ELIGIBILITY != APPROVAL
APPROVAL != PUBLICATION
```

## 2. Pipeline

```text
CAPTURE
→ HASH
→ IDENTITY_CHECK
→ PROVENANCE
→ CUSTODY_REVIEW
→ SOURCE_COMPARISON
→ AUTHORITY_CLASSIFICATION
→ CONFLICT_AND_GAP_ANALYSIS
→ EXTERNAL_VERIFICATION
→ ADMISSION_REVIEW
→ ELIGIBLE | REJECTED | INDETERMINATE
```

No stage may be skipped. Failure, ambiguity, or missing evidence produces a receipt and stops forward movement.

## 3. Gate States

```text
UNOPENED
PENDING_INPUT
IN_REVIEW
PASS_LIMITED
FAIL
INDETERMINATE
```

`PASS_LIMITED` means only that a declared stage was satisfied for a bounded purpose. It does not satisfy later gates.

## 4. Required Capture Packet

Each candidate object must declare:

- object ID
- source URI or physical locator
- capture method
- capture timestamp
- media type
- byte length
- SHA-256 digest
- claimed author
- claimed date
- claimed jurisdiction
- custody before capture
- capture operator
- uncertainty notes

Missing source bytes produce `NO_SOURCE_BYTES` and halt the pipeline.

## 5. Integrity Gate

Hash equality establishes byte integrity only.

```text
BYTE_EQUALITY = INTEGRITY_ONLY
INCLUSION_PROOF != AUTHORSHIP
HASH_MATCH != TRUTH
```

At least two independently acquired captures are required for Gate 1 consideration unless a separate exception artifact is authorized externally. No exception exists in this version.

## 6. Identity and Provenance

Identity review asks whether the object is what it claims to be. Provenance review asks how it moved from creation to capture.

Required outputs:

```text
identity_status: VERIFIED | CONTESTED | UNPROVEN | FAIL
provenance_status: VERIFIED | PARTIAL | CONTESTED | UNPROVEN | FAIL
custody_status: COMPLETE | PARTIAL | BROKEN | UNKNOWN
```

Partial provenance cannot be silently promoted to complete provenance.

## 7. Source Comparison

Candidate material must be compared against independent sources where available.

Comparison outcomes:

```text
CORROBORATED
PARTIALLY_CORROBORATED
CONTRADICTED
UNIQUE_SOURCE
INDETERMINATE
```

Conflicting records must remain forked. Missing history must remain an explicit gap.

## 8. Authority Classification

The gate may classify a document's claimed authority type and state. It may not adjudicate validity.

```text
CLASSIFICATION != ADJUDICATION
DOCUMENT_EXISTENCE != AUTHORITY
OFFICIAL_FORMAT != LEGAL_VALIDITY
```

## 9. External Verification

External verification must be independent of the capture operator and the proponent of admission.

The verifier must declare:

- verifier identity or pseudonymous key
- method
- environment
- source access
- findings
- conflicts of interest
- signature or attestation reference

Self-verification cannot complete this stage.

## 10. Admission Review

Admission Review may return only:

```text
ELIGIBLE_FOR_LIMITED_REVIEW
REJECTED
REMANDED_FOR_MORE_EVIDENCE
INDETERMINATE
```

Eligibility creates no authority and does not populate the core docket automatically.

A separate authorization artifact would be required to move an eligible object into any historical docket. That artifact is outside scope and does not exist here.

## 11. Receipts

Every transition emits an append-only receipt containing:

- receipt ID
- object ID
- stage
- result
- evidence references
- reviewer
- timestamp
- previous receipt hash
- authority: false
- Gate 1 status
- historical truth established: false

Corrections create new receipts. Existing receipts are never overwritten.

## 12. Fail-Closed Rules

```text
NO_SOURCE_BYTES       -> HALT
NO_SECOND_CAPTURE     -> GATE_1_REMAINS_BLOCKED
HASH_MISMATCH         -> FORK_AND_HALT
UNKNOWN_PROVENANCE    -> NO_PROVENANCE_PASS
SELF_VERIFICATION     -> EXTERNAL_VERIFICATION_FAIL
CONFLICTING_RECORDS   -> FORK_DO_NOT_COLLAPSE
MISSING_HISTORY       -> GAP_DO_NOT_INVENT
UNRESOLVED_AUTHORITY  -> NO_AUTHORITY_PASS
```

## 13. Separation from Pedagogical Docket

Synthetic cases may continue under `PEDAGOGICAL_ONLY`. Real historical material may not enter the moot-court core docket through this design artifact.

```text
PEDAGOGICAL_DOCKET != HISTORICAL_DOCKET
PRACTICE_RECEIPT != ADMISSION_RECEIPT
MOOT_OUTCOME != HISTORICAL_FINDING
```

## 14. Current State

```text
ARTIFACT                 = HISTORICAL_RESEARCH_GATE_v0.1-theta
GATE_1                   = BLOCKED
CAPTURE_PAIRS_ADMITTED   = 0
CORE_DOCKET              = EMPTY
AUTHORITY                = FALSE
EXECUTION                = DESIGN_ONLY
HISTORICAL_VERIFICATION  = NOT_PERFORMED
PROMOTION                = BLOCKED
```
