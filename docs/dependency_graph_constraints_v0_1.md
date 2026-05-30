# Dependency Graph Constraints v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/dependency_graph_constraints_v0_1.md`  
**Status:** Integration Block / Graph Constraint Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Node Receipt

```json
{
  "node_id": "DEPENDENCY_PROTOCOL_V0_1::NODE_03",
  "artifact": "DEPENDENCY_GRAPH_CONSTRAINTS_V0_1",
  "prev": "DEPENDENCY_PROTOCOL_V0_1::NODE_02",
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Purpose

Dependency Graph Constraints v0.1 defines replay-safe constraints for dependency graphs in the Alabama-ALMS speed-layer.

Dependencies may form chains.

Dependencies may not form paradoxes.

Dependency constraints define ordering safety only.

They do not define truth, causation, admission, legitimacy, or authority.

---

## Integration Block With STATE_TRANSITION_MEMBRANE_V0_1

Dependency graph changes are treated as governed state transitions.

Before any dependency graph change commits, it must pass the following checks:

1. **Operator Pin Check** — `operator_pin` must match `JAY_WISDOM_12`.
2. **Receipt Lifecycle Check** — graph change must have a receipt state at least `RECORDED_LINK` or `DEPENDENCY_RECORD`.
3. **State Transition Membrane Check** — mutation type must be allowed: `ADD_DEPENDENCY`, `UPDATE_DEPENDENCY`, or `DEPRECATE_DEPENDENCY`.
4. **Graph Constraint Check** — no self-dependency, immediate cycle, or unbounded block chain.
5. **Drift Meter Check** — graph churn must remain below active threshold for current meter state.

Forbidden graph changes are auto-tainted and must not partially commit.

---

## Concrete Root Nodes For Alabama-ALMS Speed-Layer

```yaml
root_nodes:
  - id: ROOT_ALMS_SPEED_LAYER
    type: replay_root
    description: Alabama-ALMS speed-layer reconstruction root
    scope: IN_SCOPE

  - id: ROOT_OPERATOR_JAY
    type: operator_root
    description: Jay Wisdom / ZeroCool Observer-Operator pin
    scope: IN_SCOPE

  - id: ROOT_MEMBRANE
    type: membrane_root
    description: Authority false and membrane HOLDS boundary
    scope: IN_SCOPE

  - id: ROOT_RECEIPT_LIFECYCLE
    type: lifecycle_root
    description: Replay Receipt Lifecycle governs strengthening through replay only
    scope: IN_SCOPE

  - id: ROOT_DEPENDENCY_GRAPH
    type: graph_root
    description: Dependency ordering graph for replay sequence
    scope: IN_SCOPE
```

---

## Initial Dependency Set

```yaml
initial_dependencies:
  - id: DEP-001
    dependent_id: ROOT_DEPENDENCY_GRAPH
    dependency_id: ROOT_ALMS_SPEED_LAYER
    ordering_type: REQUIRES
    operator_pin: JAY_WISDOM_12

  - id: DEP-002
    dependent_id: ROOT_DEPENDENCY_GRAPH
    dependency_id: ROOT_OPERATOR_JAY
    ordering_type: REQUIRES
    operator_pin: JAY_WISDOM_12

  - id: DEP-003
    dependent_id: ROOT_DEPENDENCY_GRAPH
    dependency_id: ROOT_MEMBRANE
    ordering_type: REQUIRES
    operator_pin: JAY_WISDOM_12

  - id: DEP-004
    dependent_id: ROOT_DEPENDENCY_GRAPH
    dependency_id: ROOT_RECEIPT_LIFECYCLE
    ordering_type: REQUIRES
    operator_pin: JAY_WISDOM_12

  - id: DEP-005
    dependent_id: ROOT_RECEIPT_LIFECYCLE
    dependency_id: ROOT_OPERATOR_JAY
    ordering_type: REQUIRES
    operator_pin: JAY_WISDOM_12

  - id: DEP-006
    dependent_id: ROOT_RECEIPT_LIFECYCLE
    dependency_id: ROOT_MEMBRANE
    ordering_type: REQUIRES
    operator_pin: JAY_WISDOM_12
```

These dependencies define replay ordering only.

They do not assert causation, correctness, or authority.

---

## Graph Constraint Rules

### NO_SELF_DEPENDENCY

An object may not depend on itself.

```text
A REQUIRES A -> TAINTED
```

### NO_IMMEDIATE_CYCLE

Two objects may not mutually require or block each other in a direct loop.

```text
A REQUIRES B
B REQUIRES A
-> TAINTED
```

### NO_UNBOUNDED_BLOCK_CHAIN

A `BLOCKS` chain must have bounded inspection depth.

```text
A BLOCKS B
B BLOCKS C
C BLOCKS D
...
```

If chain exceeds active max depth, status becomes `DRIFT_REVIEW_REQUIRED`.

### MAX_GRAPH_DEPTH

Default maximum dependency graph depth:

```yaml
max_graph_depth: 7
```

Depth above 7 triggers AMBER drift state for review.

### WEAKEST_LINK_PROPAGATION

A dependency chain inherits the weakest non-proof state for replay readiness.

```text
If any required dependency is TAINTED, dependent replay readiness is HOLD.
If any required dependency is UNCLASSIFIED, dependent replay readiness is REVIEW.
If all required dependencies are REPLAY_CONFIRMED, dependent replay readiness may advance.
```

Weakest-link propagation is readiness guidance only.

It does not create legitimacy or authority.

---

## Drift Meter Thresholds For Graph Churn

```yaml
dependency_graph_churn_thresholds:
  GREEN:
    added_or_updated_dependencies_per_cycle: 0-3
    action: OBSERVE_ONLY

  AMBER:
    added_or_updated_dependencies_per_cycle: 4-7
    action: DRIFT_ACKNOWLEDGED_REQUIRED
    requirement: compensation_plan_within_72h

  RED:
    added_or_updated_dependencies_per_cycle: 8+
    action: DRIFT_REJECTED_REMEDIATION_REQUIRED
    requirement: rollback_target_or_boundary_reaffirmation
```

Thresholds create visibility only.

Thresholds do not trigger automatic action.

---

## Validation Checks

```yaml
dependency_graph_validation_v0_1:
  checks:
    - NO_SELF_DEPENDENCY
    - NO_IMMEDIATE_CYCLE
    - NO_UNBOUNDED_BLOCK_CHAIN
    - MAX_GRAPH_DEPTH
    - WEAKEST_LINK_PROPAGATION
    - OPERATOR_PIN_MATCH
    - MEMBRANE_HOLDS
    - AUTHORITY_FALSE
```

All checks are replay-observable.

Failed checks create drift and taint markers, not deletion.

---

## Status

```json
{
  "artifact": "DEPENDENCY_GRAPH_CONSTRAINTS_V0_1",
  "node_id": "DEPENDENCY_PROTOCOL_V0_1::NODE_03",
  "status": "COMMITTED",
  "authority": false,
  "membrane": "HOLDS"
}
```
