# COMPARISON_HISTORY_PROTOCOL_V0_1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/comparison_history_protocol_v0_1.md`  
**Status:** Active / Comparison History Observation Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Record observation-only history of multi-run comparisons.

History is observation.

History is not evaluation.

History does not imply validation, legitimacy, authority, correctness, causation, or truth.

---

## Core Invariant

```text
History is observation.
History is not evaluation.
```

---

## Observer-Operator

```json
{
  "operator": "JAY_WISDOM_ZEROCOOL",
  "role": "OBSERVER_OPERATOR",
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Minimum Requirement

Comparison history requires at least one completed multi-run comparison.

If no comparisons exist, the protocol returns `BLOCKED`.

---

## History Entry Structure

```json
{
  "history_id": "HIST-20260530-001",
  "comparison_id": "MRUN-20260530-001",
  "timestamp": "2026-05-30T00:00:00Z",
  "run_refs": [
    "RUN-20260530-001",
    "RUN-20260530-002"
  ],
  "added_refs": [],
  "removed_refs": [],
  "shared_refs": [],
  "changed_refs": [],
  "snapshot_refs": [],
  "authority": false,
  "operator": "ZeroCool"
}
```

---

## Allowed Fields

- `added_refs`
- `removed_refs`
- `shared_refs`
- `changed_refs`
- `snapshot_refs`
- `unavailable`

---

## Forbidden Fields

- `correct`
- `incorrect`
- `valid`
- `invalid`
- `true`
- `false`
- `authoritative`
- `trusted`

---

## Blocked Conditions

The protocol blocks when:

- no comparison entries exist
- comparison reference is missing
- comparison output is unavailable
- evaluation is attempted
- authority claim is attempted
- validation claim is attempted

Blocked status does not imply failure, error, guilt, or invalidity.

Blocked means history observation cannot proceed under the current membrane.

---

## Safety Rules

- No synthetic comparisons.
- No fake history.
- No trust scoring.
- No correctness scoring.
- No automatic action.
- Results are references only.

---

## Integration

Builds on:

- `MULTI_RUN_OBSERVATION_PROTOCOL_V0_1`
- `REPLAY_RUN_PROTOCOL_V0_1`
- `REPLAY_OUTPUT_OBSERVATION_PROTOCOL_V0_1`
- `REPLAY_GRAPH_SNAPSHOT_PROTOCOL_V0_1`
- `REPLAY_EVIDENCE_BINDING_PROTOCOL_V0_1`

---

## Status Object

```json
{
  "artifact": "COMPARISON_HISTORY_PROTOCOL_V0_1",
  "status": "ACTIVE",
  "authority": false,
  "membrane": "HOLDS"
}
```
