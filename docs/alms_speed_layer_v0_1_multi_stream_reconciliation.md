# ALMS Speed Layer — Multi-Stream Reconciliation (V0.1 Draft)

**Status:** DRAFT  
**Authority:** false  
**Membrane:** HOLDS  
**Advancement:** NONE  
**Sealing:** NONE  
**Hashing:** NONE  
**Receipts:** NONE  
**Epoch:** UNCHANGED

## Purpose

Define the V0.1 multi-stream reconciliation model for the ALMS speed layer.
Reconciliation determines how multiple replay sessions, observations, and projections are aligned and compared in a deterministic replay environment.

## Constraints

- No authority elevation
- No canonicalization
- No epoch creation
- No sealing
- No invented hashes
- No ghost references
- Must be replay-safe
- Must be GitHub-direct committed with a real SHA

## Reconciliation Model

### Reconciliation ID
- Deterministic, human-readable identifier
- Unique within the reconciliation table
- No hashes, UUIDs, or opaque identifiers

### Boundary Reference
- References a valid Replay Boundary entry
- Uses a real GitHub commit SHA
- References an existing repository path

### Reconciliation Envelope
- Deterministic only
- No external state
- No nondeterministic operations
- No authority advancement

### Reconciliation Types
- ALIGN — align replay outputs across streams
- COMPARE — deterministic comparison of multi-stream results
- MERGE_STRUCTURE — deterministic structural merging without authority
- VERIFY_STRUCTURE — structural integrity check without truth claim

### Replay Discipline
- Reproducible from GitHub-pinned bytes
- No assistant-invented state
- Operator-reported state allowed but non-authoritative

## Multi-Stream Reconciliation Table

| Field | Description | Constraints |
|---|---|---|
| reconciliation_id | Deterministic identifier | Must be unique |
| boundary_id | Replay Boundary reference | Must exist |
| source_sha | GitHub commit SHA | Must be real |
| reconciliation_type | ALIGN / COMPARE / MERGE_STRUCTURE / VERIFY_STRUCTURE | Must match envelope |
| reconciliation_rule | Deterministic reconciliation description | Optional |
| notes | Optional contextual notes | No lineage impact |

## Initial V0.1 Reconciliations

No reconciliations are defined in the V0.1 draft.
Population requires explicit operator or assistant action in future AL Game steps.

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_MULTI_STREAM_RECONCILIATION_V0_1",
  "status": "DRAFT_NON_CANONICAL",
  "authority": false,
  "membrane": "HOLDS"
}
```

End of V0.1 draft.
