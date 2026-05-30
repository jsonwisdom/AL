# REPLAY_GRAPH_QUERY_PROTOCOL_V0_1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/replay_graph_query_protocol_v0_1.md`  
**Status:** Active / Graph Traversal Observation Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Define inert graph query surfaces over:

- Receipts
- Evidence bindings
- Validation observations
- Binding lineage

Traversal is observation only.

Queries do not imply validation, legitimacy, authority, correctness, causation, or truth.

---

## Core Invariant

```text
Traversal is observation.
Traversal is not interpretation.
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

## Query Structure

```json
{
  "query_id": "QRY-20260530-001",
  "traversal_type": "LINEAGE | EVIDENCE | VALIDATION_REF | FULL_GRAPH",
  "start_node": "AL-R-001",
  "direction": "FORWARD | BACKWARD | BIDIRECTIONAL",
  "depth": 5,
  "filters": {
    "binding_status": ["OBSERVED_ONLY"],
    "timestamp_range": ["2026-05-01", "2026-05-30"]
  },
  "result_mode": "REFERENCES_ONLY",
  "authority": false,
  "timestamp": "2026-05-30T08:36:00Z",
  "operator": "ZeroCool"
}
```

---

## Traversal Modes

| Mode | Meaning |
|---|---|
| `LINEAGE` | Follow binding parent and child chains. |
| `EVIDENCE` | Walk evidence references attached to receipts. |
| `VALIDATION_REF` | Surface linked validation observations. |
| `FULL_GRAPH` | Return connected subgraph of all referenced nodes. |

---

## Graph Nodes and Edges

Nodes may include:

- receipts
- evidence references
- validation observations
- bindings

Edges are referential only:

- `references`
- `bound_to`
- `observed_in`
- `parent_of`
- `child_of`

Edges carry no semantic weight.

Edges do not imply causation.

---

## Query Results Format

```json
{
  "query_id": "QRY-20260530-001",
  "nodes": [
    "AL-R-001",
    "EV-20260530-ab12cd34"
  ],
  "edges": [
    {
      "from": "AL-R-001",
      "to": "EV-20260530-ab12cd34",
      "type": "evidence_ref"
    }
  ],
  "binding_status": "OBSERVED_ONLY",
  "authority": false
}
```

---

## Safety Rules

- All results return raw references only.
- No evaluation is attached.
- No scoring is attached.
- No validation is attached.
- Queries are logged in binding history but create no authority.
- `result_mode: REFERENCES_ONLY` is default.
- Data embedding is avoided unless separately authorized by Operator receipt.

---

## Separation Rules

Graph queries never touch:

- validation authority
- legitimacy
- admission
- authority
- correctness
- causation
- truth

Traversal is not interpretation.

---

## Integration Points

- Builds on `REPLAY_EVIDENCE_BINDING_PROTOCOL_V0_1`.
- Feeds replay engine with observable topology.
- Precedes graph snapshot and archival query layers.
- Complements Dependency Graph Query Protocol without replacing dependency ordering.

---

## Status

```json
{
  "artifact": "REPLAY_GRAPH_QUERY_PROTOCOL_V0_1",
  "status": "ACTIVE",
  "authority": false,
  "membrane": "HOLDS"
}
```
