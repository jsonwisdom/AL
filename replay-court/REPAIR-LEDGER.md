# Replay Court Repair Ledger

The Repair Ledger is the append-only memory surface for Replay Court repairs.

If a repair is not recorded here, it did not happen as a Replay Court repair.

If a repair is recorded here, the contradiction it references must remain preserved.

## Purpose

```text
No hidden repair.
No erased contradiction.
No self-exemption.
```

The ledger makes repair activity visible by construction.

## Ledger Rules

```text
- append-only
- one entry per bounded repair
- every repair must reference a contradiction
- every contradiction must remain preserved
- every repair must identify the smallest safe action
- every repair must include pre-repair and post-repair evidence
- every repair must include a replay / rescore result when applicable
```

Do not edit prior entries except to add a clearly marked correction entry that points to the original entry.

## Entry Schema

```text
repair_id:
created_at:
report_or_issue_ref:
trigger:
contradiction_ref:
contradiction_hash:
pre_repair_state:
repair_action:
repair_diff_ref:
post_repair_state:
historical_state_preserved: true / false
replay_rerun_ref:
post_repair_score:
status: open / completed / superseded
next_action:
```

## Hash Chain Fields

Each entry should include:

```text
previous_repair_hash:
entry_hash:
```

`entry_hash` is computed over the canonical entry content excluding `entry_hash` itself.

The first entry may use:

```text
previous_repair_hash: GENESIS
```

## Validation Rule

A repair is invalid if:

```text
- contradiction_ref is missing
- contradiction_hash is missing
- historical_state_preserved is false
- repair_action erases the original contradiction
- post_repair_state hides pre_repair_state
- no replay or rescore is performed when public artifacts are affected
```

## Entry 001 — Issue #228 verifier contract repair

```text
repair_id: repair_001_issue_228_verifier_contract
created_at: 2026-05-17T12:28:17Z
report_or_issue_ref: https://github.com/jsonwisdom/AL/issues/228
trigger: Route B public artifact contradiction
contradiction_ref: artifacts/public/latest/verifier-current-tip.txt
contradiction_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
pre_repair_state: RECEIPT_CONFIRMED + status: failure
repair_action: separate verifier_verdict from recorded_outcome_status
repair_diff_ref: commit d7e179f6a4f0e9dc2b4ef882b17905fb81d133c1
post_repair_state: RECEIPT_CONFIRMED + verifier_verdict: confirmed + recorded_outcome_status: failure
historical_state_preserved: true
replay_rerun_ref: artifacts/public/latest/* refreshed after repair
post_repair_score: 100
status: completed
next_action: monitor future verifier outputs for verifier_contract_drift
previous_repair_hash: GENESIS
entry_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
```

## Doctrine

```text
A repair may clarify semantics.
A repair may not erase history.
A repair may not grant authority.
A repair may not activate settlement.
```

## Invariant

```text
Contradiction preservation is required for repair legitimacy.
```
