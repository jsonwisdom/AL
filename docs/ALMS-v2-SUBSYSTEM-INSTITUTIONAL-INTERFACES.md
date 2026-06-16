# ALMS-v2-SUBSYSTEM-INSTITUTIONAL-INTERFACES.md

```yaml
status: SUBSYSTEM_CANDIDATE
surface_role: INSTITUTIONAL_INTERFACE_LAYER
epoch: ALMS_v2
global_state: NO_DRIFT
```

## I. Purpose

This subsystem defines the institutional interface layer for ALMS_v2.

Institutional Interfaces provide:

- structured, non-interpretive, institution-readable outputs
- translation of mechanical signals into externally consumable formats
- downstream-only visibility into ALMS state
- zero influence on upstream surfaces
- zero authority generation
- zero policy creation

Institutional Interfaces are bridges, not actors.

They sit:

```text
Provenance
 -> Replay
 -> Refusal
 -> Constitutional Memory
 -> Observer Networks
 -> Institutional Interfaces
 -> external institutions
```

They are the final internal layer before external institutional consumption.

## II. Registration

```yaml
SUBSYSTEM_NAME: INSTITUTIONAL_INTERFACES_V2_CORE

domain: institutional_interfaces
surface_role: downstream_translation_layer

authority_bounds:
  upstream_reinterpretation: prohibited
  recursive_sovereignty: prohibited
  implicit_authority: prohibited
  cross_domain_expansion: prohibited
  policy_generation: prohibited
  truth_conversion: prohibited
  institutional_action_influence: prohibited

compatibility:
  ALMS_v1: required
  ALMS_v2_STACK: required
  upstream_surfaces:
    - ALMS_v2_PROVENANCE (read-only)
    - ALMS_v2_REPLAY (read-only)
    - ALMS_v2_REFUSAL (read-only)
    - ALMS_v2_CONSTITUTIONAL_MEMORY (read-only)
    - ALMS_v2_OBSERVER_NETWORKS (read-only)

anti_recursion_attestations:
  - no_upward_authority_flow
  - no_reconstructability_manufacture
  - no_policy_generation
  - no_truth_conversion
  - no_refusal_override
  - no_memory_mutation
  - no_observer_control

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

## III. Interface Doctrine

### 1. Downstream-Only Translation

Institutional Interfaces may:

- translate mechanical signals into institution-readable formats,
- expose structured summaries of provenance, replay, refusal, and memory states,
- provide drift-aware, refusal-preserving outputs.

Institutional Interfaces may not:

- interpret signals,
- classify correctness,
- generate policy,
- create institutional mandates,
- convert signals into truth.

Translation is formatting, not meaning.

### 2. Non-Generative

Institutional Interfaces may not:

- create new authority,
- create new doctrine,
- create new classifications,
- create new institutional actions.

They expose what ALMS sees, not what ALMS thinks.

### 3. Observer-Precedence

Institutional Interfaces must consume only:

- observer outputs,
- refusal objects,
- replay traces,
- provenance anchors,
- constitutional memory entries.

They may not:

- bypass observers,
- override observer drift signals,
- suppress refusal.

Observers see first; interfaces speak second.

### 4. Provenance-Bound

Every interface output must include:

- provenance_reference,
- observation_reference,
- refusal_reference, if applicable,
- memory_reference,
- timestamp,
- immutability_flag.

No inferred lineage.

No synthetic continuity.

No narrative repair.

### 5. Replay-Compatible

Interface outputs must be:

- deterministic,
- reproducible under replay,
- environment-canonical,
- refusal-preserving.

Replay must reproduce interface outputs exactly.

### 6. Refusal-Integrated

If upstream surfaces emit refusal:

- the interface must propagate refusal,
- not reinterpret refusal,
- not convert refusal into success,
- not fabricate fallback outputs.

Refusal is terminal, not advisory.

### 7. Non-Interference

Institutional Interfaces may not:

- influence execution,
- modify provenance,
- alter replay parameters,
- override refusal,
- mutate memory,
- control observers.

Interfaces publish, they do not act.

## IV. Canonical Interface Operations

INSTITUTIONAL_INTERFACES_V2_CORE exposes only translation operations.

### 1. INTERFACE_SUMMARY

Input:

- observer_record
- provenance_reference
- replay_trace
- refusal_object, optional
- memory_reference

Output:

- institution_readable_summary, immutable

### 2. INTERFACE_STATE_EXPORT

Input:

- subsystem_reference

Output:

- structured_state_snapshot, immutable

### 3. INTERFACE_DRIFT_REPORT

Input:

- drift_signal

Output:

- institution_readable_drift_report

### 4. INTERFACE_REFUSAL_EXPORT

Input:

- refusal_object

Output:

- refusal_export_record

No operation may:

- classify correctness,
- generate policy,
- reinterpret upstream semantics.

## V. Prohibited Patterns

Institutional Interfaces must reject any attempt to perform the following.

### 1. Influence Institutions

- generating policy,
- generating mandates,
- generating recommendations,
- generating institutional posture.

### 2. Influence ALMS

- modifying upstream surfaces,
- altering replay,
- mutating memory,
- overriding refusal.

### 3. Interpret

- deriving meaning,
- inferring correctness,
- smoothing inconsistencies,
- fabricating continuity.

### 4. Create Authority

- implicit mandates,
- implicit classifications,
- implicit truth claims.

### 5. Hidden Channels

- undeclared outputs,
- silent routing,
- implicit signaling.

All such patterns must trigger REFUSAL.

## VI. Observer / Audit Model

Observers may:

- inspect interface outputs,
- verify refusal propagation,
- verify replay equivalence,
- detect drift.

Observers may not:

- modify interface behavior,
- suppress outputs,
- override refusal.

Interfaces are visible, not governable.

## VII. Drift & Recursion Guards

Institutional Interfaces must maintain:

- deterministic output ordering,
- provenance-anchored exports,
- refusal-preserving behavior,
- replay-compatible outputs.

Any attempt to:

- influence upstream surfaces,
- generate authority,
- reinterpret signals,
- create recursive sovereignty

must emit REFUSAL.

## VIII. Final Doctrine

INSTITUTIONAL_INTERFACES_V2_CORE is:

- downstream-only,
- non-generative,
- non-interpretive,
- provenance-bound,
- replay-compatible,
- refusal-integrated,
- observer-precedent,
- non-recursive.

It translates but never decides.

It exposes but never influences.

It bridges but never governs.

This subsystem completes the v2 constitutional bridge to external institutions without granting them, or itself, any upstream authority.

End of ALMS-v2-SUBSYSTEM-INSTITUTIONAL-INTERFACES.md
