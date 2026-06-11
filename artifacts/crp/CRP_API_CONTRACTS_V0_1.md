# CRP_API_CONTRACTS_V0_1

_api contract surface — authority: false_

## 1. Purpose and Scope

The CRP API Contracts V0.1 artifact defines the request and response surface for accessing CRP implementation schemas through explicit, replay-safe endpoints.

It does not:

- reinterpret constitutional meaning
- upgrade schema semantics
- introduce authority
- define UI rendering behavior
- define storage engine internals
- assert Git-backed status for upstream V0.1 constitutional artifacts

APIs expose contracted data shapes.
APIs do not decide truth.

---

## 2. Binding Receipts

This artifact binds to the Git-backed schema normalization artifact:

```json
{
  "artifact": "CRP_IMPLEMENTATION_SCHEMA_NORMALIZATION_V0_1",
  "repo": "jsonwisdom/AL",
  "path": "artifacts/crp/CRP_IMPLEMENTATION_SCHEMA_NORMALIZATION_V0_1.md",
  "commit": "722fb5640ef9a3658a160d0d696a05101fdc5ea1",
  "authority": false
}
```

Canonical schema IDs:

```json
{
  "entry": "https://crp.local/schemas/v0.1/entry.schema.json",
  "index": "https://crp.local/schemas/v0.1/index.schema.json",
  "aggregation": "https://crp.local/schemas/v0.1/aggregation.schema.json",
  "convergence": "https://crp.local/schemas/v0.1/convergence.schema.json",
  "floor_interface": "https://crp.local/schemas/v0.1/floor-interface.schema.json",
  "observer": "https://crp.local/schemas/v0.1/observer.schema.json",
  "meta": "https://crp.local/schemas/v0.1/meta.schema.json"
}
```

These IDs are structural binding targets only. They do not imply network availability or authority.

---

## 3. Global API Invariants

All CRP API contracts obey:

- CONTRACT_ONLY — endpoints define request and response envelopes only.
- NON_AUTHORITY — every response carries `authority: false`.
- NO_SEMANTIC_CHANGE — APIs do not alter schema meaning.
- NO_HIDDEN_SIDE_EFFECTS — GET-like reads never mutate CRP state.
- IDEMPOTENT_WRITES — write-like submissions are keyed by stable identifiers.
- SCHEMA_BOUND — payloads must bind to the corresponding normalized schema `$id`.
- REPLAY_STABLE_ENVELOPES — same request and same registry state produce byte-stable responses where implementation supports deterministic serialization.

---

## 4. Versioning Rules

Base version:

```text
/v0.1
```

Required headers:

```http
Accept: application/json
X-CRP-Version: 0.1
```

Optional idempotency header for write-like endpoints:

```http
Idempotency-Key: <stable-client-key>
```

Version rule:

- Minor-compatible clarifications may be documented without changing endpoint paths.
- Shape changes require a new version path.
- Authority semantics may not change inside any compatible version.

---

## 5. Error Envelope

