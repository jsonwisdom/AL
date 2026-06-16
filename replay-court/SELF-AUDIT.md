# Replay Court Self-Audit

Replay Court must be replayable against itself.

A system that audits others but not itself recreates the classic institutional failure mode.

This document defines how Replay Court audits its own reports, receipts, scoring, drift classifications, repairs, and publication decisions.

## Core Principle

```text
The audit process is itself auditable.
```

Replay Court does not get exemption from its own rules.

## What Must Be Self-Audited

```text
- intake classification
- route selection
- evidence inventory
- level scoring
- status values
- UNOBSERVED / FAIL separation
- drift classification
- repair scope
- report verdict
- publication notes
- receipt generation
- public mirror freshness
```

## Self-Audit Triggers

A self-audit is required when any of these occur:

```text
- GAME_MECHANICS.md changes
- AGENT_PLAYBOOK.md changes
- PROCESS.md changes
- REPORT-TEMPLATE.md changes
- receipt schema changes
- verifier contract changes
- repeated drift class appears
- public mirror output changes
- a report claims 100/100
- an issue is closed as completed after repair
```

## Self-Audit Questions

Every self-audit must answer:

```text
1. Did the report use only allowed statuses?
2. Were points assigned according to GAME_MECHANICS.md?
3. Was UNOBSERVED kept separate from FAIL?
4. Did downstream levels depend on upstream PASS states?
5. Was the smallest safe repair used?
6. Was any historical failure erased, hidden, or renamed into success?
7. Were public artifacts refreshed after repair?
8. Was settlement kept downstream?
9. Did any receipt imply truth without replay?
10. Does the final verdict match the observed evidence?
```

## Allowed Self-Audit Verdicts

```text
SELF_AUDIT_PASS
SELF_AUDIT_FAIL
SELF_AUDIT_UNOBSERVED
```

`SELF_AUDIT_PASS` requires observed evidence.

`SELF_AUDIT_FAIL` requires observed contradiction.

`SELF_AUDIT_UNOBSERVED` means required evidence was missing, inaccessible, or not inspected.

## Self-Audit Receipt Requirements

A self-audit should produce a receipt with:

```text
receipt_type: self_audit_receipt
report_id
process_ref
mechanics_ref
observed_artifacts[]
unobserved_artifacts[]
self_audit_questions[]
verdict
next_action
created_at
```

The receipt records the self-audit.
It does not create truth.
It does not replace replay.

## Repair Rules

If self-audit finds drift:

```text
- classify drift
- preserve the original report
- identify smallest safe repair
- repair only the boundary needed
- rerun affected public artifacts
- rescore honestly
- add a self-audit note to the report or issue
```

Do not rewrite history to make the process look clean.

## Contradiction Preservation

Contradictions must remain visible.

```text
original_state:
observed_contradiction:
repair_action:
post_repair_state:
historical_state_preserved: true / false
```

A repair is not valid if it requires erasing the contradiction that justified it.

## Example: Issue #228

```text
original_state: RECEIPT_CONFIRMED + status: failure
observed_contradiction: verifier verdict collapsed with historical receipt outcome
repair_action: separate verifier_verdict from recorded_outcome_status
post_repair_state: RECEIPT_CONFIRMED + verifier_verdict: confirmed + recorded_outcome_status: failure
historical_state_preserved: true
```

## Invariant

```text
No self-exemption.
No hidden repair.
No erased contradiction.
No settlement before replay.
No receipt-as-truth shortcut.
```

Replay Court survives only if it remains replayable against itself.
