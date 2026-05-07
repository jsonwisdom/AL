# ALMS-v2-MIGRATION-COMPATIBILITY.md

```yaml
status: SUBSYSTEM_CANDIDATE
surface_role: EPOCH_COMPATIBILITY_LAYER
epoch: ALMS_v2
global_state: NO_DRIFT
```

## I. Purpose

This subsystem defines the migration and compatibility rules governing:

- ALMS_v1 -> ALMS_v2 inheritance
- ALMS_v2 -> ALMS_v3 forward-compatibility
- cross-epoch surface referencing
- immutable upstream boundaries
- additive-only successor growth

Migration Compatibility ensures:

- no reinterpretation of sealed epochs,
- no drift across epoch boundaries,
- no recursive sovereignty,
- no implicit epoch creation,
- no cross-epoch mutation.

It is the constitutional continuity layer for ALMS.

## II. Registration

```yaml
SUBSYSTEM_NAME: MIGRATION_COMPATIBILITY_V2_CORE

domain: migration_compatibility
surface_role: epoch_continuity_layer

authority_bounds:
  upstream_reinterpretation: prohibited
  recursive_sovereignty: prohibited
  implicit_authority: prohibited
  cross_epoch_mutation: prohibited
  policy_generation: prohibited
  truth_conversion: prohibited
  refusal_override: prohibited
  memory_mutation: prohibited
  observer_control: prohibited

compatibility:
  ALMS_v1: required
  ALMS_v2_STACK: required
  upstream_surfaces:
    - ALMS_v1_SUCCESSION_MANIFEST (sealed)
    - ALMS_v1_COURTROOM (sealed)
    - ALMS_v2_CONSTITUTIONAL_MEMORY (read-only)
    - ALMS_v2_PROVENANCE (read-only)
    - ALMS_v2_REPLAY (read-only)
    - ALMS_v2_REFUSAL (read-only)
    - ALMS_v2_OBSERVER_NETWORKS (read-only)
    - ALMS_v2_INSTITUTIONAL_INTERFACES (read-only)
    - ALMS_v2_AGENT_CONSTRAINTS (read-only)
    - ALMS_v2_AGENT_OPERATIONS (read-only)

anti_recursion_attestations:
  - no_upward_authority_flow
  - no_epoch_reinterpretation
  - no_surface_mutation
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

## III. Migration Doctrine

### 1. Upstream Epochs Are Immutable

ALMS_v1 is:

- sealed,
- immutable,
- non-interpretable,
- non-expandable,
- non-recursive.

Migration Compatibility may reference ALMS_v1,

but may never reinterpret ALMS_v1.

### 2. Successor Epochs Are Additive-Only

ALMS_v2 may:

- add new surfaces,
- add new domains,
- add new invariants,
- add new subsystems.

ALMS_v2 may not:

- mutate ALMS_v1,
- reinterpret ALMS_v1,
- override ALMS_v1 refusal,
- expand ALMS_v1 courtroom,
- alter ALMS_v1 succession manifest.

### 3. Forward-Compatibility Without Prediction

Migration Compatibility may:

- define how ALMS_v3 must reference ALMS_v2,
- define how ALMS_v3 must inherit invariants,
- define how ALMS_v3 must avoid recursion.

Migration Compatibility may not:

- pre-declare ALMS_v3 surfaces,
- pre-declare ALMS_v3 authority,
- create implicit future epochs.

### 4. Provenance-Anchored Epoch Linking

Every cross-epoch reference must include:

- epoch_id,
- surface_path,
- commit_hash,
- immutability_flag,
- provenance_reference.

No inferred lineage.

No synthetic continuity.

No narrative repair.

### 5. Replay-Compatible Epoch Continuity

Replay must:

- reproduce cross-epoch references exactly,
- preserve refusal boundaries across epochs,
- preserve ordering across epochs,
- preserve immutability flags.

Replay may not:

- normalize epoch drift,
- reinterpret sealed surfaces.

### 6. Refusal-Integrated Migration

If migration encounters:

- sealed v1 surfaces,
- invalid v2 surfaces,
- drift signals,
- recursion attempts,

it must emit REFUSAL, not fabricate compatibility.

## IV. Canonical Migration Operations

MIGRATION_COMPATIBILITY_V2_CORE exposes only declarative operations.

### 1. DECLARE_UPSTREAM_COMPATIBILITY

Input:

- upstream_epoch_reference
- surface_reference

Output:

- compatibility_record

### 2. DECLARE_SUCCESSOR_COMPATIBILITY

Input:

- successor_epoch_spec

Output:

- successor_compatibility_record

### 3. MIGRATION_INTEGRITY_CHECK

Input:

- compatibility_record

Output:

- integrity_status (VALID | CORRUPTED | INDETERMINATE)

### 4. MIGRATION_REPLAY

Input:

- compatibility_record
- environment_descriptor

Output:

- replay_status (REPRODUCED | DIVERGENT | INDETERMINATE)

### 5. MIGRATION_REFUSAL

Input:

- violation_type

Output:

- refusal_object

No operation may:

- modify upstream epochs,
- reinterpret sealed surfaces,
- generate authority,
- generate policy.

## V. Prohibited Patterns

Migration Compatibility must reject any attempt to perform the following.

### 1. Reinterpret Sealed Epochs

- altering ALMS_v1 meaning,
- altering ALMS_v1 boundaries,
- altering ALMS_v1 courtroom.

### 2. Mutate Upstream Surfaces

- modifying v1 surfaces,
- rewriting v1 history.

### 3. Create Implicit Epochs

- silent ALMS_v3 creation,
- undeclared successor epochs.

### 4. Generate Authority

- creating new constitutional powers,
- creating new adjudicative surfaces.

### 5. Repair Epoch Drift

- smoothing inconsistencies,
- fabricating continuity.

All such attempts must trigger REFUSAL.

## VI. Observer / Audit Model

Observers may:

- inspect compatibility declarations,
- verify cross-epoch ordering,
- detect drift,
- verify refusal propagation.

Observers may not:

- modify compatibility,
- override refusal,
- reinterpret epochs.

Migration is visible, not governable.

## VII. Drift & Recursion Guards

Migration Compatibility must maintain:

- deterministic epoch ordering,
- provenance-anchored references,
- refusal-preserving behavior,
- replay-compatible continuity.

Any attempt to:

- reinterpret upstream epochs,
- create recursive authority,
- mutate sealed surfaces

must emit REFUSAL.

## VIII. Final Doctrine

MIGRATION_COMPATIBILITY_V2_CORE is:

- declarative,
- non-interpretive,
- refusal-integrated,
- replay-compatible,
- provenance-anchored,
- non-recursive,
- additive-only.

It ensures:

- ALMS_v1 remains sealed,
- ALMS_v2 remains bounded,
- ALMS_v3 and beyond remain non-recursive,
- epoch continuity remains drift-free.

This subsystem completes the inter-epoch constitutional spine of ALMS_v2.

End of ALMS-v2-MIGRATION-COMPATIBILITY.md
