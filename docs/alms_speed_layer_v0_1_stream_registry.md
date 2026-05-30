# ALMS Speed Layer — Stream Registry (V0.1 Draft)

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

Define the V0.1 stream registry for the ALMS speed layer.

The registry specifies which streams may be observed, how they are identified, and how they participate in replay-safe multi-stream observation.

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

## Stream Registry Model (Draft)

Each stream entry must conform to the following structure:

### 1. Stream ID

- Deterministic, human-readable identifier.
- Must be unique within the registry.
- No hashes, UUIDs, or opaque tokens.

### 2. Source Surface

- Must be a GitHub-pinned artifact.
- Must exist at a real commit SHA.
- No ephemeral or external surfaces allowed.

### 3. Stream Type

- `TEXT` — markdown, plaintext, protocol surfaces.
- `STRUCT` — JSON, YAML, structured documents.
- `META` — relational or structural surfaces.

### 4. Validation Envelope

- Must be deterministic.
- Must not introduce authority.
- Must not require external state.
- Must be reproducible from GitHub-pinned bytes.

### 5. Replay Discipline

- Every stream must be replayable from its pinned source.
- No assistant-invented state.
- Operator-reported state is allowed but non-authoritative.

---

## Stream Registry Table (Draft)

| Field | Description | Constraints |
|---|---|---|
| `stream_id` | Deterministic identifier | Must be unique |
| `path` | Path to source artifact | Must exist in repo |
| `source_sha` | GitHub commit SHA | Must be real |
| `type` | TEXT / STRUCT / META | Must match envelope |
| `validation_rule` | Deterministic validation description | Optional, no authority |
| `notes` | Optional contextual notes | No lineage impact |

---

## Initial V0.1 Streams

No streams are registered in this V0.1 draft.

Population of the registry requires explicit operator or assistant action in future AL Game steps.

---

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_STREAM_REGISTRY_V0_1",
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
