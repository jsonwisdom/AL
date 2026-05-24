# GOVERNANCE_BOUNDARY.md

## Constitutional Epoch

Genesis boundary commit: `fab0e39388aa37c971ab4d172f189173e19b1d9b`

All governance receipts and state transitions after this commit are constitutional.

Commits before this boundary are construction history and ignored for counting and replay.

## Canonical Receipt Path

`_truth/governance/`

All machine-issued receipts must live here. This directory is the single source of truth.

## GREEN Receipt Rules

- Issued only by successful workflow runs.
- Must be valid JSON matching the defined schema.
- Required fields: `receipt_id`, `track`, `status: "GREEN"`, `issued_by`, `timestamp_utc`, `constitutional_epoch_boundary`.
- No manual GREEN receipts.
- Failed heartbeat = no receipt issued.

## Transition Receipt Rules

- Issued when 3 consecutive GREEN receipts meet the threshold.
- Example filename: `HEARTBEAT_STABLE_TO_READY_RECEIPT.json`.
- Must record: `previous_state`, `next_state`, `trigger_condition`, `timestamp`, `verifier_path`.
- Transition receipt is written first.
- Next independent Heartbeat must validate the resulting state.

## Heartbeat Validation Rules

- Rust crate compiles.
- `cargo test` passes.
- Receipt fixtures parse correctly.
- Semantic invariants hold.
- Hashes, prefixes, and content bindings are valid.
- Transition receipts are consistent with prior history.
- Verifier checks its own issuance path.

## Stable Anchor Definition

Current stable state: `READY_FOR_CEREMONY`

The stable anchor is considered valid only if subsequent Verifier Heartbeats continue to return GREEN.

## Prohibited During Hold Phase

- DO NOT issue manual GREEN receipts.
- DO NOT mutate or reorder existing transition history.
- DO NOT add or modify workflows/automation.
- DO NOT introduce hidden state files outside the receipt directory.
- DO NOT bypass Heartbeat validation before advancing state.
- DO NOT infer state from workflow UI alone. State must be reconstructed from committed receipts.
- DO NOT alter the genesis boundary commit reference.

## Replay Procedure

1. `git clone` the repository.
2. Locate the constitutional epoch commit.
3. Scan canonical receipt directory for GREEN receipts after genesis.
4. Count consecutive GREEN receipts.
5. Replay transition receipts in order.
6. Validate final state against current HEAD.

The repository is the authoritative witness of state.
