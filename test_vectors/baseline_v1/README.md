# Baseline V1 — First Witness Scaffold

This directory contains the initial scaffold for the Baseline V1 witness vector.

## Status

State: `AWAITING_OPERATOR_UIDS_AND_RUNTIME_WITNESS`  
Issue: #79

## Purpose

Provide a minimal, schema-aligned structure for the first baseline witness.  
No UIDs, hashes, or runtime outputs are included.  
All placeholders must be replaced by the operator during runtime execution.

## Operator Edit Boundary

Only `input.json` is operator-editable prior to running the lineage walker.  
Do **not** modify this README during witness preparation or runtime execution.  
This file exists solely for human context and is **never** part of the witness surface.

## Contents

- `input.json` — Operator-fillable input envelope
- `output.json` — **Intentionally omitted** (must be produced by operator runtime)

## Next Steps

1. Operator supplies canonical UIDs for:
   - `start_uid`
   - any referenced attestations
2. Operator runs the lineage walker to produce:
   - `output.json` (runtime witness)
3. Commit `output.json` in a follow-up PR.

This scaffold ensures Copilot does not fabricate witness data and preserves the trust boundary.
