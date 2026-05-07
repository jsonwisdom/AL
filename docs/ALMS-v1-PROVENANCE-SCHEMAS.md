# ALMS-v1-PROVENANCE-SCHEMAS.md

## Autonomous Ledger for Machine & Institutional Sovereignty — Provenance Schemas

```text
DOCUMENT TYPE:    constitutional_surface
EPOCH:            ALMS-v1
EPOCH_OBJECT:     ALMS-v1-EPOCH-0001
PARENT_SURFACES:  ALMS-v1-TREATIES.md
                  ALMS-v1-REGISTRY-CHARTER.md
                  ALMS-v1-COURT-PROCEDURE.md
EXTENSION_RULE:   EXTEND_ONLY
V0_MUTATION:      false
STATUS:           CANONICAL
DEPENDS_ON:       Treaty I.2, II.2, II.3, III.1, III.2
SCHEMA_FORMAT:    JSON_SCHEMA_2020_12
```

## Preamble

This document defines the canonical provenance schemas for all ALMS v1 claims. It operationalizes Treaty I.2 (Provenance Completeness) and Treaty II.3 (Provenance Schemas) by specifying exact JSON Schema 2020-12 definitions, determinism class requirements, environment specification depth rules, and JCS canonicalization procedures.

A provenance record that does not satisfy the applicable schema defined here is structurally incomplete. A structurally incomplete provenance record renders the claim inadmissible without requiring replay. This is not a judgment of truth — it is a classification.

The governing principle for schema design in ALMS v1:

> An operator may declare a weaker determinism class, but may not claim a stronger one unless the required environment specification depth for that class is fully satisfied.

Overclaiming determinism is a provenance forgery.

## Part I — Common Fields

### Schema 1.1 — Common Provenance Fields

All ALMS v1 provenance records must include common fields for epoch, claim type, claim hash, operator identity, registry identity, timestamp, parent receipts, and provenance hash.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://alms.constitutional/v1/schemas/common-provenance",
  "title": "ALMS v1 Common Provenance Fields",
  "type": "object",
  "required": [
    "epoch",
    "claim_type",
    "claim_hash",
    "operator_id",
    "registry_id",
    "timestamp_utc",
    "parent_receipts",
    "provenance_hash"
  ],
  "properties": {
    "epoch": { "type": "string", "const": "ALMS-v1" },
    "claim_type": { "type": "string", "enum": ["M", "I"] },
    "claim_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "operator_id": { "type": "string", "minLength": 1 },
    "registry_id": { "type": "string", "minLength": 1 },
    "timestamp_utc": { "type": "integer", "minimum": 0 },
    "parent_receipts": {
      "type": "array",
      "items": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" }
    },
    "provenance_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" }
  }
}
```

### Schema 1.2 — Claim Identity Construction

```text
CLAIM_ID = "alms-v1:" + base64url(sha256(JCS(provenance_record)))
```

Two claims with identical content but different provenance records have different CLAIM_IDs.

## Part II — Schema M: Machine-Generated Claim Provenance

### Schema 2.1 — Determinism Class Ladder

```text
CLASS             GUARANTEE                           ENV_SPEC_DEPTH
NONDETERMINISTIC  No replay guarantee                 none_required
SEEDED            Seeded equivalent replay            shallow
REPLAYABLE        Input and dependency equivalent      shallow_plus_dependency_hashes
DETERMINISTIC     Bit-identical under environment      deep
TEE_BOUND         Verified TEE execution              deep_plus_tee_attestation
COURT_ADMISSIBLE  Court-ready resolved provenance      deep_plus_registry_resolution
```

An operator may declare a weaker class than execution warrants. They may not declare a stronger class than their environment specification supports.

### Schema 2.2 — Environment Specification Depths

Minimum depth by determinism class:

```text
NONDETERMINISTIC       none_required
SEEDED                 shallow
REPLAYABLE             shallow_plus_dependency_hashes
DETERMINISTIC          deep
TEE_BOUND              deep_plus_tee_attestation
COURT_ADMISSIBLE       deep_plus_registry_resolution
```

A verifier must reject before replay if `environment_spec.depth_class` does not meet the required minimum for the declared `determinism_class`.

### Schema 2.3 — Complete Schema M

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://alms.constitutional/v1/schemas/provenance-m",
  "title": "ALMS v1 Schema M: Machine-Generated Claim Provenance",
  "type": "object",
  "allOf": [
    { "$ref": "https://alms.constitutional/v1/schemas/common-provenance" }
  ],
  "required": [
    "model_id",
    "model_hash",
    "input_hash",
    "determinism_class",
    "environment_spec",
    "execution_log_hash"
  ],
  "properties": {
    "claim_type": { "type": "string", "const": "M" },
    "model_id": { "type": "string", "minLength": 1 },
    "model_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "input_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "input_refs": { "type": "array", "items": { "type": "string" } },
    "determinism_class": {
      "type": "string",
      "enum": ["NONDETERMINISTIC", "SEEDED", "REPLAYABLE", "DETERMINISTIC", "TEE_BOUND", "COURT_ADMISSIBLE"]
    },
    "equivalence_class": {
      "type": "object",
      "required": ["class_id", "class_spec_hash", "class_spec_ref"],
      "properties": {
        "class_id": { "type": "string" },
        "class_spec_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
        "class_spec_ref": { "type": "string" }
      }
    },
    "environment_spec": {
      "type": "object",
      "required": ["depth_class"],
      "properties": {
        "depth_class": {
          "type": "string",
          "enum": ["none_required", "shallow", "shallow_plus_dependency_hashes", "deep", "deep_plus_tee_attestation", "deep_plus_registry_resolution"]
        }
      }
    },
    "execution_log_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "output_format": { "type": "string" }
  },
  "if": { "properties": { "determinism_class": { "enum": ["NONDETERMINISTIC", "SEEDED"] } } },
  "then": { "required": ["equivalence_class"] }
}
```

