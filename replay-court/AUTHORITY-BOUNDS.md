# Replay Court Authority Bounds

Authority in Replay Court is bounded by replayable evidence, preserved contradiction, and validator-checkable process.

No actor may quietly weaken the rules that constrain their own authority.

Authority derives from checkability, not from role.

## Purpose

```text
Close the self-exemption loophole.
Protect the validator.
Protect contradiction memory.
Protect repair legitimacy.
Make authority changes visible, reviewable, and replayable.
```

## Protected Core

The following files are protected core surfaces:

```text
GAME_MECHANICS.md
AGENT_PLAYBOOK.md
replay-court/PROCESS.md
replay-court/SELF-AUDIT.md
replay-court/VALIDATOR.md
replay-court/REPAIR-LEDGER.md
replay-court/CONTRADICTION-STORE.md
replay-court/REPORT-TEMPLATE.md
replay-court/receipt-schema.json
```

Only a Structural Amendment may remove a file from the protected core.

## Amendment Classes

### Minor Amendment

Examples:

```text
- typo fixes
- formatting
- link updates
- non-normative examples
```

Requirements:

```text
review: one reviewer
contradiction_ref: optional
time_lock: none
self_audit_required: no unless protected semantics change
```

### Operational Amendment

Examples:

```text
- scoring details
- report format
- route handling
- validator checks
- receipt field requirements
- public artifact path rules
```

Requirements:

```text
review: two independent approvals, neither being the proposer
contradiction_ref: required
time_lock: 48 hours
self_audit_required: yes
impact_note: required
```

### Structural Amendment

Examples:

```text
- allowed status values
- UNOBSERVED / FAIL semantics
- contradiction preservation rules
- repair legitimacy rules
- self-audit triggers
- validator authority
- protected core list
- settlement boundary doctrine
- this file
```

Requirements:

```text
review: three-person unanimous supermajority, none being the proposer
contradiction_ref: required
time_lock: 7 days
self_audit_required: yes
impact_analysis: required
external_witness: required when available
```

## Auto-Escalation Rule

Any proposal that weakens constraints on the proposer, validator, repair ledger, contradiction store, or protected core is automatically treated as Structural.

The label chosen by the proposer does not control the amendment class.

Validator must reject under-classified proposals.

## Contradiction-Linked Rationale

Operational and Structural amendments must cite a preserved contradiction:

```text
Contradiction: <contradiction_hash or contradiction_id>
Contradiction: <hash> - <one-line summary>
```

No contradiction reference, no merge.

Rationale must answer:

```text
- What contradiction forced this change?
- Where is it preserved?
- Why is this the smallest safe amendment?
- What authority surface does this affect?
- What downstream reports or receipts require replay?
```

## Time-Lock Rules

```text
Minor: none
Operational: 48 hours
Structural: 7 days
```

The time-lock begins only after:

```text
- amendment class is declared
- contradiction reference is supplied when required
- impact note or analysis is included
- required reviewers are requested
```

Time-lock starts at proposal publication, not at first review.

Time-lock cannot be bypassed by force-push, rebase, or new PR.

Emergency bypass is not allowed in v0.

## Self-Audit Triggers

A self-audit is required after:

```text
- any Structural amendment
- any Operational amendment to validator/scoring/reporting/receipt rules
- any failed bypass attempt
- any validator rejection involving protected core
- any edit to the protected core list
- any change to this file
```

Self-audit must reference:

```text
- amendment id
- contradiction_ref
- affected protected files
- validator result
- replay impact
- next action
```

## Validator Enforcement Hooks

Validator must check:

```text
1. protected_core_change_detected
2. amendment_class_declared
3. contradiction_ref_required_and_present
4. time_lock_required_and_satisfied
5. self_audit_triggered_when_required
6. proposer_authority_not_self-weakened_without_structural_review
```

If any authority-bounds check fails, result is FAIL, not UNOBSERVED. UNOBSERVED is not acceptable for authority changes.

Failure classes:

```text
authority_bounds_drift
protected_core_drift
amendment_class_drift
contradiction_rationale_drift
time_lock_drift
self_exemption_drift
```

## Forbidden Moves

```text
- removing contradiction preservation without Structural review
- weakening validator checks without contradiction-linked rationale
- editing repair history to hide pre-repair state
- deleting preserved contradictions
- treating payment or settlement as authority to amend replay truth
- changing allowed status values as a Minor or Operational amendment
- weakening this file through a lower amendment class
```

## Doctrine

```text
Authority is earned by checkable process.
Process changes require preserved contradiction.
Protected memory cannot be quietly weakened.
No actor may exempt themselves from replay.
```

## Invariant

```text
If the authority boundary cannot be checked, authority cannot be claimed.
```

<!-- validator-timelock-test: structural metadata present, timelock immature -->
