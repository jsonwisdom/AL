# ALMS Speed Layer — Projection Replay Surface (V0.1 Draft)

**Status:** DRAFT
**Authority:** false
**Membrane:** HOLDS
**Advancement:** NONE
**Sealing:** NONE
**Hashing:** NONE
**Receipts:** NONE
**Epoch:** UNCHANGED

## Purpose

Define the V0.1 projection replay surface for the ALMS speed layer.
The replay surface specifies how projection observations are reconstructed, replayed, and compared within deterministic boundaries.

## Constraints

- No authority elevation
- No canonicalization
- No epoch creation
- No sealing
- No invented hashes
- No ghost references
- Must be replay-safe
- Must be GitHub-direct committed with a real SHA

## Replay Surface Model

### Replay ID
- Deterministic, human-readable identifier
- Unique within the replay table
- No hashes, UUIDs, or opaque identifiers

### Observation Reference
- References a valid Projection Observation entry
- Uses a real GitHub commit SHA
- References an existing repository path

### Replay Envelope
- Deterministic only
- No external state
- No nondeterministic operations
- No authority advancement

### Replay Types
- RECONSTRUCT — deterministic reconstruction of observation
- VERIFY_STRUCTURE — structural consistency check
- COMPARE — deterministic comparison across observations

### Replay Discipline
- Reproducible from GitHub-pinned bytes
- No assistant-invented state
- Operator-reported state allowed but non-authoritative

## Replay Surface Table

| Field | Description | Constraints |
|---|---|---|
| replay_id | Deterministic identifier | Must be unique |
| observation_id | Projection Observation reference | Must exist |
| source_sha | GitHub commit SHA | Must be real |
| replay_type | RECONSTRUCT / VERIFY_STRUCTURE / COMPARE | Must match envelope |
| replay_rule | Deterministic replay description | Optional |
| notes | Optional contextual notes | No lineage impact |

## Initial V0.1 Replay Surfaces

No replay surfaces are defined in the V0.1 draft.
Population requires explicit operator or assistant action in future AL Game steps.

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_PROJECTION_REPLAY_SURFACE_V0_1",
  "status": "DRAFT_NON_CANONICAL",
  "authority": false,
  "membrane": "HOLDS"
}
```

End of V0.1 draft.
