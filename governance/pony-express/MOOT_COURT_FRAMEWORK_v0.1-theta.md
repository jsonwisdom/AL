# Moot Court Framework v0.1-θ

**Parent systems:** `PONY_EXPRESS_v0.1`, `CIVIC_WAR_BOARD_GAME_v0.1`, `AMERICAN_HISTORY_3D_NAVIGATION_SCHEMA_v0.1`  
**Classification:** Pedagogical simulation / educational practice layer  
**Variant tag:** θ (theta) — structured argument & procedure  
**Authority:** false  
**Historical verification:** not performed  
**Promotion:** blocked  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY until source-admission rules are satisfied

## 1. Purpose

Provide a bounded, fail-closed practice environment in which participants rehearse:

- claim formulation,
- evidence attachment and integrity checks,
- jurisdictional analysis,
- structured oral and written argument,
- provisional ruling under declared procedure,
- appeal path preservation,
- receipt generation.

This framework teaches process. It does not adjudicate history, create public authority, or convert game outcomes into legal or historical truth.

```text
MOOT_RESULT          != HISTORICAL_TRUTH
MOOT_ROLE            != PUBLIC_OFFICE
SIMULATED_RULING     != ADJUDICATION
ROUTE_ACCESS         != JURISDICTION
BYTE_EQUALITY        = INTEGRITY_ONLY
DOCUMENT_EXISTENCE   != TRUTH
INTERPRETATION       != AUTHORITY
```

## 2. Constitutional Boundaries (Fail-Closed)

The moot court may:

- accept only packets that declare incomplete or verified status explicitly;
- require participants to separate claim, evidence, custody, jurisdiction, and requested effect;
- preserve forks and gaps rather than collapse them;
- issue simulation receipts;
- enforce turn order, time limits, and argument structure;
- record dissent and minority views.

The moot court may not:

- invent missing source bytes or provenance;
- treat a delivery receipt as authentication or truth;
- grant or expand real-world authority;
- populate the core historical docket without independent source admission;
- unlock Gate 1;
- declare any historical actor guilty or any historical act lawful solely by moot outcome;
- equate `CIVIC_WAR` gameplay with the historical `CIVIL_WAR` era.

## 3. Participant Roles (Simulation Only)

Roles grant procedural capabilities inside the session. They confer no public office, standing, or real authority.

```text
CHIEF_MODERATOR     — enforces procedure, time, and gate order; does not decide merits
CLAIMANT            — advances a structured claim with cited sources
RESPONDENT          — contests jurisdiction, evidence, or requested effect
AMICUS              — offers limited, non-binding supplemental argument (optional)
CLERK               — maintains the session ledger and receipt chain
PANEL               — issues provisional in-game rulings under declared rules
OBSERVER            — may watch; may not speak or vote unless invited
```

No participant may self-validate a disputed claim that rests on their own role.

## 4. Session Lifecycle

```text
1  OPEN_SESSION
2  ADMIT_PARTICIPANTS
3  STATE_QUESTION_PRESENTED
4  JURISDICTION_CHECK
5  EVIDENCE_EXCHANGE
6  ORAL_ARGUMENT
7  PANEL_DELIBERATION
8  PROVISIONAL_RULING
9  DISSENT_OR_CONCURRENCE
10 APPEAL_WINDOW
11 CLOSE_SESSION + RECEIPT
```

Every transition produces an append-only receipt. Failed or incomplete steps are recorded, never erased.

### 4.1 Question Presented

Must be a single, answerable procedural or interpretive question framed for simulation, e.g.:

```text
"Under the declared rules of this session, does Claimant’s evidence packet
satisfy Z0–Z4 gates for the limited purpose of continuing argument?"
```

Questions that demand real historical adjudication or real legal effect are rejected at intake.

### 4.2 Jurisdiction Check (Mandatory)

Before merits:

- Confirm the session is simulation-only.
- Confirm Gate 1 remains BLOCKED unless an external byte-capture pair has already been independently admitted (currently none).
- Confirm the claimed coordinate (time / geography / authority class) is inside the pedagogical scope.
- Reject any attempt to assert real-world enforcement power.

### 4.3 Evidence Exchange

Evidence is attached as references only. Actual source bytes, if any, remain outside the moot until Gate 1 is satisfied by an independent process.

Each attachment must declare:

```text
gate targeted:     Z0 | Z1 | Z2 | Z3 | Z4 | Z5 | Z6 | Z7 | Z8
integrity status:  UNTESTED | PASS | FAIL | INDETERMINATE
custody status:    UNPROVEN_BEFORE_INGESTION | ...
authority claim:   false (always inside this framework)
```

