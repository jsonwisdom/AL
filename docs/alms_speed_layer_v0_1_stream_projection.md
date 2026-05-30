# ALMS Speed Layer — Stream Projection (V0.1 Draft)

**Status:** DRAFT  
**Authority:** false  
**Membrane:** HOLDS  
**Advancement:** NONE  
**Sealing:** NONE  
**Hashing:** NONE  
**Receipts:** NONE  
**Epoch:** UNCHANGED

---

## Purpose

Define the V0.1 stream projection rules for the ALMS speed layer.

Projection determines how bound streams are transformed into deterministic, replay-safe outputs suitable for multi-stream analysis.

This document is non-canonical and does not modify governance lineage.

---

## Constraints

- No authority elevation.
- No canonicalization.
- No epoch creation.
- No sealing.
- No invented hashes.
- No ghost references.
- Must be replay-safe.
- Must be committed through GitHub direct with a real commit SHA when assistant-authored.

---

## Projection Model (Draft)

Each projection must conform to the following structure:

### 1. Projection ID

- Deterministic, human-readable identifier.
- Must be unique within the projection table.
- No hashes, UUIDs, or opaque tokens.

### 2. Binding Reference

- Must reference a valid entry in the Stream Binding table.
- Must use real GitHub commit SHA.
- Must reference an existing path in the repository.

### 3. Projection Type

- `DIRECT` — byte-level passthrough.
- `STRUCTURED` — deterministic structural transformation.
- `META` — relational or contextual projection.

### 4. Projection Envelope

- Deterministic only.
- No new authority.
- No hashes.
- No receipts.
- No lineage advancement.

### 5. Replay Discipline

- Every projection must be reproducible from GitHub-pinned bytes.
- No assistant-invented state.
- Operator-reported state is allowed but non-authoritative.

---

## Projection Table (Draft)

| Field | Description | Constraints |
|---|---|---|
| `projection_id` | Deterministic identifier | Must be unique |
| `binding_id` | Stream Binding reference | Must exist |
| `source_sha` | GitHub commit SHA | Must be real |
| `projection_type` | DIRECT / STRUCTURED / META | Must match envelope |
| `projection_rule` | Deterministic projection description | Optional, no authority |
| `notes` | Optional contextual notes | No lineage impact |

---

## Initial V0.1 Projections

No projections are defined in this V0.1 draft.

Population of the projection table requires explicit operator or assistant action in future AL Game steps.

---

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_STREAM_PROJECTION_V0_1",
  "status": "DRAFT_NON_CANONICAL",
  "authority": false,
  "membrane": "HOLDS",
  "advancement": "NONE",
  "sealing": "NONE",
  "epoch": "UNCHANGED"
}
```

---

End of V0.1 draft.
