# ALMS Speed Layer — Replay Boundary (V0.1 Draft)

**Status:** DRAFT  
**Authority:** false  
**Membrane:** HOLDS  
**Advancement:** NONE  
**Sealing:** NONE  
**Hashing:** NONE  
**Receipts:** NONE  
**Epoch:** UNCHANGED

## Purpose

Define the V0.1 replay boundary for the ALMS speed layer.
A replay boundary establishes the deterministic limits, scopes, and termination conditions for replay sessions.

## Constraints

- No authority elevation
- No canonicalization
- No epoch creation
- No sealing
- No invented hashes
- No ghost references
- Must be replay-safe
- Must be GitHub-direct committed with a real SHA

## Boundary Model

### Boundary ID
- Deterministic, human-readable identifier
- Unique within the boundary table
- No hashes, UUIDs, or opaque identifiers

### Session Reference
- References a valid Replay Session entry
- Uses a real GitHub commit SHA
- References an existing repository path

### Boundary Envelope
- Deterministic only
- No external state
- No nondeterministic operations
- No authority advancement

### Boundary Types
- START — define replay entry conditions
- LIMIT — define replay scope and constraints
- STOP — define deterministic termination
- CHECK — validate boundary adherence

### Replay Discipline
- Reproducible from GitHub-pinned bytes
- No assistant-invented state
- Operator-reported state allowed but non-authoritative

## Replay Boundary Table

| Field | Description | Constraints |
|---|---|---|
| boundary_id | Deterministic identifier | Must be unique |
| session_id | Replay Session reference | Must exist |
| source_sha | GitHub commit SHA | Must be real |
| boundary_type | START / LIMIT / STOP / CHECK | Must match envelope |
| boundary_rule | Deterministic boundary description | Optional |
| notes | Optional contextual notes | No lineage impact |

## Initial V0.1 Boundaries

No replay boundaries are defined in the V0.1 draft.
Population requires explicit operator or assistant action in future AL Game steps.

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_REPLAY_BOUNDARY_V0_1",
  "status": "DRAFT_NON_CANONICAL",
  "authority": false,
  "membrane": "HOLDS"
}
```

End of V0.1 draft.
