# ALMS Speed Layer — Replay Coordinator (V0.1 Draft)

**Status:** DRAFT
**Authority:** false
**Membrane:** HOLDS
**Advancement:** NONE
**Sealing:** NONE
**Hashing:** NONE
**Receipts:** NONE
**Epoch:** UNCHANGED

## Purpose

Define the V0.1 replay coordinator for the ALMS speed layer.
The coordinator governs how replay surfaces are scheduled, orchestrated, and grouped across deterministic replay workflows.

## Constraints

- No authority elevation
- No canonicalization
- No epoch creation
- No sealing
- No invented hashes
- No ghost references
- Must be replay-safe
- Must be GitHub-direct committed with a real SHA

## Coordination Model

### Coordinator ID
- Deterministic, human-readable identifier
- Unique within the coordinator table
- No hashes, UUIDs, or opaque identifiers

### Replay Surface Reference
- References a valid Projection Replay Surface entry
- Uses a real GitHub commit SHA
- References an existing repository path

### Coordination Envelope
- Deterministic only
- No external state
- No nondeterministic operations
- No authority advancement

### Coordination Types
- SCHEDULE — determine replay ordering
- GROUP — organize replay surfaces into sets
- DISPATCH — initiate replay workflows
- AGGREGATE — collect replay outputs

### Replay Discipline
- Reproducible from GitHub-pinned bytes
- No assistant-invented state
- Operator-reported state allowed but non-authoritative

## Replay Coordinator Table

| Field | Description | Constraints |
|---|---|---|
| coordinator_id | Deterministic identifier | Must be unique |
| replay_id | Replay Surface reference | Must exist |
| source_sha | GitHub commit SHA | Must be real |
| coordination_type | SCHEDULE / GROUP / DISPATCH / AGGREGATE | Must match envelope |
| coordination_rule | Deterministic coordination description | Optional |
| notes | Optional contextual notes | No lineage impact |

## Initial V0.1 Coordinators

No coordinators are defined in the V0.1 draft.
Population requires explicit operator or assistant action in future AL Game steps.

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_REPLAY_COORDINATOR_V0_1",
  "status": "DRAFT_NON_CANONICAL",
  "authority": false,
  "membrane": "HOLDS"
}
```

End of V0.1 draft.