All errors use the same non-authoritative structure.

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Payload does not satisfy schema.",
    "details": []
  },
  "authority": false,
  "semantic_change": false
}
```

Status classes:

- `400 BAD_REQUEST` — malformed JSON, missing required request envelope, unsupported version header.
- `404 NOT_FOUND` — requested identifier is not present in the implementation surface.
- `409 CONFLICT` — idempotency key or stable ID conflicts with a different payload.
- `422 UNPROCESSABLE_ENTITY` — JSON is well-formed but fails the bound normalized schema.
- `500 INTERNAL_ERROR` — implementation failure; no authority claim created.

---

## 6. Endpoint: Submit Entry

```http
POST /v0.1/entries
```

Schema binding:

```json
{
  "request_schema": "https://crp.local/schemas/v0.1/entry.schema.json",
  "response_schema": "https://crp.local/schemas/v0.1/entry.schema.json"
}
```

Idempotency key:

```text
entry_id
```

Request example:

```json
{
  "entry_id": "entry_001",
  "layer": "ENTRY",
  "timestamp_utc": "2026-06-11T17:00:00Z",
  "payload": {
    "kind": "witness_entry",
    "note": "structural payload only"
  },
  "authority": false,
  "semantic_change": false
}
```

Response example:

```json
{
  "data": {
    "entry_id": "entry_001",
    "layer": "ENTRY",
    "timestamp_utc": "2026-06-11T17:00:00Z",
    "payload": {
      "kind": "witness_entry",
      "note": "structural payload only"
    },
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/entry.schema.json",
  "authority": false,
  "semantic_change": false
}
```

Forbidden behavior:

- no verification result
- no witness credibility scoring
- no automatic convergence decision

---

## 7. Endpoint: Fetch Entry

```http
GET /v0.1/entries/{entry_id}
```

Response binds to:

```text
https://crp.local/schemas/v0.1/entry.schema.json
```

Response example:

```json
{
  "data": {
    "entry_id": "entry_001",
    "layer": "ENTRY",
    "timestamp_utc": "2026-06-11T17:00:00Z",
    "payload": {},
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/entry.schema.json",
  "authority": false,
  "semantic_change": false
}
```

Read behavior:

- stateless
- no mutation
- no observer logging required by this contract

---

## 8. Endpoint: Create Index Record

```http
POST /v0.1/indexes
```

Schema binding:

```text
https://crp.local/schemas/v0.1/index.schema.json
```

Idempotency key:

```text
index_id
```

Request example:

```json
{
  "index_id": "index_001",
  "layer": "INDEX",
  "entry_id": "entry_001",
  "coordinates": {
    "seed_id": "seed_001",
    "insertion_order": 1
  },
  "authority": false,
  "semantic_change": false
}
```

Response example:

```json
{
  "data": {
    "index_id": "index_001",
    "layer": "INDEX",
    "entry_id": "entry_001",
    "coordinates": {
      "seed_id": "seed_001",
      "insertion_order": 1
    },
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/index.schema.json",
  "authority": false,
  "semantic_change": false
}
```

Forbidden behavior:

- no ranking
- no priority labels
- no trust ordering

---

## 9. Endpoint: Fetch Index Record

```http
GET /v0.1/indexes/{index_id}
```

Response binds to:

```text
https://crp.local/schemas/v0.1/index.schema.json
```

Response example:

```json
{
  "data": {
    "index_id": "index_001",
    "layer": "INDEX",
    "entry_id": "entry_001",
    "coordinates": {},
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/index.schema.json",
  "authority": false,
  "semantic_change": false
}
```

---

## 10. Endpoint: Create Aggregation

```http
POST /v0.1/aggregations
```

Schema binding:

```text
https://crp.local/schemas/v0.1/aggregation.schema.json
```

Idempotency key:

```text
aggregation_id
```

Request example:

```json
{
  "aggregation_id": "aggregation_001",
  "layer": "AGGREGATION",
  "inputs": ["entry_001", "entry_002"],
  "comparison_result": {
    "reported_only": true,
    "outcome_counts": {
      "GREEN_MATCH": 1,
      "YELLOW_DIVERGENCE": 1,
      "RED_FAILURE": 0
    }
  },
  "authority": false,
  "semantic_change": false
}
```

Response example:

```json
{
  "data": {
    "aggregation_id": "aggregation_001",
    "layer": "AGGREGATION",
    "inputs": ["entry_001", "entry_002"],
    "comparison_result": {
      "reported_only": true
    },
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/aggregation.schema.json",
  "authority": false,
  "semantic_change": false
}
```

Forbidden behavior:

- no consensus declaration
- no majority-as-truth claim
- no evidence deletion

---

## 11. Endpoint: Fetch Aggregation

```http
GET /v0.1/aggregations/{aggregation_id}
```

Response binds to:

```text
https://crp.local/schemas/v0.1/aggregation.schema.json
```

Response example:

```json
{
  "data": {
    "aggregation_id": "aggregation_001",
    "layer": "AGGREGATION",
    "inputs": [],
    "comparison_result": {},
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/aggregation.schema.json",
  "authority": false,
  "semantic_change": false
}
```

---

## 12. Endpoint: Create Convergence Record

```http
POST /v0.1/convergences
```

Schema binding:

```text
https://crp.local/schemas/v0.1/convergence.schema.json
```

Idempotency key:

```text
convergence_id
```

Request example:

```json
{
  "convergence_id": "convergence_001",
  "layer": "CONVERGENCE",
  "aggregation_id": "aggregation_001",
  "aligned_record": {
    "event_type": "ALIGNMENT_OBSERVED",
    "truth_claim_allowed": false
  },
  "authority": false,
  "semantic_change": false
}
```

Response example:

```json
{
  "data": {
    "convergence_id": "convergence_001",
    "layer": "CONVERGENCE",
    "aggregation_id": "aggregation_001",
    "aligned_record": {
      "event_type": "ALIGNMENT_OBSERVED",
      "truth_claim_allowed": false
    },
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/convergence.schema.json",
  "authority": false,
  "semantic_change": false
}
```

Forbidden behavior:

- no certification
- no proof declaration
- no authority transfer

---

## 13. Endpoint: Fetch Convergence Record

```http
GET /v0.1/convergences/{convergence_id}
```

Response binds to:

```text
https://crp.local/schemas/v0.1/convergence.schema.json
```

Response example:

```json
{
  "data": {
    "convergence_id": "convergence_001",
    "layer": "CONVERGENCE",
    "aggregation_id": "aggregation_001",
    "aligned_record": {},
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/convergence.schema.json",
  "authority": false,
  "semantic_change": false
}
```

---

## 14. Endpoint: Create Floor Interface View

```http
POST /v0.1/floor-interfaces
```

Schema binding:

```text
https://crp.local/schemas/v0.1/floor-interface.schema.json
```

Idempotency key:

```text
floor_id
```

Request example:

```json
{
  "floor_id": "floor_001",
  "layer": "FLOOR_INTERFACE",
  "convergence_id": "convergence_001",
  "exposed_record": {
    "view": "structural_only"
  },
  "floor_notice": "This interface exposes evidence. It does not interpret evidence.",
  "authority": false,
  "semantic_change": false
}
```

Response example:

```json
{
  "data": {
    "floor_id": "floor_001",
    "layer": "FLOOR_INTERFACE",
    "convergence_id": "convergence_001",
    "exposed_record": {
      "view": "structural_only"
    },
    "floor_notice": "This interface exposes evidence. It does not interpret evidence.",
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/floor-interface.schema.json",
  "authority": false,
  "semantic_change": false
}
```

Forbidden behavior:

- no verified badge
- no endorsed view
- no hidden interpretation

---

## 15. Endpoint: Fetch Floor Interface View

```http
GET /v0.1/floor-interfaces/{floor_id}
```

Response binds to:

```text
https://crp.local/schemas/v0.1/floor-interface.schema.json
```

Response example:

```json
{
  "data": {
    "floor_id": "floor_001",
    "layer": "FLOOR_INTERFACE",
    "convergence_id": "convergence_001",
    "exposed_record": {},
    "floor_notice": "This interface exposes evidence. It does not interpret evidence.",
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/floor-interface.schema.json",
  "authority": false,
  "semantic_change": false
}
```

---

## 16. Endpoint: Submit Observer Statement

```http
POST /v0.1/observers
```

Schema binding:

```text
https://crp.local/schemas/v0.1/observer.schema.json
```

Idempotency key:

```text
observer_id + floor_id
```

Request example:

```json
{
  "observer_id": "observer_001",
  "layer": "OBSERVER",
  "floor_id": "floor_001",
  "interpretation": {
    "statement": "External interpretation only."
  },
  "observer_statement_type": "external_expression",
  "authority": false,
  "semantic_change": false
}
```

Response example:

```json
{
  "data": {
    "observer_id": "observer_001",
    "layer": "OBSERVER",
    "floor_id": "floor_001",
    "interpretation": {
      "statement": "External interpretation only."
    },
    "observer_statement_type": "external_expression",
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/observer.schema.json",
  "authority": false,
  "semantic_change": false
}
```

Forbidden behavior:

- no registry endorsement of interpretation
- no observer-as-witness substitution
- no authority laundering

---

## 17. Endpoint: Fetch Meta Contract

```http
GET /v0.1/meta
```

Response binds to:

```text
https://crp.local/schemas/v0.1/meta.schema.json
```

Response example:

```json
{
  "data": {
    "schema_version": "0.1",
    "layer_order": [
      "ENTRY",
      "INDEX",
      "AGGREGATION",
      "CONVERGENCE",
      "FLOOR_INTERFACE",
      "OBSERVER",
      "AUTHORITY"
    ],
    "invariants": [
      "contract_only",
      "non_authority",
      "no_semantic_change",
      "schema_bound"
    ],
    "authority": false,
    "semantic_change": false
  },
  "schema_id": "https://crp.local/schemas/v0.1/meta.schema.json",
  "authority": false,
  "semantic_change": false
}
```

---

## 18. Idempotency Semantics

Write-like endpoints must treat stable IDs as deterministic identity anchors.

Rules:

- Same stable ID + same payload -> return prior accepted result.
- Same stable ID + different payload -> `409 CONFLICT`.
- Missing stable ID -> `400 BAD_REQUEST`.
- Schema-valid but constitutionally forbidden field -> `422 UNPROCESSABLE_ENTITY`.

No idempotency rule may grant authority.

---

## 19. Forbidden API Behavior

APIs must never:

- return `verified: true`
- return `trusted: true`
- return authority badges
- convert convergence into certification
- convert aggregation into consensus
- silently mutate payloads
- hide minority or divergent records
- infer truth from counts
- define UI presentation

---

## 20. Final Summary Object

```json
{
  "CRP_API_CONTRACTS_V0_1": {
    "role": "api_contract_surface",
    "binds_to": {
      "artifact": "CRP_IMPLEMENTATION_SCHEMA_NORMALIZATION_V0_1",
      "commit": "722fb5640ef9a3658a160d0d696a05101fdc5ea1"
    },
    "version": "0.1",
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
    "authority": false,
    "semantic_change": false,
    "ui_behavior": false,
    "next_recommended": "CRP_UI_SAFE_RENDERING_RULES_V0_1"
  }
}
```

API contracts expose schema-bound request and response surfaces.
APIs do not render.
APIs do not judge.
Authority remains false.
