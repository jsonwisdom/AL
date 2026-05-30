# ALMS Speed Layer — Projection Observation (V0.1 Draft)

**Status:** DRAFT  
**Authority:** false  
**Membrane:** HOLDS  
**Advancement:** NONE  
**Sealing:** NONE  
**Hashing:** NONE  
**Receipts:** NONE  
**Epoch:** UNCHANGED

## Purpose

Define the V0.1 projection observation rules for the ALMS speed layer.
Observation determines how projection outputs are captured, structured, and replayed during deterministic runtime execution.

## Constraints

- No authority elevation
- No canonicalization
- No epoch creation
- No sealing
- No invented hashes
- No ghost references
- Must be replay-safe
- Must be GitHub-direct committed with a real SHA

## Observation Model (Draft)

### 1. Observation ID
- Deterministic, human-readable identifier
- Unique within the observation table
- No hashes, UUIDs, or opaque identifiers

### 2. Runtime Reference
- References a valid Projection Runtime entry
- Uses a real GitHub commit SHA
- References an existing repository path

### 3. Observation Envelope
- Deterministic only
- No external state
- No nondeterministic operations
- No authority advancement

### 4. Observation Types
- OUTPUT — direct capture of projection output
- STRUCTURE — structural observation of output
- META — contextual or relational observation

### 5. Replay Discipline
- Reproducible from GitHub-pinned bytes
- No assistant-invented state
- Operator-reported state allowed but non-authoritative

## Observation Table

| Field | Description | Constraints |
|---|---|---|
| observation_id | Deterministic identifier | Must be unique |
| runtime_id | Projection Runtime reference | Must exist |
| source_sha | GitHub commit SHA | Must be real |
| observation_type | OUTPUT / STRUCTURE / META | Must match envelope |
| observation_rule | Deterministic observation description | Optional |
| notes | Optional contextual notes | No lineage impact |

## Initial V0.1 Observations

No observations are defined in the V0.1 draft.
Population requires explicit operator or assistant action in future AL Game steps.

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_PROJECTION_OBSERVATION_V0_1",
  "status": "DRAFT_NON_CANONICAL",
  "authority": false,
  "membrane": "HOLDS"
}
```

End of V0.1 draft.
