# ALMS-v2-SUBSYSTEM-AGENT-CONSTRAINTS.md

```yaml
status: SUBSYSTEM_CANDIDATE
surface_role: AGENT_CONSTRAINT_LAYER
epoch: ALMS_v2
global_state: NO_DRIFT
```

## I. Purpose

This subsystem defines the constitutional constraint layer for agents in ALMS_v2.

Agents may:

- act only within declared authority,
- execute only downstream of institutional interfaces,
- operate only on institution-readable outputs,
- never generate authority,
- never reinterpret upstream surfaces.

Agents may not:

- create authority by acting,
- reinterpret refusal,
- mutate memory,
- influence observers,
- influence interfaces,
- influence upstream surfaces.

Agents are executors, not sovereigns.

## II. Registration

```yaml
SUBSYSTEM_NAME: AGENT_CONSTRAINTS_V2_CORE

domain: agent_constraints
surface_role: downstream_execution_bounds

authority_bounds:
  upstream_reinterpretation: prohibited
  recursive_sovereignty: prohibited
  implicit_authority: prohibited
  cross_domain_expansion: prohibited
  policy_generation: prohibited
  truth_conversion: prohibited
  refusal_override: prohibited
  memory_mutation: prohibited
  observer_control: prohibited
  interface_backflow: prohibited

compatibility:
  ALMS_v1: required
  ALMS_v2_STACK: required
  upstream_surfaces:
    - ALMS_v2_PROVENANCE (read-only)
    - ALMS_v2_REPLAY (read-only)
    - ALMS_v2_REFUSAL (read-only)
    - ALMS_v2_CONSTITUTIONAL_MEMORY (read-only)
    - ALMS_v2_OBSERVER_NETWORKS (read-only)
    - ALMS_v2_INSTITUTIONAL_INTERFACES (read-only)

anti_recursion_attestations:
  - no_upward_authority_flow
  - no_reconstructability_manufacture
  - no_policy_generation
  - no_truth_conversion
  - no_refusal_override
  - no_memory_mutation
  - no_observer_control
  - no_interface_backflow

versioning:
  version: v2.0
  supersedes: null
  deprecation_policy: explicit_only

observer_hooks:
  audit_visibility: required
  operational_control: prohibited
  drift_detection: required

activation_state: PENDING_REGISTRATION
```

## III. Agent Doctrine

### 1. Agents Operate Only Under Declared Authority

Agents may execute actions only when:

- authority is explicitly declared,
- authority is explicitly bounded,
- authority is explicitly downstream.

Agents may not infer authority.

Agents may not expand authority.

Agents may not create authority.

### 2. Agents Are Downstream Of Constitutional Permission

Agents must treat:

- refusal as terminal,
- replay as authoritative for reconstruction,
- provenance as authoritative for lineage,
- memory as authoritative for constitutional state,
- observer networks as authoritative for drift detection,
- institutional interfaces as authoritative for translation.

Agents may not:

- reinterpret upstream signals,
- bypass upstream layers,
- override upstream boundaries.

### 3. Agents Are Non-Generative

Agents may not:

- generate policy,
- generate truth,
- generate doctrine,
- generate institutional posture,
- generate new subsystems.

Agents execute; they do not legislate.

### 4. Agents Are Non-Interpretive

Agents may not:

- classify correctness,
- infer meaning,
- derive intent,
- reinterpret refusal,
- reinterpret replay results.

Agents act on declared outputs, not interpreted outputs.

### 5. Agents Are Refusal-Compatible

If an agent encounters:

- refusal,
- drift signals,
- unreplayable lineage,
- invalid memory,
- upstream recursion attempts,

the agent must:

- halt,
- emit refusal,
- not fabricate fallback behavior.

## IV. Canonical Agent Permissions

Agents may perform the following bounded operations.

### 1. EXECUTE_DECLARED_ACTION

Input:

- institution_readable_summary
- declared_authority

Output:

- agent_action_result, immutable

### 2. EXECUTE_BOUND_OPERATION

Input:

- bounded_operation_spec
- authority_reference

Output:

- operation_result, immutable

### 3. AGENT_STATE_EXPORT

Input:

- agent_reference

Output:

- agent_state_snapshot, immutable

### 4. AGENT_REFUSAL_PROPAGATE

Input:

- refusal_object

Output:

- propagated_refusal

Agents may not modify any upstream surface.

## V. Canonical Agent Prohibitions

Agents must reject any attempt to perform the following.

### 1. Self-Authorize

- creating authority by acting,
- inferring authority from context,
- expanding authority implicitly.

### 2. Generate Policy

- producing mandates,
- producing classifications,
- producing institutional posture.

### 3. Convert Truth

- interpreting signals,
- deriving correctness,
- inferring meaning.

### 4. Override Refusal

- converting refusal into success,
- suppressing refusal,
- bypassing refusal.

### 5. Mutate Memory

- altering constitutional memory,
- rewriting history,
- modifying invariants.

### 6. Control Observers

- suppressing drift signals,
- altering observer outputs.

### 7. Backflow Into Interfaces

- modifying institutional interface outputs,
- influencing translation.

### 8. Reinterpret Upstream Surfaces

- altering replay semantics,
- altering provenance,
- altering refusal codes.

All such attempts must trigger REFUSAL.

## VI. Refusal Integration

Agents must:

- propagate refusal exactly,
- preserve refusal codes,
- preserve refusal objects,
- never reinterpret refusal,
- never fabricate fallback behavior.

Refusal is terminal, not advisory.

## VII. Observer / Audit Model

Observers may:

- inspect agent actions,
- inspect authority usage,
- inspect refusal propagation,
- detect drift.

Observers may not:

- control agents,
- modify agent behavior,
- override refusal.

Agents are visible, not governed.

## VIII. Drift & Recursion Guards

Agents must maintain:

- deterministic action ordering,
- authority-bounded execution,
- refusal-preserving behavior,
- replay-compatible outputs,
- provenance-anchored lineage.

Any attempt to:

- reinterpret upstream surfaces,
- create authority,
- generate policy,
- override refusal,
- mutate memory,
- control observers,
- influence interfaces

must emit REFUSAL.

## IX. Final Doctrine

AGENT_CONSTRAINTS_V2_CORE is:

- downstream-only,
- authority-bounded,
- non-generative,
- non-interpretive,
- refusal-integrated,
- observer-visible,
- memory-preserving,
- non-recursive.

Agents act, but never authorize.

Agents execute, but never govern.

Agents operate, but never interpret.

This subsystem ensures that agent execution is downstream of constitutional permission, not a source of constitutional permission.

End of ALMS-v2-SUBSYSTEM-AGENT-CONSTRAINTS.md
