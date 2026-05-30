# ALMS Speed Layer — Projection Catalog (V0.1 Draft)

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

Define the V0.1 projection catalog for the ALMS speed layer.

The catalog enumerates all available projections, their deterministic structure, and their replay-safe characteristics.

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

## Catalog Model (Draft)

Each catalog entry must conform to the following structure:

### 1. Catalog ID

- Deterministic, human-readable identifier.
- Must be unique within the catalog.
- No hashes, UUIDs, or opaque tokens.

### 2. Projection Reference

- Must reference a valid entry in the Stream Projection table.
- Must use real GitHub commit SHA.
- Must reference an existing path in the repository.

### 3. Catalog Type

- `PRIMARY` — core projection.
- `DERIVED` — deterministic transformation of a primary projection.
- `META` — relational or contextual catalog entry.

### 4. Catalog Envelope

- Deterministic only.
- No new authority.
- No hashes.
- No receipts.
- No lineage advancement.

### 5. Replay Discipline

- Every catalog entry must be reproducible from GitHub-pinned bytes.
- No assistant-invented state.
- Operator-reported state is allowed but non-authoritative.

---

## Projection Catalog Table (Draft)

| Field | Description | Constraints |
|---|---|---|
| `catalog_id` | Deterministic identifier | Must be unique |
| `projection_id` | Stream Projection reference | Must exist |
| `source_sha` | GitHub commit SHA | Must be real |
| `catalog_type` | PRIMARY / DERIVED / META | Must match envelope |
| `catalog_rule` | Deterministic catalog description | Optional, no authority |
| `notes` | Optional contextual notes | No lineage impact |

---

## Initial V0.1 Catalog

No catalog entries are defined in this V0.1 draft.

Population of the catalog requires explicit operator or assistant action in future AL Game steps.

---

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_PROJECTION_CATALOG_V0_1",
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
