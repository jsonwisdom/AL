# ALMS-v1-EQUIVALENCE-CLASSES.md

```yaml
status: CANONICAL_CANDIDATE
global_state: NO_DRIFT
surface_role: DEFINES_CANONICAL_EQUIVALENCE_CLASSES
governs: PROV-008, PROV-009, Treaty III.2
```

## 1. Constitutional Purpose

This surface defines the canonical equivalence classes admissible in ALMS-v1 and the executability requirements for any class specification referenced by provenance objects.

This document closes the constitutional gap introduced by PROV-008 and PROV-009 by ensuring that every `class_id` referenced in provenance is:

- defined,
- executable,
- total over its declared domain,
- substrate-bounded,
- and replay-verifiable.

No equivalence class may be defined in natural language.

All class specifications MUST be executable predicates.

## 2. Substrate Model

### 2.1 Active Substrate

```text
JSON_SCHEMA_2020_12
```

All canonical v1 equivalence classes MUST be defined as JSON Schema 2020-12 predicates over output pairs.

### 2.2 Reserved Substrate

```text
WASM_DETERMINISTIC_V1
```

This substrate is reserved for future epochs. No v1 class may use it, but the schema allows its declaration without drift.

### 2.3 Inadmissible Substrates

- Natural language
- Unbounded programming languages such as Python or JavaScript
- Any substrate lacking deterministic replay semantics

Any class using an inadmissible substrate MUST be rejected by the Registry.

## 3. Canonical Record Structure

Each equivalence class is a constitutional object with the following shape:

```json
{
  "class_id": "string",
  "class_spec_hash": "sha256:<64 lowercase hex>",
  "spec_substrate": "JSON_SCHEMA_2020_12 | WASM_DETERMINISTIC_V1",
  "predicate_schema": { "type": "object" },
  "totality": true,
  "determinism_class": "DET_STRICT | DET_HASH | DET_STRUCTURAL | DET_DISTRIBUTIONAL",
  "test_vectors": [
    {
      "input_pair": { "lhs": {}, "rhs": {} },
      "expected": true
    }
  ],
  "test_vectors_hash": "sha256:<64 lowercase hex>"
}
```

Mandatory invariants:

1. `totality` MUST be true.
2. `test_vectors` MUST be non-empty.
3. `spec_substrate` MUST be one of the allowed substrates for the epoch.
4. `class_spec_hash` MUST be the canonical SHA-256 of the executable predicate.
5. `test_vectors_hash` MUST be the canonical SHA-256 of the test vector set.
6. `predicate_schema` MUST be a valid JSON Schema 2020-12 document when `spec_substrate = JSON_SCHEMA_2020_12`.

## 4. Canonical v1 Equivalence Classes

The following classes are constitutionally seated in v1.

All are defined using JSON Schema 2020-12 predicates over `{ lhs, rhs }`.

### 4.1 HASH_EQUIVALENCE_V1

```yaml
class_id: hash_equivalence_v1
determinism_class: DET_HASH
definition: lhs.hash == rhs.hash
spec_substrate: JSON_SCHEMA_2020_12
```

Predicate meaning: both sides expose a hash field and the two hashes are equal.

Test vectors:

- equal hashes -> true
- unequal hashes -> false

### 4.2 STRUCTURAL_EQUIVALENCE_V1

```yaml
class_id: structural_equivalence_v1
determinism_class: DET_STRUCTURAL
definition: lhs.structure == rhs.structure
spec_substrate: JSON_SCHEMA_2020_12
```

Predicate meaning: both sides expose structural fields and those fields match exactly under the declared structure predicate.

Test vectors:

- identical structure -> true
- differing field sets -> false

### 4.3 SEMANTIC_EQUIVALENCE_V1

```yaml
class_id: semantic_equivalence_v1
determinism_class: DET_STRICT
definition: strict semantic identity under declared fields
spec_substrate: JSON_SCHEMA_2020_12
```

Predicate meaning: semantic fields are explicitly declared and must match exactly.

Natural language semantic similarity is not accepted.

Test vectors:

- identical semantic fields -> true
- mismatch in any semantic field -> false

### 4.4 DISTRIBUTIONAL_EQUIVALENCE_V1

```yaml
class_id: distributional_equivalence_v1
determinism_class: DET_DISTRIBUTIONAL
definition: equality of declared distributional statistics
spec_substrate: JSON_SCHEMA_2020_12
```

Predicate meaning: declared metrics, such as mean and variance, must match exactly unless a later epoch seats a formal tolerance model.

Test vectors:

- identical metrics -> true
- any metric mismatch -> false

## 5. Executability Test

Any equivalence class, canonical or custom, MUST pass the Executability Test.

```json
{
  "type": "object",
  "required": [
    "class_id",
    "class_spec_hash",
    "spec_substrate",
    "predicate_schema",
    "totality",
    "determinism_class",
    "test_vectors",
    "test_vectors_hash"
  ]
}
```

A class passes the Executability Test iff:

1. `spec_substrate` is allowed in the epoch.
2. `predicate_schema` is valid JSON Schema 2020-12 when substrate is active.
3. `totality == true`.
4. `test_vectors` are non-empty and replay to the expected outputs.
5. `class_spec_hash` matches the canonical hash of the predicate.
6. `test_vectors_hash` matches the canonical hash of the test vector set.

Any failure MUST be treated as provenance forgery under Treaty III.2.

## 6. Registry Integration

The Registry MUST reject any provenance object referencing a `class_id` that:

- is not defined in this document,
- fails the Executability Test,
- uses an inadmissible substrate,
- or has mismatched hashes.

This closes PROV-008 and PROV-009.

## 7. Succession Constraints

This surface MUST be seated before the v1 Succession Manifest.

The epoch cannot close with undefined or non-executable equivalence classes.

## 8. Constitutional State

```yaml
global_state: NO_DRIFT
surface_state: READY_FOR_SEATING
```

## 9. Equivalence Class Invariants

```text
EQ-INV-001  Natural language equivalence is inadmissible.
EQ-INV-002  Every equivalence class must be executable.
EQ-INV-003  Every equivalence class must be total over its declared domain.
EQ-INV-004  Every equivalence class must include non-empty test vectors.
EQ-INV-005  JSON_SCHEMA_2020_12 is the only active substrate in v1.
EQ-INV-006  WASM_DETERMINISTIC_V1 is reserved but inactive in v1.
EQ-INV-007  Unknown class_id references are provenance failures.
EQ-INV-008  Mismatched class_spec_hash or test_vectors_hash is provenance forgery.
EQ-INV-009  Custom classes must pass the same Executability Test as canonical classes.
EQ-INV-010  Later epochs may add substrates but may not retroactively legalize non-executable v1 classes.
```

End of ALMS-v1-EQUIVALENCE-CLASSES.md
