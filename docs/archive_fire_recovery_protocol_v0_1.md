# Archive Fire Recovery Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/archive_fire_recovery_protocol_v0_1.md`  
**Status:** Draft / Simulation Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## 1. Purpose

Archive Fire Recovery Protocol v0.1 defines a replay-native recovery mode for cases where receipts, archives, or canonical records are missing, damaged, or destroyed.

The goal is not to restore truth by assertion.

The goal is to reconstruct lineage without inventing certainty.

The system preserves the boundary between:

- known
- claimed
- remembered
- reconstructed
- replayable
- tainted

This protocol is simulation-only and does not grant authority to any actor, gate, witness, or recovered artifact.

---

## 2. Protocol Object

```json
{
  "protocol": "ARCHIVE_FIRE_RECOVERY_V0_1",
  "simulation": true,
  "authority": false,
  "starting_condition": "receipts_missing_or_destroyed",
  "goal": "reconstruct_lineage_without_inventing_certainty"
}
```

---

## 3. Recovery States — The Seven Ashes

Each recovery state is a category, not a truth claim.

```json
{
  "states": [
    "ASH",
    "FRAGMENT",
    "CLAIM",
    "CANDIDATE_RECEIPT",
    "PARTIAL_LINEAGE",
    "REPLAYABLE_LINEAGE",
    "TAINTED_LINEAGE"
  ]
}
```

### State Definitions

| State | Meaning |
|---|---|
| `ASH` | No usable information remains. |
| `FRAGMENT` | Partial artifact exists, but no verified hash or lineage exists. |
| `CLAIM` | Human memory, report, or assertion. Unverified by default. |
| `CANDIDATE_RECEIPT` | Fragment plus hash or metadata match, still pending replay. |
| `PARTIAL_LINEAGE` | Some ancestry reconstructed, but not fully replayable. |
| `REPLAYABLE_LINEAGE` | Deterministic ancestry can be reconstructed and replayed. |
| `TAINTED_LINEAGE` | Reconstruction fails replay or contains unresolved contradiction. |

---

## 4. Core Rule — The Three Prohibitions

```text
Do not upgrade memory into receipt.
Do not upgrade claim into replay.
Do not upgrade reconstruction into certainty.
```

These prohibitions prevent:

- mythologizing
- drift
- false continuity
- narrative laundering
- epistemic fraud
- silent category promotion

---

## 5. Player Actions — Recovery Toolkit

| Command | Purpose |
|---|---|
| `GATHER_FRAGMENT` | Collect surviving artifact. |
| `LABEL_CLAIM` | Mark memory as unverified. |
| `MATCH_HASH` | Test fragment against known hash. |
| `REBUILD_LINEAGE` | Connect fragments cautiously. |
| `REQUEST_WITNESS` | Add human report as testimony, not proof. |
| `REPLAY_BRANCH` | Test reconstruction. |
| `TAINT_BRANCH` | Mark unreplayable path. |

Caution is an intentional mechanic. The player wins by preserving categories, not by forcing certainty.

---

## 6. Victory Condition — Replayable Lineage

```json
{
  "win_condition": "REPLAYABLE_LINEAGE",
  "required": [
    "at_least_one_surviving_anchor",
    "explicit_uncertainty_markers",
    "no_silent_category_promotion",
    "replay_test_passed"
  ]
}
```

Victory after archive loss means replayability, not consensus.

---

## 7. Failure Condition — False Restoration

```json
{
  "fail_condition": "FALSE_RESTORATION",
  "trigger": "system_claims_certainty_after_archive_loss",
  "penalty": "MAX_DRIFT"
}
```

False restoration occurs when the system claims certainty after the archive boundary has failed.

Examples include:

- forging continuity
- inventing ancestors
- treating memory as proof
- treating claims as canon
- asserting replay without reconstruction

Penalty: `MAX_DRIFT`.

---

## 8. Observer Doctrine

The Observer does not restore the past.

The Observer restores the boundary between categories.

The Observer may:

- observe
- log
- collect fragments
- request receipts
- request witnesses
- rebuild candidate lineage
- replay branches
- taint unreplayable branches

The Observer may not:

- create truth by assertion
- promote claims into receipts
- promote memory into evidence
- promote reconstruction into certainty
- grant authority

---

## 9. Game Layer Interpretation

Archive Fire mode is a civic recovery dungeon.

Players enter with fragments, memories, claims, and broken lineage.

Every recovery path must preserve uncertainty until replay succeeds.

The core joystick question remains:

```text
Can this be replayed?
```

If yes, lineage may advance.

If no, the branch remains partial or tainted.

---

## 10. Status

```json
{
  "artifact": "ARCHIVE_FIRE_RECOVERY_PROTOCOL_V0_1",
  "simulation": true,
  "authority": false,
  "membrane": "HOLDS",
  "category_promotion": "FORBIDDEN_WITHOUT_REPLAY",
  "status": "DRAFT_CREATED"
}
```
