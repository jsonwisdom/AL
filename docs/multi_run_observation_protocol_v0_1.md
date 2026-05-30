# MULTI_RUN_OBSERVATION_PROTOCOL_V0_1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/multi_run_observation_protocol_v0_1.md`  
**Status:** Active / Multi-Run Comparison Observation Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Define observation-only comparison surfaces across two or more replay runs.

Comparison is observation.

Comparison is not evaluation.

Multi-run observation does not imply validation, legitimacy, authority, correctness, causation, or truth.

---

## Core Invariant

```text
Comparison is observation.
Comparison is not evaluation.
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

Multi-run observation requires at least two replay run references.

If fewer than two runs exist, the protocol returns `BLOCKED`.

---

## Comparison Structure

```json
{
  "comparison_id": "MRUN-20260530-001",
  "run_refs": [
    "RUN-20260530-001",
    "RUN-20260530-002"
  ],
  "comparison_status": "OBSERVED_ONLY",
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

## Allowed Results

- `ADDED_REFS`
- `REMOVED_REFS`
- `SHARED_REFS`
- `CHANGED_REFS`
- `UNAVAILABLE`

---

## Forbidden Results

- `CORRECT`
- `INCORRECT`
- `VALID`
- `INVALID`
- `TRUE`
- `FALSE`
- `AUTHORITATIVE`
- `TRUSTED`

---

## Blocked Conditions

The protocol blocks when:

- fewer than two replay runs exist
- a run reference is missing
- output observation is unavailable
- evaluation is attempted
- authority claim is attempted
- validation claim is attempted

Blocked status does not imply failure, error, guilt, or invalidity.

Blocked means observation cannot proceed under the current membrane.

---

## Safety Rules

- No synthetic runs.
- No fake comparison.
- No recommendation engine.
- No trust scoring.
- No correctness scoring.
- No automatic action.
- Results are references only.

---

## Integration

Builds on:

- `REPLAY_RUN_PROTOCOL_V0_1`
- `REPLAY_OUTPUT_OBSERVATION_PROTOCOL_V0_1`
- `REPLAY_GRAPH_SNAPSHOT_PROTOCOL_V0_1`
- `REPLAY_EVIDENCE_BINDING_PROTOCOL_V0_1`

---

## Status Object

```json
{
  "artifact": "MULTI_RUN_OBSERVATION_PROTOCOL_V0_1",
  "status": "ACTIVE",
  "authority": false,
  "membrane": "HOLDS"
}
```
