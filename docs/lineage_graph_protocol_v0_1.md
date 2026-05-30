# Lineage Graph Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/lineage_graph_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Branch Ancestry Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Lineage Graph Protocol v0.1 defines parent, child, sibling, archived, reactivated, and fork relationships across replay branches.

Lineage is preserved even when activity stops.

Activity does not equal existence.

Archiving is not deletion.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "LINEAGE_GRAPH_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Active branch:** currently receiving Operator decisions and drift scans.
- **Archived branch:** frozen for decisions, preserved for replay and inspection.
- **Lineage:** immutable relationship record between decisions, branches, forks, archives, and reactivations.
- **Archive:** decision freeze, not deletion, deprecation, or wrongness.

---

## Example Graph

```text
root (genesis decision)
  ├── branch_A (active)
  │     ├── decision_1
  │     ├── decision_2
  │     └── (continues)
  ├── branch_B (archived)
  │     ├── decision_1
  │     ├── decision_3
  │     └── [ARCHIVED timestamp]
  └── branch_C (active — forked from branch_B pre-archive)
        ├── decision_1
        ├── decision_3
        ├── decision_4
        └── (continues)
```

---

## Relationship Rules

- Branches know their direct parent.
- Branches know all forks from the same collision point as siblings.
- Archived branches retain full drift history.
- Archived branches retain full justification receipts.
- No branch is ancestor of another unless explicitly forked.
- No branch becomes wrong because another branch stays active.
- No branch becomes primary by default.

---

## Archival Rules

Archival is Operator-only.

Archival requires a justification receipt with a stated reason, such as:

```text
inspect only, no longer replaying
```

Archived branches may be reactivated.

Reactivation produces a new fork from the archive point.

Reactivation does not delete the archive.

The original archive remains frozen.

---

## Integration With Decision Collision Protocol

- Decision Collision Protocol creates branches.
- Lineage Graph Protocol tracks them.
- Collision resolution is never required.
- Branches may coexist indefinitely.
- Drift Meter aggregates entropy across active branches only.
- Archived branches remain static but inspectable.

---

## Query Surface

Jay-only, read-only query surface may:

- view full lineage graph
- filter by active or archived
- compare drift between any two branches, including archived branches
- trace decision ancestry for any node

The query surface must not:

- mark a branch correct
- select a winner
- collapse branches automatically
- mutate branch status
- promote archive to authority

---

## Collision Test Baseline

```json
{
  "collision_test": "READY",
  "collision_count": 0,
  "active_branches": 1,
  "archived_branches": 0,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Status

```json
{
  "artifact": "LINEAGE_GRAPH_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
