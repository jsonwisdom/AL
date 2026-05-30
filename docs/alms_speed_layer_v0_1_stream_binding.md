# ALMS Speed Layer — Stream Binding (V0.1 Draft)

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

Define the V0.1 stream binding rules for the ALMS speed layer.

Binding determines how registered streams attach to observation contexts defined by the observer matrix.

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

## Binding Model (Draft)

Each binding event must conform to the following structure:

### 1. Binding ID

- Deterministic, human-readable identifier.
- Must be unique within the binding table.
- No hashes, UUIDs, or opaque tokens.

### 2. Stream Reference

- Must reference a valid entry in the Stream Registry.
- Must use real GitHub commit SHA.
- Must reference an existing path in the repository.

### 3. Observer Context

- Must reference a valid observation type from the Observer Matrix.
- Must not introduce new observation types.
- Must not modify existing observation rules.

### 4. Binding Envelope

- Deterministic only.
- No new authority.
- No hashes.
- No receipts.
- No lineage advancement.

### 5. Replay Discipline

- Every binding must be reproducible from GitHub-pinned bytes.
- No assistant-invented state.
- Operator-reported state is allowed but non-authoritative.

---

## Binding Table (Draft)

| Field | Description | Constraints |
|---|---|---|
| `binding_id` | Deterministic identifier | Must be unique |
| `stream_id` | Stream Registry reference | Must exist |
| `source_sha` | GitHub commit SHA | Must be real |
| `observer_type` | STATIC / DYNAMIC / META | Must match matrix |
| `binding_rule` | Deterministic binding description | Optional, no authority |
| `notes` | Optional contextual notes | No lineage impact |

---

## Initial V0.1 Bindings

No bindings are defined in this V0.1 draft.

Population of the binding table requires explicit operator or assistant action in future AL Game steps.

---

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_STREAM_BINDING_V0_1",
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
