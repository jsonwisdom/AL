# Temporal Snapshot Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/temporal_snapshot_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Read-Only Time Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Temporal Snapshot Protocol v0.1 defines how replay state, lineage, drift, witness clusters, active branches, archived branches, pending decisions, and collision manifests are captured at a point in time without changing state.

A snapshot records state.

A snapshot does not create state.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "TEMPORAL_SNAPSHOT_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Snapshot:** complete point-in-time capture of replay state.
- **Time-machine layer:** Jay-only, read-only inspection of prior state.
- **Atomic read:** capture without state changes during capture.
- **Snapshot scope:** fields captured for inspection and trend analysis.

A snapshot is not:

- a fork
- a lineage node
- a branch
- a decision
- a rollback point
- a source of authority

---

## Snapshot Schema

```yaml
temporal_snapshot_v0_1:
  snapshot_id: UUID
  timestamp: ISO_8601
  parent_lineage_id: lineage_id
  active_branches:
    - branch_id
    - head_node
  archived_branches:
    - branch_id
    - archive_timestamp
  drift_meter_readings:
    - branch_id
    - entropy
    - trend
    - threshold
  witness_clusters:
    - cluster_id
    - receipt_ids
  pending_decisions:
    - decision_id
  justification_receipt_log:
    - latest_N_receipts
  membrane_state: HOLDS | RELEASES | suspended
  collision_manifest:
    - unresolved_collision_id
```

---

## Capture Rules

- Snapshot may be triggered by Operator command.
- Snapshot may be triggered automatically at milestone intervals.
- No state changes occur during capture.
- Snapshot capture is an atomic read.
- Snapshot does not freeze live replay.
- Replay continues on active branches after capture.

---

## Time-Machine Inspection

Jay-only, read-only inspection may:

- load snapshot T0, T1, T2 independently
- compare drift delta between snapshots
- replay decision lineage up to snapshot point
- inspect witness cluster evolution over time
- reconstruct collision timing before and after fork

Inspection may not:

- resume from snapshot as active state
- inject decisions into past snapshots
- branch from snapshot
- mutate snapshot contents
- alter witness proposals in snapshots
- back-propagate drift readings

---

## Restrictions

Strictly forbidden:

- decision injection into past snapshots
- snapshot branching
- witness proposal modification in snapshots
- drift meter back-propagation
- snapshot-as-authority promotion
- snapshot-as-proof promotion

---

## Integration

- Snapshots feed historical entropy curves.
- Snapshots enable collision reconstruction.
- Snapshots preserve visibility into lineage state over time.
- Snapshots do not replace justification receipts.
- Justification receipts remain decision-source records.
- Lineage Graph Protocol remains ancestry source.
- Drift Meter remains observation-only.

---

## Status

```json
{
  "artifact": "TEMPORAL_SNAPSHOT_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "snapshot_effect": "READ_ONLY_CAPTURE",
  "authority": false,
  "membrane": "HOLDS"
}
```
