# Judicial Engineering Handbook v0.1-θ

**Classification:** PEDAGOGICAL_ONLY  
**Authority:** false  
**Historical truth established:** false  
**Public effect:** none  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY

## 1. Purpose

Train learners to separate legal-style reasoning into inspectable stages without claiming to practice law, decide real disputes, or establish historical truth.

The handbook governs simulated exercises only.

```text
STUDY -> ISSUE -> RULE -> SOURCE -> GATE -> ARGUMENT -> REVIEW -> REFLECTION
```

## 2. Judicial Engineering Discipline

A learner must keep these objects distinct:

```text
FACT_ASSERTION
CLAIM
SOURCE_REFERENCE
SOURCE_BYTES
PROVENANCE
RULE_TEXT
RULE_INTERPRETATION
JURISDICTION
REQUESTED_EFFECT
SIMULATION_OUTCOME
```

No object inherits truth or authority merely because another object exists.

## 3. Core Invariants

```text
DOCUMENT_EXISTENCE != TRUTH
BYTE_EQUALITY = INTEGRITY_ONLY
ROUTE_ACCESS != JURISDICTION
INTERPRETATION != ADJUDICATION
SIMULATED_RULING != LAW
EDUCATIONAL_LINEAGE != LEGAL_PRECEDENT
GAME_RESULT != HISTORICAL_TRUTH
```

## 4. Learner Workflow

### 4.1 Frame the Question

Write one answerable question tied to declared rules and a limited simulated effect.

Reject questions that demand real legal advice, real guilt, real liability, or historical adjudication.

### 4.2 Identify the Issue

Classify the disagreement:

```text
JURISDICTION
ADMISSIBILITY
INTERPRETATION
PROCEDURE
CUSTODY
INTEGRITY
AUTHORITY_CLAIM
REQUESTED_EFFECT
```

### 4.3 State the Rule

Quote or reference the exact sandbox rule. Distinguish:

```text
MUST
MAY
MUST_NOT
UNSPECIFIED
AMBIGUOUS
```

### 4.4 Map the Z Depth

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

No argument may skip unresolved intermediate layers.

### 4.5 Test Evidence

For every evidence token ask:

1. What claim does it support?
2. Which Z layer does it target?
3. Is integrity known?
4. Is custody known?
5. Is the token contested?
6. What conclusion does it not support?

### 4.6 Build Both Sides

Every learner must produce:

```text
PRIMARY_ARGUMENT
BEST_COUNTERARGUMENT
LIMITING_PRINCIPLE
REVERSAL_CONDITION
```

A claim without a serious counterargument is incomplete.

### 4.7 Review Procedure Before Merits

Order:

```text
SCOPE
ROLE AUTHORITY
JURISDICTION
ADMISSIBILITY
MERITS
REMEDY OR SIMULATED EFFECT
APPEAL PATH
```

### 4.8 Record the Outcome

Allowed outcomes:

```text
UPHELD_IN_GAME
OVERRULED_IN_GAME
REMANDED_FOR_EVIDENCE
DENIED_FOR_PROCEDURE
INDETERMINATE
```

Every outcome carries:

```text
authority: false
historical_truth_established: false
public_effect: none
```

## 5. Precedent Discipline

Prior sandbox sessions may be:

```text
CITED_IN_GAME
DISTINGUISHED_IN_GAME
LIMITED_IN_GAME
OVERRULED_IN_GAME
REMANDED_IN_GAME
```

They may not be called binding law or historical precedent.

A later exercise must identify:

- the earlier rule set and version;
- the earlier facts or tokens;
- the exact similarity or distinction;
- whether any semantic rule changed.

## 6. Bias and Self-Examination

Before closing a session, each learner records:

- the outcome they initially wanted;
- the rule that constrained them most;
- the strongest excluded argument;
- the evidence that could reverse their position;
- whether they confused fairness, preference, procedure, and authority.

```text
SELF WITHOUT JUSTICE = EGO
JUSTICE WITHOUT STUDY = ACCIDENT
PRECEDENT WITHOUT REVIEW = DOGMA
WISDOM = TESTED JUDGMENT
```

## 7. Failure Modes

```text
INVENTED_BYTES
UNDECLARED_SOURCE
ROLE_SELF_VALIDATION
GATE_SKIPPING
FORK_COLLAPSE
MORAL_PREFERENCE_AS_RULE
OUTCOME_AS_AUTHORITY
REAL_CASE_IMPORT
HISTORICAL_EQUIVALENCE
UNRECORDED_RULE_CHANGE
```

Any failure produces a receipt and limits or terminates the exercise.

## 8. Handbook Receipt

```json
{
  "receipt_id": "RECEIPT-JEH-<session>-<seq>",
  "artifact": "JUDICIAL_ENGINEERING_HANDBOOK_v0.1-theta",
  "classification": "PEDAGOGICAL_ONLY",
  "action": "ISSUE_FRAMED | RULE_MAPPED | EVIDENCE_TESTED | ARGUMENT_REVIEWED | REFLECTION_RECORDED",
  "result": "PASS | FAIL | CONTESTED | INDETERMINATE | RECORDED",
  "gate_1": "BLOCKED",
  "authority": false,
  "historical_truth_established": false,
  "previous_receipt_hash": null
}
```

## 9. Current State

```text
ARTIFACT                 = JUDICIAL_ENGINEERING_HANDBOOK_v0.1-theta
CLASSIFICATION           = PEDAGOGICAL_ONLY
GATE_1                   = BLOCKED
CORE_DOCKET              = EMPTY
EXECUTION_AUTHORITY      = FALSE
HISTORICAL_VERIFICATION  = NOT_PERFORMED
PROMOTION                = BLOCKED
```
