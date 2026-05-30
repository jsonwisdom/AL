# ALMS Speed Layer — Projection Runtime (V0.1 Draft)

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

Define the V0.1 projection runtime for the ALMS speed layer.

The runtime specifies how projections are executed, observed, and replayed in a deterministic, multi-stream environment.

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

## Runtime Model (Draft)

Each projection execution must conform to the following structure:

### 1. Runtime ID

- Deterministic, human-readable identifier.
- Must be unique within the runtime table.
- No hashes, UUIDs, or opaque tokens.

### 2. Projection Reference

- Must reference a valid entry in the Projection Catalog.
- Must use real GitHub commit SHA.
- Must reference an existing path in the repository.

### 3. Execution Envelope

- Deterministic only.
- No external state.
- No nondeterministic operations.
- No authority advancement.

### 4. Runtime Types

- `EVAL` — direct evaluation of projection rules.
- `STRUCTURE` — structural normalization.
- `META` — contextual or relational runtime behavior.

### 5. Replay Discipline

- Every runtime execution must be reproducible from GitHub-pinned bytes.
- No assistant-invented state.
- Operator-reported state is allowed but non-authoritative.

---

## Runtime Table (Draft)

| Field | Description | Constraints |
|---|---|---|
| `runtime_id` | Deterministic identifier | Must be unique |
| `projection_id` | Projection Catalog reference | Must exist |
| `source_sha` | GitHub commit SHA | Must be real |
| `runtime_type` | EVAL / STRUCTURE / META | Must match envelope |
| `runtime_rule` | Deterministic runtime description | Optional, no authority |
| `notes` | Optional contextual notes | No lineage impact |

---

## Initial V0.1 Runtime

No runtime entries are defined in this V0.1 draft.

Population of the runtime table requires explicit operator or assistant action in future AL Game steps.

---

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_PROJECTION_RUNTIME_V0_1",
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
