# ALMS-v1-EPOCH-CHECK-REFUSALS.md

```yaml
status: CANONICAL_CANDIDATE
surface_role: EPOCH_CHECK_REFUSAL_CODES
epoch_id: ALMS_v1
global_state: NO_DRIFT
```

## 1. Purpose

This surface defines the complete refusal code taxonomy for `alms-epoch-check`, the constitutional gatekeeper for ALMS.

`alms-epoch-check` has a two-symbol output space:

```text
PASS
REFUSE
```

No warnings.

No partial passes.

No best-effort behavior.

No advisory messages.

A refusal code is not an error. It is a constitutional violation.

This document defines the only admissible refusal codes for ALMS-v1.

## 2. Output Space

```yaml
output_space:
  - PASS
  - REFUSE
warnings_allowed: false
partial_pass_allowed: false
best_effort_allowed: false
```

Any attempt to emit output outside this space is itself a constitutional violation.

## 3. Refusal Code Families

Refusal codes are grouped by constitutional domain:

```text
REFUSE-EPOCH-*       epoch / closed surface failures
REFUSE-REGISTRY-*    standing / operator failures
REFUSE-PROV-*        provenance schema failures
REFUSE-EQ-*          equivalence class failures
REFUSE-REPLAY-*      replay story failures
REFUSE-MUTATION-*    closed epoch mutation attempts
```

Each family corresponds directly to a seated v1 surface:

- Epoch -> Succession Manifest
- Registry -> Registry Charter
- Provenance -> Provenance Schemas
- Equivalence -> Equivalence Classes
- Replay -> Provenance + Equivalence + Boundary
- Mutation -> Succession Manifest immutability clause

This ensures refusal semantics are constitutionally grounded, not implementation-defined.

## 4. Canonical v1 Refusal Matrix

The following code set is canonical for ALMS-v1.

Successor epochs may extend the taxonomy but may not mutate these codes.

### 4.1 Epoch Refusals

```text
REFUSE-EPOCH-001    UNKNOWN_EPOCH
REFUSE-EPOCH-002    EPOCH_NOT_CLOSED
REFUSE-EPOCH-003    SURFACE_SET_MISMATCH
```

Meanings:

- `UNKNOWN_EPOCH`: `epoch_id` does not correspond to a seated epoch.
- `EPOCH_NOT_CLOSED`: the epoch surface set is not closed under its Succession Manifest.
- `SURFACE_SET_MISMATCH`: one or more canonical surfaces do not match the hash declared in the Succession Manifest.

### 4.2 Registry Refusals

```text
REFUSE-REGISTRY-001 UNKNOWN_OPERATOR
REFUSE-REGISTRY-002 OPERATOR_NOT_ACTIVE
REFUSE-REGISTRY-003 REGISTRY_CHAIN_INVALID
```

Meanings:

- `UNKNOWN_OPERATOR`: operator not present in the v1 Registry.
- `OPERATOR_NOT_ACTIVE`: operator exists but lacks active standing.
- `REGISTRY_CHAIN_INVALID`: registry lineage or authorization chain is invalid or non-replayable.

### 4.3 Provenance Refusals

```text
REFUSE-PROV-001     MISSING_PROVENANCE
REFUSE-PROV-002     SCHEMA_VALIDATION_FAILED
REFUSE-PROV-003     PARENT_RECEIPT_MISSING
REFUSE-PROV-004     LINEAGE_CYCLE_DETECTED
```

Meanings:

- `MISSING_PROVENANCE`: no provenance file provided.
- `SCHEMA_VALIDATION_FAILED`: provenance does not validate against v1 Provenance Schemas.
- `PARENT_RECEIPT_MISSING`: a referenced parent receipt is missing.
- `LINEAGE_CYCLE_DETECTED`: provenance lineage contains a cycle.

### 4.4 Equivalence Refusals

```text
REFUSE-EQ-001       UNKNOWN_CLASS_ID
REFUSE-EQ-002       NATURAL_LANGUAGE_EQUIVALENCE
REFUSE-EQ-003       TEST_VECTORS_MISSING
REFUSE-EQ-004       PREDICATE_NOT_TOTAL
```

Meanings:

- `UNKNOWN_CLASS_ID`: `class_id` not defined in v1 Equivalence Classes.
- `NATURAL_LANGUAGE_EQUIVALENCE`: equivalence class uses inadmissible natural-language semantics.
- `TEST_VECTORS_MISSING`: required test vectors absent.
- `PREDICATE_NOT_TOTAL`: predicate fails totality requirement.

### 4.5 Replay Refusals

```text
REFUSE-REPLAY-001   NON_REPLAYABLE_STORY
REFUSE-REPLAY-002   EXECUTION_LOG_MISSING
```

Meanings:

- `NON_REPLAYABLE_STORY`: the claim plus provenance cannot be replayed under v1 law.
- `EXECUTION_LOG_MISSING`: required execution log or replay evidence is missing.

### 4.6 Mutation Refusals

```text
REFUSE-MUTATION-001 CLOSED_EPOCH_MUTATION_ATTEMPT
```

Meaning:

- `CLOSED_EPOCH_MUTATION_ATTEMPT`: attempt to mutate a canonical surface in a closed epoch.

## 5. Constitutional Guarantees

This refusal taxonomy guarantees:

- no ambiguity in refusal semantics,
- no drift between implementation and law,
- no helpful behavior from the gatekeeper,
- no silent fallback to best-effort execution,
- no undefined refusal states.

Every refusal is:

- enumerated,
- constitutional,
- replayable,
- hash-bound,
- epoch-scoped.

## 6. Constitutional State

```yaml
epoch_id: ALMS_v1
refusal_taxonomy: CLOSED
global_state: NO_DRIFT
```

End of ALMS-v1-EPOCH-CHECK-REFUSALS.md
