# Lineage Append-Only Store v1

**Artifact:** `LINEAGE_APPEND_ONLY_V1`

The lineage database is an append-only JSONL ledger used to preserve sovereign memory for asset bindings.

## Invariants

- Append-only
- No deletion
- No in-place modification
- Atomic append semantics
- Tamper-evident hash chain
- Replay-verifiable ordering

## Event Log

```text
lineage/asset_lineage_events.jsonl
```

Each line is exactly one JSON event.

## Hash Chain

Every event contains:

```json
{
  "prev_file_hash": "sha256:<hash>"
}
```

The hash refers to the SHA-256 of the event log *before* the append.

Verification rule:

```text
Replay all events in order.
For event N:
  prev_file_hash MUST equal SHA-256(file after event N-1).
Any mismatch:
  LINEAGE_TAMPER_DETECTED
```

## Purpose

The lineage layer prevents:

- hash rebind attacks
- silent history overwrite
- hidden provenance mutation
- trust-on-first-use state capture

## Constitutional Boundary

The lineage layer does not execute CBRE traces.
The lineage layer does not interpret SSD semantics.
The lineage layer preserves continuity.

## Core Law

```text
The trace proves computation.
The manifest proves declaration.
The lineage remembers continuity.
```
