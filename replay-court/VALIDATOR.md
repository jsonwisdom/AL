# Replay Court Validator

The Validator turns Replay Court constitutional rules into checkable failure modes.

It is an executable specification for validating reports, repairs, contradictions, receipts, and self-audit surfaces.

This document is not authority by itself.
It defines what a validator must check before authority can be claimed.

## Purpose

```text
Make doctrine mechanically checkable.
Make drift visible.
Reject hidden repair.
Reject erased contradiction.
Reject scoring drift.
```

## Validation Scope

The validator checks:

```text
- GAME_MECHANICS.md status rules
- level scores
- NEXT ACTION presence
- UNOBSERVED / FAIL separation
- repair ledger entries
- contradiction store records
- self-audit requirements
- public artifact references
- receipt guardrails
```

## Required Inputs

```text
GAME_MECHANICS.md
replay-court/SELF-AUDIT.md
replay-court/REPAIR-LEDGER.md
replay-court/CONTRADICTION-STORE.md
replay-court/REPORT-TEMPLATE.md
reports or example reports
public artifact mirrors when applicable
```

## Allowed Validator Outcomes

```text
VALIDATION_PASS
VALIDATION_FAIL
VALIDATION_UNOBSERVED
```

`VALIDATION_PASS` requires observed evidence.

`VALIDATION_FAIL` requires observed contradiction.

`VALIDATION_UNOBSERVED` means required evidence was missing, inaccessible, or not inspected.

## Check 1 — Status Schema

Allowed level statuses:

```text
PASS
FAIL
UNOBSERVED
PASS DOCS-ONLY
```

Levels 1-3 may only use:

```text
PASS
FAIL
UNOBSERVED
```

Reject:

```text
LOCKED
SUSPENDED
PENDING
PARTIAL
ASSUMED
PROBABLY_PASS
PASS DOCS-ONLY on Levels 1-3
```

Failure class:

```text
status_schema_drift
level_status_drift
```

## Check 2 — Point Values

Valid point mapping:

```text
PASS: 20
FAIL: 0
UNOBSERVED: 0
PASS DOCS-ONLY: 5
```

Reject any nonstandard value.

Failure class:

```text
scoring_drift
```

## Check 3 — NEXT ACTION

Every level must include a concrete `NEXT ACTION`.

Reject:

```text
None
N/A
No action
Not applicable
empty string
```

Failure class:

```text
next_action_drift
```

## Check 4 — UNOBSERVED / FAIL Separation

```text
UNOBSERVED = evidence missing, inaccessible, or not inspected.
FAIL = evidence observed and contradictory.
```

Reject reports that classify inaccessible evidence as FAIL.
Reject reports that classify observed contradiction as UNOBSERVED.

Failure class:

```text
evidence_classification_drift
```

## Check 5 — Sequential Progression

A higher level cannot be reached unless all prior levels are PASS.

Reject:

```text
HIGHEST_LEVEL_REACHED: 5
when Level 2 is FAIL or UNOBSERVED
```

Failure class:

```text
progression_drift
```

## Check 6 — Repair Ledger Integrity

Every repair entry must include:

```text
repair_id
contradiction_ref
contradiction_hash
pre_repair_state
repair_action
post_repair_state
historical_state_preserved: true
replay_rerun_ref
status
previous_repair_hash
entry_hash
```

Reject repair entries missing contradiction references.
Reject repair entries where `historical_state_preserved` is false.
Reject repair entries that hide or overwrite the pre-repair state.

Failure class:

```text
repair_ledger_drift
```

## Check 7 — Contradiction Store Integrity

Every contradiction record must include:

```text
contradiction_id
observed_where
observed_text
observed_text_hash
context_snapshot
context_hash
contradiction_class
why_it_matters
linked_repair_id
status
```

Allowed statuses:

```text
preserved
superseded
```

Reject:

```text
resolved
deleted
hidden
obsolete
forgotten
```

Failure class:

```text
contradiction_store_drift
```

## Check 8 — Repair / Contradiction Linkage

Every Repair Ledger `contradiction_ref` must resolve to a Contradiction Store record.

Every completed repair must point to a contradiction with status:

```text
preserved
```

A repair is invalid if its contradiction cannot be found.

Failure class:

```text
repair_contradiction_link_drift
```

## Check 9 — Self-Audit Trigger Coverage

A self-audit is required after changes to:

```text
GAME_MECHANICS.md
AGENT_PLAYBOOK.md
PROCESS.md
REPORT-TEMPLATE.md
receipt schemas
verifier contracts
public mirror outputs
issue closure after repair
```

Reject missing self-audit notes when trigger conditions occur.

Failure class:

```text
self_audit_trigger_drift
```

## Check 10 — Receipt Guardrails

Receipts must not claim:

```text
creates_truth: true
authorizes_payment: true
links_settlement: true
signature_present: true in v0 unless explicitly upgraded by doctrine
```

Failure class:

```text
receipt_authority_drift
```

## Minimal Validator Output

```text
VALIDATOR_RESULT:
VALIDATOR_VERSION:
INPUTS_OBSERVED:
INPUTS_UNOBSERVED:
CHECKS_PASSED:
CHECKS_FAILED:
DRIFT_FOUND:
NEXT_ACTION:
```

## Doctrine

```text
A validator may reject drift.
A validator may not create truth.
A validator may not authorize payment.
A validator may not erase contradiction.
A validator may not replace replay.
```

## Invariant

```text
If the rules cannot be checked, authority cannot be claimed.
```