## Part III — Schema I: Institution-Generated Claim Provenance

### Schema 3.1 — Complete Schema I

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://alms.constitutional/v1/schemas/provenance-i",
  "title": "ALMS v1 Schema I: Institution-Generated Claim Provenance",
  "type": "object",
  "allOf": [
    { "$ref": "https://alms.constitutional/v1/schemas/common-provenance" }
  ],
  "required": [
    "authority_id",
    "decision_process",
    "quorum_record",
    "input_refs",
    "jurisdiction",
    "institutional_class"
  ],
  "properties": {
    "claim_type": { "type": "string", "const": "I" },
    "authority_id": { "type": "string", "minLength": 1 },
    "institutional_class": {
      "type": "string",
      "enum": ["DECISION", "RULING", "VOTE", "POLICY", "CERTIFICATION", "ATTESTATION", "REVOCATION", "AMENDMENT"]
    },
    "decision_process": {
      "type": "object",
      "required": ["process_id", "process_spec_hash"],
      "properties": {
        "process_id": { "type": "string" },
        "process_spec_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
        "process_version": { "type": "string" }
      }
    },
    "quorum_record": {
      "type": "object",
      "required": ["quorum_threshold", "participant_count", "participant_identity_hashes", "attestation_hashes"],
      "properties": {
        "quorum_threshold": { "type": "string", "pattern": "^[0-9]+/[0-9]+$" },
        "participant_count": { "type": "integer", "minimum": 1 },
        "participating_count": { "type": "integer", "minimum": 1 },
        "participant_identity_hashes": { "type": "array", "items": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" }, "minItems": 1 },
        "attestation_hashes": { "type": "array", "items": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" }, "minItems": 1 },
        "quorum_met": { "type": "boolean" }
      }
    },
    "input_refs": { "type": "array", "items": { "type": "string" } },
    "deliberation_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "jurisdiction": {
      "type": "object",
      "required": ["registry_id", "namespace", "court_id"],
      "properties": {
        "registry_id": { "type": "string" },
        "namespace": { "type": "string" },
        "court_id": { "type": "string" }
      }
    },
    "supersedes": { "type": "array", "items": { "type": "string" } }
  },
  "if": { "properties": { "institutional_class": { "enum": ["RULING", "DECISION", "POLICY"] } } },
  "then": { "required": ["deliberation_hash"] }
}
```

### Schema 3.2 — Institutional Class Quorum Requirements

```text
DECISION       2/3      deliberation required
RULING         2/3      deliberation required
VOTE           1/2 + 1  no deliberation required
POLICY         2/3      deliberation required
CERTIFICATION  1/1      no deliberation required
ATTESTATION    1/1      no deliberation required
REVOCATION     2/3      no deliberation required
AMENDMENT      3/4      deliberation required
```

A quorum record that does not satisfy the minimum for the declared institutional class is provenance forgery. The claim is inadmissible without replay.

## Part IV — JCS Canonicalization Procedure

All ALMS v1 provenance record hashes use JCS (RFC 8785) and SHA-256.

Procedure:

1. Construct complete provenance record with all required and optional fields populated.
2. Set `provenance_hash` to the empty string `""`.
3. Apply JCS.
4. Apply SHA-256.
5. Encode lowercase hexadecimal and prefix with `sha256:`.
6. Populate `provenance_hash`.

To verify: copy the record, set `provenance_hash` to `""`, re-hash, and compare.

## Part V — Provenance Refusal Reasons

```text
PROV-001 MISSING_REQUIRED_FIELD
PROV-002 SCHEMA_VALIDATION_FAILED
PROV-003 CLAIM_HASH_MISMATCH
PROV-004 PROVENANCE_HASH_MISMATCH
PROV-005 OPERATOR_NOT_ACTIVE
PROV-006 REGISTRY_CHAIN_INVALID
PROV-007 DETERMINISM_CLASS_ENV_MISMATCH
PROV-008 EQUIVALENCE_CLASS_MISSING
PROV-009 EQUIVALENCE_CLASS_SPEC_NON_EXECUTABLE
PROV-010 TAINTED_PARENT
PROV-011 LINEAGE_CYCLE_DETECTED
PROV-012 QUORUM_NOT_MET
PROV-013 DELIBERATION_HASH_ABSENT
PROV-014 EXECUTION_LOG_UNRETRIEVABLE
PROV-015 TIMESTAMP_BEFORE_STANDING
PROV-016 EPOCH_MISMATCH
```

Multiple refusal codes may apply simultaneously.

## Appendix A — Schema M Worked Example

```json
{
  "epoch": "ALMS-v1",
  "claim_type": "M",
  "claim_hash": "sha256:a3f1c2d4e5b6789012345678901234567890abcdef1234567890abcdef123456",
  "operator_id": "op.inference.lab-42",
  "registry_id": "reg.infrastructure.builds",
  "timestamp_utc": 1748000000,
  "parent_receipts": ["sha256:b1c2d3e4f5a6789012345678901234567890abcdef1234567890abcdef123456"],
  "model_id": "llm-pipeline-v3.2.1",
  "model_hash": "sha256:c2d3e4f5a6b7890123456789012345678901abcdef234567890abcdef1234567",
  "input_hash": "sha256:d3e4f5a6b7c8901234567890123456789012bcdef34567890abcdef12345678",
  "determinism_class": "REPLAYABLE",
  "environment_spec": {
    "depth_class": "shallow_plus_dependency_hashes",
    "os_name": "Ubuntu",
    "os_version": "24.04",
    "runtime_name": "Python",
    "runtime_version": "3.12.3",
    "dependency_manifest_hash": "sha256:e4f5a6b7c8d9012345678901234567890123cdef456789abcdef0123456789ab",
    "dependency_lock_hash": "sha256:f5a6b7c8d9e0123456789012345678901234def5678901bcdef012345678901c"
  },
  "execution_log_hash": "sha256:a6b7c8d9e0f1234567890123456789012345ef678901cdef0123456789012345",
  "output_format": "application/json",
  "provenance_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
}
```

The example provenance_hash is a placeholder. Real records compute it with `provenance_hash` set to `""`.

## Appendix B — Schema Invariants

```text
SCHEMA-INV-001  An operator may not declare a stronger determinism_class than their environment_spec depth supports.
SCHEMA-INV-002  Provenance hashes are computed by JCS (RFC 8785) + SHA-256.
SCHEMA-INV-003  Schema validation failure makes the claim inadmissible without replay.
SCHEMA-INV-004  Taint in any parent_receipt propagates to the child claim unless court-limited.
SCHEMA-INV-005  Equivalence class specifications must be formally executable.
SCHEMA-INV-006  Multiple provenance refusal codes may apply simultaneously.
SCHEMA-INV-007  Execution logs must be retained and retrievable for the full admissibility period.
SCHEMA-INV-008  Schema I quorum floors are constitutional; stricter authority ceilings are allowed.
SCHEMA-INV-009  All hash fields use `sha256:<64 lowercase hex>`.
SCHEMA-INV-010  The provenance_hash sentinel during computation is the empty string `""`.
```

End of ALMS-v1-PROVENANCE-SCHEMAS.md
