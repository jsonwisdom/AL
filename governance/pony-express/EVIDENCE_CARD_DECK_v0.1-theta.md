# Evidence Card Deck v0.1-θ

**Classification:** PEDAGOGICAL_ONLY  
**Format:** printable / physical gameplay specification  
**Authority:** false  
**Historical truth established:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY

## 1. Purpose

Provide fictional evidence and procedure cards for the Civic War board game, moot court, law-student workbook, and Judicial Engineering Handbook.

Cards teach what an artifact can and cannot prove. They do not represent real evidence, cases, persons, or events.

## 2. Card Anatomy

Every card contains:

```text
CARD_ID
CARD_CLASS
TITLE
FICTIONAL_BOUNDARY
Z_LAYER
CLAIM_SUPPORTED
LIMITATION
INTEGRITY_STATUS
CUSTODY_STATUS
PLAY_EFFECT
REVERSAL_CONDITION
AUTHORITY = FALSE
```

## 3. Deck Classes

```text
SOURCE
CUSTODY
CLAIM
RULE
PROCEDURE
CHALLENGE
REVIEW
GAP
FORK
REFLECTION
```

## 4. Starter Deck — 24 Cards

### Source Cards

**EC-θ-001 — Source Byte Packet**  
Z0. Supports byte comparison only. Does not establish authorship, authority, or truth.

**EC-θ-002 — Text Excerpt**  
Z0/Z1. Readable fictional excerpt. Identity remains unproven until linked to a declared document.

**EC-θ-003 — Duplicate Copy**  
Z0. May establish byte equality with another token. Duplicate existence adds no independent truth weight.

**EC-θ-004 — Partial Record**  
Z0. Supports only the visible portion. Missing context must be marked as a gap.

### Custody Cards

**EC-θ-005 — Continuous Custody Log**  
Z2. Strengthens simulated provenance when every transfer is recorded.

**EC-θ-006 — Broken Custody**  
Z2. Marks provenance CONTESTED. Evidence may proceed only with an explicit limitation.

**EC-θ-007 — Anonymous Delivery**  
Z2. Route and receipt may be recorded; authorship and authority remain UNPROVEN.

**EC-θ-008 — Conflicting Timestamp**  
Z1/Z2. Creates a preserved fork. Players may not silently choose one timeline.

### Claim Cards

**EC-θ-009 — Witness Claim**  
Supports existence of a statement, not the truth of its contents.

**EC-θ-010 — Institutional Claim**  
Records what a fictional institution asserts. Does not self-prove jurisdiction or legality.

**EC-θ-011 — Negative Claim**  
Requires declared search scope. Absence from an incomplete record cannot prove nonexistence.

**EC-θ-012 — Competing Explanation**  
Introduces an alternative interpretation without erasing the original claim.

### Rule Cards

**EC-θ-013 — Mandatory Rule**  
Contains MUST language. Violation triggers procedural review.

**EC-θ-014 — Permissive Rule**  
Contains MAY language. Permission does not create obligation.

**EC-θ-015 — Prohibition**  
Contains MUST_NOT language. Cannot be waived by player agreement where a hard gate applies.

**EC-θ-016 — Ambiguous Rule**  
Requires two plausible readings and a clarifying rewrite before stable reuse.

### Procedure Cards

**EC-θ-017 — Jurisdiction Challenge**  
Pauses merits until Z4 scope is addressed.

**EC-θ-018 — Evidence Excluded**  
Removes a token from the current issue only; the token remains preserved in the session record.

**EC-θ-019 — Remand for Evidence**  
Returns the claim to the earliest unresolved Z layer.

**EC-θ-020 — Appeal Window**  
Permits review while preserving the original receipt, objections, and outcome.

### Gap, Fork, and Review Cards

**EC-θ-021 — Historical Gap**  
Missing information must remain missing. No invented bridge is allowed.

**EC-θ-022 — Preserved Fork**  
Two incompatible records remain visible until independently resolved.

**EC-θ-023 — Dissent**  
Records a reasoned minority interpretation. It has no independent authority.

**EC-θ-024 — Reversal Evidence**  
Declares the specific fictional evidence that would change a player’s position.

## 5. Play Rules

1. A card may affect only its declared Z layer and issue scope.
2. Cards cannot unlock Gate 1.
3. Source cards cannot self-authenticate.
4. Delivery and custody cards cannot establish substantive truth.
5. Challenge cards pause or narrow play; they do not destroy records.
6. Forks and gaps remain visible.
7. Every excluded card remains logged.
8. No card creates law, office, jurisdiction, historical truth, or public effect.

## 6. Card Resolution

```text
DRAW
DECLARE ISSUE
DECLARE TARGET Z LAYER
STATE SUPPORTED CLAIM
STATE LIMITATION
ALLOW CHALLENGE
RECORD RESULT
EMIT RECEIPT
```

Allowed results:

```text
ADMITTED_IN_GAME
LIMITED_IN_GAME
EXCLUDED_IN_GAME
CONTESTED
INDETERMINATE
REMANDED
```

## 7. Printable Layout

Recommended poker-card size: 2.5 × 3.5 inches.

Front:

```text
TITLE
CARD CLASS
Z LAYER
PLAY EFFECT
```

Back:

```text
CLAIM SUPPORTED
LIMITATION
REVERSAL CONDITION
PEDAGOGICAL_ONLY
AUTHORITY: FALSE
```

No colors are normative. Card class may also be represented by symbols for accessibility.

## 8. Deck Receipt

```json
{
  "receipt_id": "RECEIPT-ECD-<session>-<seq>",
  "deck_version": "EVIDENCE_CARD_DECK_v0.1-theta",
  "card_id": "EC-theta-000",
  "action": "DRAWN | PLAYED | CHALLENGED | LIMITED | EXCLUDED | PRESERVED",
  "result": "RECORDED | PASS | FAIL | CONTESTED | INDETERMINATE",
  "gate_1": "BLOCKED",
  "authority": false,
  "historical_truth_established": false,
  "previous_receipt_hash": null
}
```

## 9. Prohibited Cards and Effects

```text
REAL_PERSON_CARD
REAL_CASE_CARD
INVENTED_SOURCE_BYTES
GATE_1_BYPASS
AUTOMATIC_TRUTH
AUTOMATIC_AUTHORITY
FORK_DELETION
HISTORICAL_EQUIVALENCE
PUBLIC_JUDGMENT
```

## 10. Current State

```text
ARTIFACT                 = EVIDENCE_CARD_DECK_v0.1-theta
CARD_COUNT               = 24
CLASSIFICATION           = PEDAGOGICAL_ONLY
GATE_1                   = BLOCKED
CORE_DOCKET              = EMPTY
EXECUTION_AUTHORITY      = FALSE
HISTORICAL_VERIFICATION  = NOT_PERFORMED
PROMOTION                = BLOCKED
```
