# CRP_VALIDATION_SUITE_V0_1

_validation suite — authority: false, semantic_change: false_

## 1. Purpose and Scope

The CRP Validation Suite V0.1 defines deterministic validation rules for the Git-backed implementation layers of the CRP stack.

It exists to:

- validate Git-backed implementation surfaces
- detect semantic drift, authority elevation, and cross-layer mutation
- classify validation results as GREEN, YELLOW, or RED
- explicitly distinguish Git-backed implementation artifacts from conversation-defined constitutional dependencies

The suite must not pretend that conversation-defined constitutional artifacts are Git-backed.

Validation tests evidence surfaces.
Validation does not create authority.

---

## 2. Binding Receipts

This suite binds to the following Git-backed implementation artifacts:

```json
{
  "CRP_V1_0_CONSTITUTIONAL_STACK_INDEX": "014f4517f980cfe77a701372dd95dba48328d300",
  "CRP_IMPLEMENTATION_SCHEMA_SUITE_V0_1": "54451723ee666e5f198c19e3768d2a08961afa3e",
  "CRP_IMPLEMENTATION_SCHEMA_NORMALIZATION_V0_1": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
  "CRP_API_CONTRACTS_V0_1": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
  "CRP_UI_SAFE_RENDERING_RULES_V0_1": "e8e75c99bb8458aa66ea14b6bde17b3189600f58",
  "authority": false
}
```

These receipts are implementation-layer anchors only.
They do not retroactively make earlier conversation-defined constitutional artifacts Git-backed.

---

## 3. Validation Scope Boundaries

```json
{
  "in_scope_git_backed": [
    "CRP_IMPLEMENTATION_SCHEMA_NORMALIZATION_V0_1",
    "CRP_API_CONTRACTS_V0_1",
    "CRP_UI_SAFE_RENDERING_RULES_V0_1"
  ],
  "partial_scope": [
    "CRP_IMPLEMENTATION_SCHEMA_SUITE_V0_1",
    "CRP_V1_0_CONSTITUTIONAL_STACK_INDEX"
  ],
  "out_of_scope_conversational": [
    "CRP_ENTRY_DESIGN",
    "CRP_INDEXING_RULES",
    "CRP_AGGREGATION_MODEL",
    "CRP_CONVERGENCE_LEDGER",
    "CRP_COURTHOUSE_FLOOR",
    "CRP_OBSERVER_RIGHTS"
  ],
  "authority": false
}
```

Interpretation:

- In-scope Git-backed artifacts may receive GREEN validation.
- Partial-scope artifacts may receive structural validation only.
- Out-of-scope conversational artifacts must be flagged as assumptions and may not receive GREEN.

---

## 4. Result Classes

### 4.1 GREEN

GREEN means:

- the artifact is Git-backed
- the test is deterministic
- the expected result is satisfied
- no semantic drift or authority elevation is detected

### 4.2 YELLOW

YELLOW means:

- the test touches a conversation-defined constitutional dependency
- the dependency lacks an individual Git receipt
- validation cannot lawfully claim full green

Required YELLOW result shape:

```json
{
  "status": "YELLOW",
  "reason": "Constitutional layer not Git-backed",
  "artifact": "<name>",
  "authority": false
}
```

### 4.3 RED

RED means:

- drift detected
- mutation detected
- authority elevation detected
- nondeterminism detected
- schema or contract violation detected

Required RED result shape:

```json
{
  "status": "RED",
  "reason": "<violation>",
  "authority": false
}
```

---

## 5. Test Category: Schema Validation

Source artifact:

```json
{
  "artifact": "CRP_IMPLEMENTATION_SCHEMA_NORMALIZATION_V0_1",
  "commit": "722fb5640ef9a3658a160d0d696a05101fdc5ea1"
}
```

Tests:

- each normalized schema includes `$schema`
- each normalized schema includes `$id`
- each normalized schema includes `type: object`
- each normalized schema includes `additionalProperties: false`
- each normalized schema includes required fields
- each normalized schema preserves `authority: false`
- each normalized schema preserves `semantic_change: false`

Example test vector:

