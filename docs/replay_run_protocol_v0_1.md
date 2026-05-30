# REPLAY_RUN_PROTOCOL_V0_1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/replay_run_protocol_v0_1.md`  
**Status:** Active / Replay Attempt Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Define inert replay run surfaces that execute:

- replay attempts using bound evidence, validation observations, and graph snapshots
- deterministic reconstruction attempts

A replay run is an attempt.

It is not proof.

Replay output does not imply truth, validation, legitimacy, authority, correctness, or causation.

---

## Core Invariant

```text
Attempt does not equal proof.
Observation does not equal truth.
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

## Run Structure

```json
{
  "run_id": "RUN-20260530-001",
  "snapshot_ref": "SNP-20260530-001",
  "query_ref": "QRY-20260530-001",
  "receipt_id": "AL-R-001",
  "run_status": "ATTEMPTED",
  "output_refs": ["OUT-20260530-xyz987"],
  "binding_status": "OBSERVED_ONLY",
  "authority": false,
  "timestamp": "2026-05-30T08:38:00Z",
  "operator": "ZeroCool",
  "lineage": ["AL-R-000"]
}
```

---

## Replay Run Execution

A replay run may trigger deterministic replay from captured snapshot plus bindings.

A replay run records attempt metadata and output references only.

It does not validate outputs.

It does not prove correctness.

---

## Run Types

| Run Type | Meaning |
|---|---|
| `LINEAGE_RUN` | Replay binding chain. |
| `EVIDENCE_RUN` | Reconstruct using attached evidence references. |
| `VALIDATION_REF_RUN` | Surface linked validation observation replay. |
| `FULL_GRAPH_RUN` | Complete topology replay attempt. |

---

## Output Format

```json
{
  "run_id": "RUN-20260530-001",
  "status": "ATTEMPTED",
  "output_refs": ["OUT-20260530-xyz987"],
  "observed_nodes": ["AL-R-001"],
  "observed_edges": [],
  "binding_status": "OBSERVED_ONLY",
  "authority": false
}
```

---

## Safety Rules

- Runs are attempts only.
- Runs are never authoritative.
- Output is raw references and traces.
- No semantic evaluation is attached.
- No truth claims are attached.
- All runs are logged in binding history.
- Authority field remains false.

---

## Run Status Values

Allowed run status values:

- `ATTEMPTED`
- `UNAVAILABLE`
- `ARCHIVED`

Not allowed in v0.1:

- `PROVEN`
- `VALIDATED`
- `TRUE`
- `AUTHORITATIVE`

---

## Integration Points

Builds on:

- `REPLAY_EVIDENCE_BINDING_PROTOCOL_V0_1`
- `REPLAY_GRAPH_QUERY_PROTOCOL_V0_1`
- `REPLAY_GRAPH_SNAPSHOT_PROTOCOL_V0_1`

Feeds observable replay surfaces for higher layers.

Precedes replay output observation and multi-run analysis.

---

## Separation Rules

Replay runs never touch:

- validation authority
- legitimacy
- admission
- authority
- correctness
- causation
- truth

Attempt is not proof.

Observation only.

---

## Status

```json
{
  "artifact": "REPLAY_RUN_PROTOCOL_V0_1",
  "status": "ACTIVE",
  "authority": false,
  "membrane": "HOLDS"
}
```