### 4.4 Oral Argument Structure

Default time box (adjustable by Chief Moderator):

```text
Claimant opening     8 min
Respondent opening   8 min
Claimant rebuttal    4 min
Respondent rebuttal  4 min
Panel questions      10 min
```

Argument must stay inside the Question Presented and the declared gates. New evidence introduced for the first time in oral argument is flagged and may be excluded from the provisional ruling.

### 4.5 Provisional Ruling

The Panel issues an in-game result only:

```text
UPHELD_IN_GAME
OVERRULED_IN_GAME
REMANDED_FOR_EVIDENCE
INDETERMINATE
DENIED_FOR_PROCEDURE
```

Every ruling carries the fixed annotations:

```text
authority: false
historical_truth_established: false
public_effect: none
```

### 4.6 Appeal Window

A denied or overruled claim may move to a higher simulated review node along an explicit path. The original record, evidence list, objections, and ruling are preserved in full. Appeal does not erase the prior receipt.

## 5. Depth-Gate Discipline (Inherited)

Rulings must respect the Z-layer order from the parent navigation schema:

```text
Z0 SOURCE_BYTES
Z1 DOCUMENT_IDENTITY
Z2 PROVENANCE_AND_CUSTODY
Z3 FORMAL_AUTHORITY_CLAIM
Z4 JURISDICTION
Z5 IMPLEMENTATION
Z6 EFFECT
Z7 LATER_REVIEW
Z8 INTERPRETATION
```

A participant may not jump from Z0 directly to Z8 inside the moot. Incomplete intermediate gates remain marked and limit the scope of any provisional result.

## 6. Receipt Model

Every material action emits a receipt compatible with Pony Express and Civic War schemas:

```json
{
  "receipt_id": "RECEIPT-MC-<session>-<seq>",
  "framework_version": "MOOT_COURT_v0.1-theta",
  "session_id": "MC-...",
  "action": "PROVISIONAL_RULING | EVIDENCE_ATTACHED | APPEAL_FILED | ...",
  "result": "PASS | FAIL | CONTESTED | INDETERMINATE | RECORDED",
  "authority": false,
  "historical_truth_established": false,
  "gate_1_status": "BLOCKED",
  "previous_receipt_hash": null,
  "recorded_at": null
}
```

Receipts are append-only. Corrections appear as new receipts.

## 7. Docket Rules

```text
CORE_DOCKET = EMPTY
```

No historical scenario may be placed on the core docket until it independently satisfies source-admission rules (byte-capture pair, provenance, and external verification). Practice questions and synthetic teaching hypos may be used for skill drills; they remain clearly labeled `PEDAGOGICAL_ONLY` and never migrate into the core historical deck.

## 8. Prohibited Outcomes

```text
MOOT_VOTE_CREATES_LAW                 = PROHIBITED
MOOT_ROLE_EQUALS_PUBLIC_OFFICE        = PROHIBITED
SIMULATED_RULING_EQUALS_HISTORY       = PROHIBITED
GATE_1_BYPASS_BY_CONSENT              = PROHIBITED
INVENTED_SOURCE_BYTES                 = PROHIBITED
COLLAPSE_OF_PRESERVED_FORKS           = PROHIBITED
EQUIVALENCE_CIVIL_WAR_CIVIC_WAR       = PROHIBITED
AUTHORITY_EXPANSION_BY_MERGE_OR_PR    = PROHIBITED
```

## 9. Integration Points

- **Pony Express** — transport of evidence packets and receipts only.
- **US3D Navigation** — coordinate system and depth layers.
- **Civic War Board Game** — optional scenario framing and scoring for integrity discipline.
- **Judicial Engineering Quantum Variant** — may be enabled as a separate experimental overlay; its tunneling and superposition mechanics remain subordinate to the procedural sequence above and cannot bypass Gate 1.

## 10. Current State

```text
ARTIFACT                 = MOOT_COURT_FRAMEWORK_v0.1-theta
PARENT                   = CIVIC_WAR_BOARD_GAME_v0.1 + PONY_EXPRESS_v0.1
GATE_1                   = BLOCKED
AUTHORITY                = FALSE
HISTORICAL_VERIFICATION  = NOT_PERFORMED
CORE_DOCKET              = EMPTY
EXECUTION                = SIMULATION_ONLY
PROMOTION                = BLOCKED
INTERPRETATION_LAYER     = LOCKED
```

## 11. Promotion Boundary

This document is a pedagogical candidate only. Presence on a branch or in a pull request does not make it normative. Activation of any real governance or historical claim requires an explicit external promotion action separate from transport, hashing, delivery, merge status, or moot outcome.