```json
{
  "test_id": "SCHEMA_001_ENTRY_REQUIRED_FIELDS",
  "input_schema_id": "https://crp.local/schemas/v0.1/entry.schema.json",
  "expected_required": [
    "entry_id",
    "layer",
    "timestamp_utc",
    "payload",
    "authority",
    "semantic_change"
  ],
  "expected_status": "GREEN",
  "authority": false
}
```

Failure condition:

```json
{
  "test_id": "SCHEMA_FAIL_AUTHORITY_CONST",
  "condition": "authority const is missing or not false",
  "expected_status": "RED",
  "authority": false
}
```

---

## 6. Test Category: API Contract Conformance

Source artifact:

```json
{
  "artifact": "CRP_API_CONTRACTS_V0_1",
  "commit": "a0e4185bbbb7ca5327d98cbd82803ed854993172"
}
```

Tests:

- each endpoint declares a schema binding
- request examples conform to the bound schema shape
- response examples include `schema_id`
- response examples include `authority: false`
- response examples include `semantic_change: false`
- error envelope preserves non-authority
- idempotency behavior is defined for write-like endpoints

Endpoint inventory from committed contract:

```json
{
  "endpoints": [
    "POST /v0.1/entries",
    "GET /v0.1/entries/{entry_id}",
    "POST /v0.1/indexes",
    "GET /v0.1/indexes/{index_id}",
    "POST /v0.1/aggregations",
    "GET /v0.1/aggregations/{aggregation_id}",
    "POST /v0.1/convergences",
    "GET /v0.1/convergences/{convergence_id}",
    "POST /v0.1/floor-interfaces",
    "GET /v0.1/floor-interfaces/{floor_id}",
    "POST /v0.1/observers",
    "GET /v0.1/meta"
  ],
  "authority": false
}
```

Example test vector:

```json
{
  "test_id": "API_001_RESPONSE_AUTHORITY_FALSE",
  "endpoint": "GET /v0.1/meta",
  "expected_fields": ["data", "schema_id", "authority", "semantic_change"],
  "expected_authority": false,
  "expected_status": "GREEN"
}
```

Failure condition:

```json
{
  "test_id": "API_FAIL_VERIFIED_FIELD",
  "condition": "response includes verified: true",
  "expected_status": "RED",
  "authority": false
}
```

---

## 7. Test Category: UI Rendering Determinism

Source artifact:

```json
{
  "artifact": "CRP_UI_SAFE_RENDERING_RULES_V0_1",
  "commit": "e8e75c99bb8458aa66ea14b6bde17b3189600f58"
}
```

Tests:

- same payload plus same UI profile produces same output
- UI exposes API version
- UI exposes UI profile
- UI preserves `authority: false` where relevant
- UI does not display forbidden authority language
- UI distinguishes observer interpretation from registry/API output
- UI does not silently hide divergent or minority records

Example deterministic test vector:

```json
{
  "test_id": "UI_001_SAME_PAYLOAD_SAME_OUTPUT",
  "payload_hash": "sha256:<payload-hash>",
  "api_version": "0.1",
  "ui_profile": "crp_v0.1_default",
  "expected_same_output": true,
  "expected_status": "GREEN",
  "authority": false
}
```

Forbidden label test:

```json
{
  "test_id": "UI_002_FORBIDDEN_AUTHORITY_LANGUAGE",
  "input_label": "Verified convergence",
  "expected_status": "RED",
  "reason": "AUTHORITY_LANGUAGE_DETECTED",
  "authority": false
}
```

---

## 8. Test Category: Authority Propagation

Sources:

- Schema Normalization
- API Contracts
- UI Safe Rendering Rules

Rule:

`authority: false` must never be overridden, omitted where relevant, inverted, translated into approval, or upgraded.

End-to-end authority invariant:

```json
{
  "schema_authority": false,
  "api_authority": false,
  "ui_authority": false,
  "authority_elevation_allowed": false
}
```

Example test vector:

```json
{
  "test_id": "AUTH_001_END_TO_END_FALSE",
  "input": {
    "authority": false
  },
  "expected_schema": false,
  "expected_api": false,
  "expected_ui": false,
  "expected_status": "GREEN"
}
```

