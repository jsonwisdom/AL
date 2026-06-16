# Eval Receipt Adapter

A lightweight post-run adapter for emitting replay-verifiable evaluation receipts.

The adapter shadows an existing evaluation pipeline without requiring deep runtime refactors.

## Goals

- hash verification-critical artifacts
- emit deterministic receipts
- support local replay verification
- avoid adding latency to the primary eval path
- keep cloud and blockchain anchoring optional

## Quickstart

1. Configure artifact paths in `adapter.config.yaml`
2. Run after an eval completes:

```bash
python3 emit_receipt.py --config adapter.config.yaml
```

3. Receipt output:

```text
receipts/eval-receipt.json
```

## Current Scope

This adapter verifies the integrity of the evaluation transformation pipeline:

- dataset artifact
- prompt/template artifact
- output artifact
- system version metadata
- deterministic receipt lineage

## Explicit Non-Claims

This project does not claim deterministic replay of frontier model API behavior.

The v1 replay surface is intentionally narrower:

```text
input artifacts
→ execution metadata
→ output artifact
→ receipt lineage
```

## Optional Future Hooks

- GCS archival
- Base/EAS attestation
- CI artifact uploads
- eval framework adapters
