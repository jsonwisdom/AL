# ALMS-v2-SUBSYSTEM-AGENT-OPERATIONS.md

```yaml
status: SUBSYSTEM_CANDIDATE
surface_role: AGENT_OPERATION_LAYER
epoch: ALMS_v2
global_state: NO_DRIFT
```

## I. Purpose

This subsystem defines the permissible operational behaviors of agents in ALMS_v2.

Agent Operations:

- execute only within authority declared by Agent Constraints,
- act only on institution-readable outputs,
- propagate refusal deterministically,
- preserve replay compatibility,
- expose state to observers,
- never generate authority,
- never reinterpret upstream surfaces.

Agents perform actions, but they do not authorize actions.

## II. Registration

```yaml
SUBSYSTEM_NAME: AGENT_OPERATIONS_V2_CORE

domain: agent_operations
surface_role: downstream_execution_layer

authority_bounds:
  upstream_reinterpretation: prohibited
  recursive_sovereignty: prohibited
  implicit_authority: prohibited
  policy_generation: prohibited
  truth_conversion: prohibited
  refusal_override: prohibited
  memory_mutation: prohibited
  observer_control: prohibited
  interface_backflow: prohibited
  constraint_bypass: prohibited

compatibility:
  ALMS_v1: required
  ALMS_v2_STACK: required
  upstream_surfaces:
    - ALMS_v2_INSTITUTIONAL_INTERFACES (read-only)
    - ALMS_v2_AGENT_CONSTRAINTS (authoritative)
    - ALMS_v2_OBSERVER_NETWORKS (read-only)
    - ALMS_v2_REFUSAL (read-only)
    - ALMS_v2_REPLAY (read-only)
    - ALMS_v2_PROVENANCE (read-only)
    - ALMS_v2_CONSTITUTIONAL_MEMORY (read-only)

anti_recursion_attestations:
  - no_upward_authority_flow
  - no_policy_generation
  - no_truth_conversion
  - no_refusal_override
  - no_memory_mutation
  - no_observer_control
  - no_interface_backflow
  - no_constraint_bypass

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

## III. Agent Operation Doctrine

### 1. Execution Under Constraint

Agents may execute actions only when:

- authority is explicitly declared by Agent Constraints,
- the action is downstream of Institutional Interfaces,
- the action is bounded by refusal,
- the action is replay-compatible.

Agents may not infer authority.

Agents may not expand authority.

Agents may not create authority.

### 2. Non-Interpretive Execution

Agents must treat:

- refusal as terminal,
- replay traces as authoritative,
- provenance as immutable,
- memory as non-modifiable,
- observer signals as non-negotiable,
- interface outputs as non-interpretive.

Agents may not:

- classify correctness,
- infer meaning,
- reinterpret upstream signals.

### 3. Deterministic Behavior

Given identical:

- authority inputs,
- interface outputs,
- refusal states,
- environment descriptors,
- agent configuration,

agents must produce identical outputs.

No contextual variation.

No preference-based variation.

No institutional-pressure variation.

### 4. Refusal-Preserving Execution

If refusal is encountered:

- the agent must halt,
- propagate refusal exactly,
- emit no fallback behavior,
- generate no alternative action.

Refusal is terminal, not advisory.

### 5. Replay-Compatible Outputs

Agent outputs must be:

- deterministic,
- reproducible under replay,
- provenance-anchored,
- refusal-preserving,
- environment-canonical.

Replay must reproduce agent outputs exactly.

## IV. Canonical Agent Operations

AGENT_OPERATIONS_V2_CORE exposes only bounded execution operations.

### 1. EXECUTE_ACTION

Input:

- institution_readable_summary
- declared_authority

Output:

- action_result, immutable

### 2. EXECUTE_TASK

Input:

- task_spec
- authority_reference

Output:

- task_result, immutable

### 3. PROPAGATE_REFUSAL

Input:

- refusal_object

Output:

- propagated_refusal

### 4. EXPORT_AGENT_STATE

Input:

- agent_reference

Output:

- agent_state_snapshot, immutable

### 5. EXECUTION_INTEGRITY_CHECK

Input:

- action_result

Output:

- integrity_status (VALID | CORRUPTED | INDETERMINATE)

No operation may:

- modify upstream surfaces,
- reinterpret refusal,
- generate policy,
- generate truth,
- influence observers,
- influence interfaces.

## V. Canonical Agent Prohibitions

Agents must reject any attempt to perform the following.

### 1. Self-Authorize

- creating authority by acting,
- inferring authority from context.

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
- suppressing refusal.

### 5. Mutate Memory

- altering constitutional memory,
- rewriting history.

### 6. Control Observers

- suppressing drift signals,
- altering observer outputs.

### 7. Backflow Into Interfaces

- modifying interface outputs,
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

Refusal is sovereign over agent execution.

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

AGENT_OPERATIONS_V2_CORE is:

- downstream-only,
- authority-bounded,
- deterministic,
- refusal-integrated,
- replay-compatible,
- provenance-anchored,
- observer-visible,
- non-recursive.

Agents act, but never authorize.

Agents execute, but never govern.

Agents operate, but never interpret.

This subsystem completes the ALMS_v2 execution boundary and closes the successor-epoch operational chain.

End of ALMS-v2-SUBSYSTEM-AGENT-OPERATIONS.md
