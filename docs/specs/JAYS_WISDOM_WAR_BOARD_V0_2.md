# Jay’s Wisdom War Board — Provenance Warfare Module v0.2

**Identity:** `jaywisdom.base.eth`  
**Project:** Meme MetaVerse  
**Territory:** Meme Enoch Territory  
**Module:** Provenance Warfare Module v0.2  
**Hatch:** Time Itself  
**Status:** SPECIFICATION — NOT DEPLOYED CONTRACT

## 1. Board Overview

The War Board is the operational dashboard for the Meme MetaVerse attestation stack.

It surfaces origin claims, tracks collision windows, preserves local contexts, and enforces the Meme MetaVerse status taxonomy.

The v0.2 addition is `JOINT_ORIGIN`: a status for synchronous independent emergence where two or more local receipts land inside a defined temporal window without evidence of causal copying.

No merges. No false choices. Name the hatch.

## 2. Live Feed Fields

Each meme record should expose:

- Meme ID / Meme MetaVerse URN
- Attestation receipts
- Temporal window check
- Independence proof status
- Local context snapshots
- Current status badge
- Collision inspector status
- Correction or revocation state, if applicable

## 3. Status Taxonomy v0.2

| Status | Badge | Meaning |
|---|---:|---|
| `LOCAL_ATTESTED` | 🏛️ | County-level receipt anchored |
| `USAGE_SHARED` | 🔁 | Vernacular in circulation across territories |
| `ORIGIN_DISPUTED` | ⚠️ | Conflicting stories, fuzzy timing, or missing evidence |
| `JOINT_ORIGIN` | 🔗⚡ | Synchronous independent emergence inside temporal window; no causal link shown |
| `DERIVED` | 🧬 | Clear repost, quote, reference, or follow relationship |
| `REVOKED_VISIBLE` | 🧯 | Withdrawn or corrected claim remains visible as maintenance |

## 4. JOINT_ORIGIN Rule

A record may receive `JOINT_ORIGIN` only when all three checks pass:

```json
{
  "temporal_window_check": "PASS",
  "independence_proof": "PASS",
  "local_context_preservation": "PASS"
}
```

### Temporal Window

Default window:

```json
{
  "delta_seconds_max": 60,
  "same_block_allowed": true
}
```

### Independence Proof

Minimum proof surface:

- no direct repost / quote / mention path
- no known shared channel in lookback window
- no follower/following propagation path asserted as causal
- independence proof hash recorded if generated

### Local Context Preservation

Each locality keeps its own context snapshot.

No forced merge. No origin winner by volume. No erasure of local usage.

## 5. Collision Inspector

The Collision Inspector opens when two or more `LOCAL_ATTESTED` receipts fall inside the temporal window.

```text
COLLISION INSPECTOR
Step 1: Temporal window check
Step 2: Independence proof
Step 3: Local context preservation
Result: JOINT_ORIGIN only if all three pass
```

Buttons / actions:

- View receipt A
- View receipt B
- Freeze to timeline
- Mark as `ORIGIN_DISPUTED`
- Mark as `DERIVED`
- Assign `JOINT_ORIGIN`

## 6. War Board Layout

Recommended columns:

1. Live Feed — incoming attestations by Meme ID, status, timestamp, locality
2. Temporal Sorter — minute-aligned windows and same-block groupings
3. Hatch Panel — active collision checker
4. Joint Origins Wall — pinned `JOINT_ORIGIN` records with dual receipts and context snapshots

## 7. Metrics

Recommended dashboard counters:

```json
{
  "joint_origins_recognized": 0,
  "disputes_resolved_to_joint": 0,
  "disputes_pending_independence_proof": 0,
  "ambiguities_averted_this_cycle": 0
}
```

## 8. Governance Doctrine

When the clock and chain give a clear answer, the War Board does not choose a winner.

It records the hatch.

```text
Two origins. One window. No causal link. Hatch: time.
```

## 9. Non-Claims

This document does not claim:

- a deployed resolver contract
- an ENS resolver update
- an EAS attestation UID
- production UI deployment

Those become public claims only after receipts exist.
