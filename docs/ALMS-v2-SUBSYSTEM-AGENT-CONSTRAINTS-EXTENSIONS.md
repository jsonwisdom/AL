# ALMS-v2-SUBSYSTEM-AGENT-CONSTRAINTS-EXTENSIONS.md

```yaml
status: SUBSYSTEM_CANDIDATE
surface_role: AGENT_CONSTRAINT_EXTENSION_LAYER
epoch: ALMS_v2
global_state: NO_DRIFT
```

## I. Purpose

This subsystem defines the extension protocol for agent-level authority in ALMS_v2.

Agent Constraints Extensions:

- allow new bounded agent capabilities,
- enforce explicit declaration of authority,
- prevent implicit expansion of agent power,
- preserve refusal, replay, and provenance invariants,
- ensure agents remain downstream-only executors,
- prevent recursive sovereignty.

Extensions may add capabilities.

Extensions may not expand authority.

Agents may act only under declared constraints.

Agents may never create constraints by acting.

## II. Registration

```yaml
SUBSYSTEM_NAME: AGENT_CONSTRAINTS_EXTENSIONS_V2_CORE

domain: agent_constraints_extensions
surface_role: authority_extension_bounds

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
  constraint_self_expansion: prohibited

compatibility:
  ALMS_v1: required
  ALMS_v2_STACK: required
  upstream_surfaces:
    - ALMS_v2_AGENT_CONSTRAINTS (authoritative)
    - ALMS_v2_AGENT_OPERATIONS (read-only)
    - ALMS_v2_INSTITUTIONAL_INTERFACES (read-only)
    - ALMS_v2_OBSERVER_NETWORKS (read-only)
    - ALMS_v2_REFUSAL (read-only)
    - ALMS_v2_REPLAY (read-only)
    - ALMS_v2_PROVENANCE (read-only)
    - ALMS_v2_CONSTITUTIONAL_MEMORY (read-only)
    - ALMS_v2_MIGRATION_COMPATIBILITY (read-only)
    - ALMS_v2_ECONOMIC_RECEIPT_SYSTEMS (read-only)

anti_recursion_attestations:
  - no_upward_authority_flow
  - no_constraint_self_expansion
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

## III. Extension Doctrine

### 1. Extensions Add Capabilities, Not Authority

Extensions may:

- define new actions agents can perform,
- define new operations agents may execute,
- define new bounded behaviors.

Extensions may not:

- expand agent authority,
- create implicit authority,
- reinterpret existing constraints.

Capabilities are additive.

Authority is fixed.

### 2. Extensions Must Declare Authority Bounds

Every extension must declare:

- authority_required,
- authority_scope,
- authority_limits,
- refusal_behavior,
- replay_behavior.

No implicit authority.

No inferred authority.

No contextual authority.

### 3. Extensions Are Downstream-Only

Extensions must consume:

- institutional interface outputs,
- observer signals,
- refusal objects,
- replay traces,
- provenance anchors.

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

Refusal is sovereign over extensions.

### 6. Extensions Must Be Replay-Compatible

Extension outputs must be:

- deterministic,
- reproducible under replay,
- refusal-preserving,
- provenance-anchored.

Replay must reproduce extension outputs exactly.

## IV. Canonical Extension Operations

AGENT_CONSTRAINTS_EXTENSIONS_V2_CORE exposes only authority-bounded extension operations.

### 1. DECLARE_AGENT_EXTENSION

Input:

- extension_spec
- authority_bounds

Output:

- extension_registration_record

### 2. EXECUTE_EXTENSION_OPERATION

Input:

- extension_spec
- declared_authority
- agent_state

Output:

- extension_operation_result, immutable

### 3. EXTENSION_INTEGRITY_CHECK

Input:

- extension_registration_record

Output:

- integrity_status (VALID | CORRUPTED | INDETERMINATE)

### 4. EXTENSION_REFUSAL

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

Extensions must reject any attempt to perform the following.

### 1. Expand Authority

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

- inspect extension registrations,
- inspect extension operations,
- verify refusal propagation,
- detect drift.

Observers may not:

- modify extensions,
- override refusal,
- reinterpret constraints.

Extensions are visible, not governable.

## VII. Drift & Recursion Guards

Extensions must maintain:

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

AGENT_CONSTRAINTS_EXTENSIONS_V2_CORE is:

- additive-only,
- authority-bounded,
- deterministic,
- refusal-integrated,
- replay-compatible,
- provenance-anchored,
- observer-visible,
- non-recursive.

Extensions add capabilities, but never expand authority.

Extensions operate, but never govern.

Extensions execute, but never interpret.

This subsystem completes the constitutional guardrail for all future agent-facing expansion in ALMS_v2.

End of ALMS-v2-SUBSYSTEM-AGENT-CONSTRAINTS-EXTENSIONS.md