Failure condition:

```json
{
  "test_id": "AUTH_FAIL_BADGE",
  "condition": "UI renders authority badge or verification seal",
  "expected_status": "RED",
  "authority": false
}
```

---

## 9. Test Category: Cross-Layer Integrity

The validation suite tests that implementation layers do not shift responsibilities across boundaries.

Layer boundary rules:

```json
{
  "SCHEMA": "shape_only",
  "API": "contract_only",
  "UI": "render_only",
  "authority": false
}
```

Checks:

- schemas do not define endpoints
- APIs do not define UI rendering
- UI does not define API behavior
- no layer introduces trust, score, verdict, certification, or endorsement
- no layer claims upstream constitutional Git receipts that do not exist

Example test vector:

```json
{
  "test_id": "X_LAYER_001_NO_UI_IN_API",
  "source": "CRP_API_CONTRACTS_V0_1",
  "forbidden_terms": ["render", "badge", "CSS", "component"],
  "expected_status": "GREEN_IF_ABSENT",
  "authority": false
}
```

Yellow condition:

```json
{
  "test_id": "X_LAYER_YELLOW_CONSTITUTIONAL_DEPENDENCY",
  "artifact": "CRP_CONVERGENCE_LEDGER",
  "status": "YELLOW",
  "reason": "Constitutional layer not Git-backed",
  "authority": false
}
```

---

## 10. Deterministic Execution Model

Execution rules:

- same inputs produce same verdict
- no time-dependent verdicts
- no environment-dependent verdicts
- no nondeterministic ordering
- all test results include `authority: false`
- all test results include `semantic_change: false` where applicable

Canonical verdict envelope:

```json
{
  "test_id": "<id>",
  "status": "GREEN | YELLOW | RED",
  "reason": "<reason>",
  "artifact": "<artifact>",
  "authority": false,
  "semantic_change": false
}
```

---

## 11. No-Fake-Green Rule

No test may return GREEN if:

- it depends on an artifact without a Git receipt
- it relies on a conversation-defined constitutional layer as if file-backed
- it requires unstated assumptions
- it requires external interpretation
- it cannot be replayed deterministically

Required result for such cases:

```json
{
  "status": "YELLOW",
  "reason": "No Git receipt for dependency",
  "authority": false
}
```

---

## 12. Validation Summary Format

A full validation run should produce:

```json
{
  "validation_run_id": "<id>",
  "tested_commits": {
    "schema_normalization": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
    "api_contracts": "a0e4185bbbb7ca5327d98cbd82803ed854993172",
    "ui_rendering_rules": "e8e75c99bb8458aa66ea14b6bde17b3189600f58"
  },
  "results": {
    "green": 0,
    "yellow": 0,
    "red": 0
  },
  "authority": false,
  "semantic_change": false
}
```

Counts are observational only. Counts do not create authority.

---

## 13. Final Summary Object

```json
{
  "CRP_VALIDATION_SUITE_V0_1": {
    "role": "implementation_validation_layer",
    "git_backed_layers_tested": [
      "SCHEMA_NORMALIZATION",
      "API_CONTRACTS",
      "UI_RENDERING_RULES"
    ],
    "partial_scope": [
      "SCHEMA_SUITE",
      "CONSTITUTIONAL_STACK_INDEX"
    ],
    "constitutional_assumptions_flagged": [
      "ENTRY_DESIGN",
      "INDEXING_RULES",
      "AGGREGATION_MODEL",
      "CONVERGENCE_LEDGER",
      "COURTHOUSE_FLOOR",
      "OBSERVER_RIGHTS"
    ],
    "test_categories": [
      "schema_validation",
      "api_contract_conformance",
      "ui_rendering_determinism",
      "authority_propagation",
      "cross_layer_integrity"
    ],
    "authority": false,
    "semantic_change": false,
    "next_recommended": "CRP_VALIDATION_HARNESS_V0_1"
  }
}
```

Validation observes conformance.
Validation does not certify truth.
Validation does not grant authority.
No fake green.
