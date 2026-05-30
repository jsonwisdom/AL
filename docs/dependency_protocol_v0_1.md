# Dependency Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/dependency_protocol_v0_1.md`  
**Status:** Protocol Continuation / Ordering Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Node Receipt

```json
{
  "node_id": "DEPENDENCY_PROTOCOL_V0_1::NODE_02",
  "type": "protocol_continuation",
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Purpose

Dependency Protocol v0.1 defines replay ordering requirements between objects without implying truth, causation, legitimacy, admission, or authority.

Dependencies define ordering only.

Dependencies do not define truth.

Dependencies do not imply causation.

Dependencies do not create authority.

---

## Constitutional Position

Dependencies sit in the ordering layer, downstream of:

- Existence Gate
- Scope Classification Protocol
- Replay Receipt Lifecycle

and upstream of:

- Relationship Protocol
- State Transition Membrane
- Speed-Layer Reconstruction

Dependencies do not:

- create truth
- imply causation
- grant authority
- elevate legitimacy
- mutate admission

Dependencies only define ordering constraints inside the lattice.

---

## Dependency Object Contract

Every dependency declaration must include:

```yaml
dependency_v0_1:
  dependent_id: object_id
  dependency_id: object_id
  ordering_type: BEFORE | AFTER | BLOCKS | REQUIRES
  operator_pin: JAY_WISDOM_12
  timestamp: ISO_8601
  receipt_id: dependency_record_receipt_id
```

The `receipt_id` must bind to `REPLAY_RECEIPT_LIFECYCLE_V0_1` as a `DEPENDENCY_RECORD`.

This contract is immutable and replay-safe.

---

## Dependency Semantics

### Ordering Types

| Type | Meaning |
|---|---|
| `BEFORE` | Dependent must appear earlier in replay order. |
| `AFTER` | Dependent must appear later in replay order. |
| `BLOCKS` | Dependent cannot proceed until dependency resolves. |
| `REQUIRES` | Dependent cannot exist without dependency present. |

These are ordering semantics only.

They do not imply correctness, truth, or authority.

---

## Non-Implications

Dependencies never assert that the dependency is:

- valid
- legitimate
- authoritative
- true
- causal
- admitted

Dependencies only assert sequence.

---

## Dependency Lineage

Each dependency event is:

- immutable
- non-retroactive
- appended to lineage
- replayed exactly as recorded

Lineage structure:

```text
object -> dependency_event -> operator_pin -> timestamp
```

No inference.

No elevation.

No mutation.

---

## Reclassification and Mutation Rules

Dependencies may be:

- added via `ADD`
- updated via `UPDATE`

Dependencies may never be:

- silently removed
- rewritten
- collapsed
- inferred

All dependency mutations must pass:

- `STATE_TRANSITION_MEMBRANE_V0_1`
- Drift Meter scan

Dependency churn is an entropy signal.

Witness suggestions are advisory only.

---

## Query Interface

Dependency queries are read-only.

A dependency query returns:

- object_id
- dependency_graph_summary
- ordering_constraints
- lineage_summary

A dependency query must not return:

- mutation path
- inference
- authority
- causation claim
- admission recommendation

---

## Integration With Speed-Layer Reconstruction

During Alabama-ALMS speed-layer replay:

- dependencies define replay order
- dependencies do not define meaning
- dependencies do not define truth
- dependencies do not define authority

Replay uses dependencies as mechanical ordering only.

---

## Archival Logic

- Dependencies attached to `IN_SCOPE` objects persist until governed deprecation.
- Dependencies attached to `OUT_OF_SCOPE` objects may be externalized.
- Dependencies attached to `UNCLASSIFIED` objects trigger review after N cycles.

Archival is boundary hygiene.

Archival is not deletion.

---

## Forbidden Patterns

Forbidden dependency patterns are auto-tainted:

- dependency treated as proof
- dependency treated as causation
- dependency treated as authority
- dependency inferred without receipt
- dependency collapsed into relationship
- witness-authored dependency mutation
- dependency used to bypass scope boundary

---

## Status

```json
{
  "artifact": "DEPENDENCY_PROTOCOL_V0_1",
  "status": "COMMITTED",
  "authority": false,
  "membrane": "HOLDS"
}
```
