# ALMS Speed Layer — V0.1 (Draft, Non-Canonical)

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

Define the initial observation and transformation rules for the ALMS (Alabama Layered Multi-Stream) speed layer.

This document is a non-canonical draft surface used for AL Game iteration and does not modify any governance lineage.

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

## V0.1 Scope

- Define the speed-layer observation envelope.
- Define allowed transformations.
- Define the non-canonical witness pattern.
- Define replay discipline.
- Define the operator/assistant boundary for this layer.

---

## Observation Envelope (Draft)

1. Inputs must be present in the repository.
2. Inputs must be commit-pinned.
3. No external or ephemeral surfaces allowed.
4. No Cloud Shell state allowed unless operator-reported.

---

## Transformation Rules (Draft)

1. Transformations must be deterministic.
2. Transformations must not introduce new authority.
3. Transformations must not create hashes.
4. Transformations must not create receipts.
5. Transformations must not reference uncommitted artifacts.

---

## Replay Discipline

- Every transformation must be reproducible from GitHub-pinned bytes.
- No assistant-invented state.
- No assistant-invented lineage.
- Operator-reported state is allowed but non-authoritative.

---

## Boundary Rules

- Assistant commits require real GitHub SHA.
- Operator commits require operator-reported receipt.
- Membrane must remain intact.
- Authority must remain false.

---

## Status Object

```json
{
  "artifact": "ALMS_SPEED_LAYER_V0_1",
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
