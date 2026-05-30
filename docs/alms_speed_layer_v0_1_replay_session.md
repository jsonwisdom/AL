# ALMS Speed Layer — Replay Session (V0.1 Draft)

**Status:** DRAFT  
**Authority:** false  
**Membrane:** HOLDS  
**Advancement:** NONE  
**Sealing:** NONE  
**Hashing:** NONE  
**Receipts:** NONE  
**Epoch:** UNCHANGED

## Purpose

Define the V0.1 replay session model for the ALMS speed layer.
A replay session represents a single deterministic execution instance of replay coordination, projection reconstruction, and observation capture.

## Constraints

- No authority elevation
- No canonicalization
- No epoch creation
- No sealing
- No invented hashes
- No ghost references
- Must be replay-safe
- Must be GitHub-direct committed with a real SHA

## Session Model

### Session ID
- Deterministic, human-readable identifier
- Unique within the session table
- No hashes, UUIDs, or opaque identifiers

### Coordinator Reference
- References a valid Replay Coordinator entry
- Uses a real GitHub commit SHA
- References an existing repository path

### Session Envelope
- Deterministic only
- No external state
- No nondeterministic operations
- No authority advancement

### Session Types
- INIT — initialize replay context
- EXECUTE — run replay operations
- COLLECT — gather replay outputs
- FINALIZE — close session without sealing

### Replay Discipline
- Reproducible from GitHub-pinned bytes
- No assistant-invented state
- Operator-reported state allowed but non-authoritative

## Replay Session Table

| Field | Description | Constraints |
|---|---|---|
| session_id | Deterministic identifier | Must be unique |
| coordinator_id | Replay Coordinator reference | Must exist |
| source_sha | GitHub commit SHA | Must be real |
| session_type | INIT / EXECUTE / COLLECT / FINALIZE | Must match envelope |
| session_rule | Deterministic session description | Optional |
| notes | Optional contextual notes | No lineage impact |

## Initial V0.1 Sessions

No replay sessions are defined in the V0.1 draft.
Population requires explicit operator or assistant action in future AL Game steps.

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_REPLAY_SESSION_V0_1",
  "status": "DRAFT_NON_CANONICAL",
  "authority": false,
  "membrane": "HOLDS"
}
```

End of V0.1 draft.
