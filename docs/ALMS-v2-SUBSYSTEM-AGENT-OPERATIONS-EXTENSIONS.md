# ALMS-v2-SUBSYSTEM-AGENT-OPERATIONS-EXTENSIONS.md

```yaml
status: SUBSYSTEM_CANDIDATE
surface_role: AGENT_OPERATION_EXTENSION_LAYER
epoch: ALMS_v2
global_state: NO_DRIFT
```

## I. Purpose

This subsystem defines the extension protocol for agent-level operational behaviors in ALMS_v2.

Agent Operations Extensions:

- allow new operational behaviors to be added,
- enforce explicit declaration of operational bounds,
- preserve refusal, replay, and provenance invariants,
- ensure all operations remain downstream-only,
- prevent implicit operational authority,
- prevent recursive sovereignty,
- prevent interpretive drift.

Extensions may add new operations.

Extensions may not expand authority.

Agents may execute only under declared constraints.

Agents may never create operational authority by acting.

## II. Registration

```yaml
SUBSYSTEM_NAME: AGENT_OPERATIONS_EXTENSIONS_V2_CORE

domain: agent_operations_extensions
surface_role: downstream_operation_extension_layer

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
  operation_self_expansion: prohibited

compatibility:
  ALMS_v1: required
  ALMS_v2_STACK: required
  upstream_surfaces:
    - ALMS_v2_AGENT_OPERATIONS (authoritative)
    - ALMS_v2_AGENT_CONSTRAINTS (read-only)
    - ALMS_v2_INSTITUTIONAL_INTERFACES (read-only)
    - ALMS_v2_OBSERVER_NETWORKS (read-only)
    - ALMS_v2_REFUSAL (read-only)
    - ALMS_v2_REPLAY (read-only)
    - ALMS_v2_PROVENANCE (read-only)
    - ALMS_v2_CONSTITUTIONAL_MEMORY (read-only)
    - ALMS_v2_MIGRATION_COMPATIBILITY (read-only)
    - ALMS_v2_ECONOMIC_RECEIPT_SYSTEMS (read-only)
    - ALMS_v2_AGENT_CONSTRAINTS_EXTENSIONS (read-only)

anti_recursion_attestations:
  - no_upward_authority_flow
  - no_operation_self_expansion
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

## III. Operation Extension Doctrine

### 1. Extensions Add Operations, Not Authority

Extensions may:

- define new operational behaviors,
- define new execution patterns,
- define new bounded tasks.

Extensions may not:

- expand agent authority,
- infer authority from context,
- reinterpret existing constraints.

Operations are additive.

Authority is fixed.

### 2. Extensions Must Declare Operational Bounds

Every extension must declare:

- operation_scope,
- authority_required,
- refusal_behavior,
- replay_behavior,
- provenance_requirements.

No implicit operational authority.

No contextual operational authority.

### 3. Extensions Are Downstream-Only

Extensions must consume:

- institutional interface outputs,
- observer signals,
- refusal objects,
- replay traces,
- provenance anchors,
- constraint declarations.

Extensions may not:

- bypass upstream layers,
- reinterpret upstream surfaces,
- mutate upstream state.

### 4. Extensions Must Preserve Determinism

Given identical:

- authority inputs,
- interface outputs,
- refusal states,
- environment descriptors,
- agent configuration,

extensions must produce identical outputs.

No contextual variation.

No preference-based variation.

No institutional-pressure variation.

### 5. Extensions Must Preserve Refusal

If refusal is encountered:

- the extension must halt,
- propagate refusal exactly,
- emit no fallback behavior.

Refusal is sovereign over operations.

### 6. Extensions Must Be Replay-Compatible

Extension outputs must be:

- deterministic,
- reproducible under replay,
- refusal-preserving,
- provenance-anchored.

Replay must reproduce extension outputs exactly.

## IV. Canonical Extension Operations

AGENT_OPERATIONS_EXTENSIONS_V2_CORE exposes only bounded operational extension functions.

### 1. DECLARE_OPERATION_EXTENSION

Input:

- operation_extension_spec
- authority_bounds

Output:

- operation_extension_registration_record

### 2. EXECUTE_OPERATION_EXTENSION

Input:

- operation_extension_spec
- declared_authority
- agent_state

Output:

- operation_extension_result, immutable

### 3. OPERATION_EXTENSION_INTEGRITY_CHECK

Input:

- operation_extension_registration_record

Output:

- integrity_status (VALID | CORRUPTED | INDETERMINATE)

### 4. OPERATION_EXTENSION_REFUSAL

Input:

- violation_type

Output:

- refusal_object

No operation may:

- generate authority,
- reinterpret constraints,
- override refusal,
- mutate memory.

## V. Prohibited Patterns

Operation Extensions must reject any attempt to perform the following.

### 1. Expand Operational Authority

- implicit authority creation,
- contextual authority inference,
- authority laundering.

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

## VI. Observer / Audit Model

Observers may:

- inspect operation extension registrations,
- inspect extension executions,
- verify refusal propagation,
- detect drift.

Observers may not:

- modify extensions,
- override refusal,
- reinterpret constraints.

Extensions are visible, not governable.

## VII. Drift & Recursion Guards

Operation Extensions must maintain:

- deterministic behavior,
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

## VIII. Final Doctrine

AGENT_OPERATIONS_EXTENSIONS_V2_CORE is:

- additive-only,
- authority-bounded,
- deterministic,
- refusal-integrated,
- replay-compatible,
- provenance-anchored,
- observer-visible,
- non-recursive.

Extensions add operations, but never expand authority.

Extensions execute, but never govern.

Extensions operate, but never interpret.

This subsystem completes the constitutional extension perimeter for agent-level execution in ALMS_v2.

End of ALMS-v2-SUBSYSTEM-AGENT-OPERATIONS-EXTENSIONS.md
