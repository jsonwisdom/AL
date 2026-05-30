# ALMS Speed Layer — Observer Matrix (V0.1 Draft)

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

Define the V0.1 observer matrix for the ALMS speed layer.

This matrix specifies how observations are structured and replayed across multiple input streams.

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

## Observer Matrix Structure (Draft)

Each observation in the speed layer must conform to the following structure:

### 1. Source Surface

- Must be a GitHub-pinned artifact.
- Must exist at a real commit SHA.
- No ephemeral or external surfaces allowed.

### 2. Observation Type

- `STATIC` — byte-level, no transformation.
- `DYNAMIC` — deterministic transformation allowed.
- `META` — structural or relational observation.

### 3. Replay Discipline

- Every observation must be reproducible from GitHub-pinned bytes.
- No assistant-invented state.
- Operator-reported state is allowed but non-authoritative.

### 4. Transformation Envelope

- Deterministic only.
- No new authority.
- No hashes.
- No receipts.
- No lineage advancement.

### 5. Boundary Rules

- Assistant commits require real GitHub SHA.
- Operator commits require operator-reported receipt.
- Membrane must remain intact.
- Authority must remain false.

---

## Observer Matrix Table (Draft)

| Field | Description | Constraints |
|---|---|---|
| `source_sha` | GitHub commit SHA of observed artifact | Must be real, no invention |
| `path` | Path to observed artifact | Must exist in repo |
| `type` | STATIC / DYNAMIC / META | Must match envelope |
| `transform` | Deterministic transformation description | Optional, no authority |
| `replay_rule` | How to reproduce observation | Must be deterministic |
| `notes` | Optional contextual notes | No lineage impact |

---

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_OBSERVER_MATRIX_V0_1",
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
