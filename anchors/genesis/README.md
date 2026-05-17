# Genesis Replay Bundle

This directory is reserved for the first Replay Court witness anchor bundle.

The Genesis Replay Bundle turns the constitutional design into an externally verifiable checkpoint.

## Purpose

```text
Replay first.
Witness later.
Settlement downstream.
```

The witness root does not create truth.
It records the current replayable constitutional memory surface so outsiders can recompute it from public evidence.

## Expected Files

```text
anchors/genesis/README.md
anchors/genesis/anchor-manifest.json
```

## Genesis Manifest Requirements

The manifest must include:

```text
anchor_id: genesis_replay_court_witness_root
schema_version: 0.1.0
created_at: <ISO8601>
repo: jsonwisdom/AL
repo_commit: <commit sha>
previous_witness_root: GENESIS
reason: Genesis Replay Court witness root
protected_core_files[]
telemetry_heads[]
witness_root: sha256:<hash>
```

## Protected Core Files

```text
GAME_MECHANICS.md
AGENT_PLAYBOOK.md
COMPUTER_WISDOM.md
replay-court/PROCESS.md
replay-court/SELF-AUDIT.md
replay-court/VALIDATOR.md
replay-court/REPAIR-LEDGER.md
replay-court/CONTRADICTION-STORE.md
replay-court/AUTHORITY-BOUNDS.md
replay-court/WITNESS-ANCHOR.md
replay-court/BOOTSTRAP-REPLAY.md
replay-court/SCORE-LEDGER.md
replay-court/CONSTITUTIONAL-MAP.md
replay-court/REPORT-TEMPLATE.md
replay-court/receipt-schema.json
```

## Telemetry Heads

```text
artifacts/public/latest/level1-output.txt
artifacts/public/latest/verifier-current-tip.txt
artifacts/public/latest/oath.json
replay-court/example-report/README.md
```

## Canonicalization Rule v0

```text
1. Create records with file_path and sha256.
2. Sort records by file_path ascending.
3. Encode as deterministic JSON with sorted object keys and no insignificant whitespace.
4. Compute witness_root = sha256(canonical JSON bytes).
```

## Third-Party Verification

A verifier should be able to:

```text
1. fetch anchor-manifest.json
2. fetch every listed file at repo_commit
3. recompute each file sha256
4. canonicalize the listed records
5. recompute witness_root
6. confirm previous_witness_root is GENESIS
```

## Guardrails

```text
Witness root does not create truth.
Witness root does not authorize payment.
Witness root does not erase contradiction.
Witness root does not replace replay.
```

## Status

```text
GENESIS_BUNDLE_PLANNED
anchor-manifest.json pending generation
```
