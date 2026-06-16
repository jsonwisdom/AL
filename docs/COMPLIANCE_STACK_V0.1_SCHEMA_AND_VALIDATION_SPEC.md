# Compliance Stack v0.1 — Schema and Validation Specification

**Artifact:** COMPLIANCE_STACK_V0.1_SCHEMA_AND_VALIDATION_SPEC  
**Related Technical Artifact:** `docs/CONSTITUTIONAL_COMPLIANCE_STACK_V0.1.md`  
**Related Legislative Artifact:** `docs/BEHAVIORAL_SYSTEMS_ACCOUNTABILITY_ACT_V0.5.md`  
**Related Litigation Artifact:** `docs/BSAA_V0.5_LITIGATION_RISK_MAP_BRANCH_C.md`  
**Doctrine:** REPLAY_FIRST_SCALE_LATER  
**Status:** Concrete Artifact Layer • Validation Surface v0.1

## 1. Purpose

This document defines the first concrete schema and validation layer for the Constitutional Compliance Stack v0.1.

The goal is to convert compliance claims into deterministic, machine-verifiable artifacts:

- Optimization Disclosures;
- Mitigation Receipts;
- Eligibility Proof Receipts;
- Replay Ledger Events;
- Canonicalization and signature envelopes.

The governing invariant is:

> Compliance is replayable computational accountability, not paperwork.

## 2. Validation Principles

All artifacts must satisfy the following requirements:

1. **Deterministic canonicalization** — equivalent objects serialize identically.
2. **Explicit versioning** — schema and receipt versions must be declared.
3. **Stable event vocabulary** — event classes must match canonical enumerations.
4. **Cryptographic signatures** — signed payloads must identify algorithm and signer commitment.
5. **Privacy boundary checks** — no raw private content, direct messages, government ID scans, full birthdates, or persistent cross-platform identifiers.
6. **Replay-safe timestamps** — timestamps must be UTC ISO-8601 strings.
7. **Algorithm agility** — signature and hash algorithms must be declared.

## 3. Canonical Event Vocabulary

Allowed `event_type` values:

- POLICY_DEPLOYMENT
- MITIGATION_DEPLOYMENT
- MITIGATION_ROLLBACK
- AUDIT_REQUEST
- AUDIT_RESPONSE
- SAFETY_CONSTRAINT_UPDATE
- AGE_PROOF_VERIFICATION
- ESCALATION_GRADIENT_ALERT
- RESEARCH_ACCESS_GRANT
- RESEARCH_ACCESS_REVOCATION
- PORTABILITY_EXPORT
- PORTABILITY_IMPORT

## 4. Common Signature Envelope

```json
{
  "algorithm": "ed25519",
  "signed_by": "platform_signing_key_commitment",
  "signature_value": "base64url_signature",
  "signed_at": "2027-01-01T00:00:00Z",
  "canonicalization": "JCS-RFC8785",
  "hash_algorithm": "sha256"
}
```

### Rules

- `algorithm` MUST be declared.
- `canonicalization` MUST be declared.
- `signed_at` MUST be UTC ISO-8601.
- `signature_value` MUST be computed over the canonicalized payload excluding the `signature` field.

## 5. Mitigation Receipt — Draft JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jsonwisdom.example/schemas/mitigation-receipt-v0.1.json",
  "title": "MitigationReceiptV01",
  "type": "object",
  "required": [
    "receipt_version",
    "receipt_type",
    "platform_id",
    "mitigation_id",
    "deployment_epoch",
    "target_cohort",
    "objective_constraints",
    "observed_effects",
    "rollback_available",
    "policy_hash",
    "signature"
  ],
  "properties": {
    "receipt_version": { "const": "0.1" },
    "receipt_type": { "const": "MITIGATION_DEPLOYMENT" },
    "platform_id": { "type": "string", "minLength": 8 },
    "mitigation_id": { "type": "string", "pattern": "^[A-Z0-9_\\-]+$" },
    "deployment_epoch": { "type": "string" },
    "target_cohort": {
      "type": "object",
      "required": ["age_range", "jurisdiction"],
      "properties": {
        "age_range": { "enum": ["UNDER_13", "13_17", "OVER_18", "UNKNOWN"] },
        "jurisdiction": { "type": "string" }
      },
      "additionalProperties": false
    },
    "objective_constraints": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "observed_effects": {
      "type": "object",
      "additionalProperties": { "type": ["number", "string", "boolean"] }
    },
    "rollback_available": { "type": "boolean" },
    "policy_hash": { "type": "string", "pattern": "^sha256:[a-fA-F0-9]{64}$" },
    "signature": { "$ref": "#/$defs/signatureEnvelope" }
  },
  "additionalProperties": false,
  "$defs": {
    "signatureEnvelope": {
      "type": "object",
      "required": ["algorithm", "signed_by", "signature_value", "signed_at", "canonicalization", "hash_algorithm"],
      "properties": {
        "algorithm": { "enum": ["ed25519"] },
        "signed_by": { "type": "string" },
        "signature_value": { "type": "string" },
        "signed_at": { "type": "string", "format": "date-time" },
        "canonicalization": { "const": "JCS-RFC8785" },
        "hash_algorithm": { "const": "sha256" }
      },
      "additionalProperties": false
    }
  }
}
```

## 6. Optimization Disclosure — Draft Shape

```json
{
  "disclosure_version": "0.1",
  "disclosure_type": "OPTIMIZATION_DISCLOSURE",
  "platform_id": "platform_hash",
  "objective_id": "engagement_v4",
  "optimization_targets": [
    "session_duration",
    "return_frequency"
  ],
  "safety_constraints": [
    "minor_night_limit",
    "escalation_gradient_cap"
  ],
  "ranking_modes": [
    "chronological",
    "personalized"
  ],
  "deployment_window": "2027-Q1",
  "policy_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "signature": {
    "algorithm": "ed25519",
    "signed_by": "platform_signing_key_commitment",
    "signature_value": "base64url_signature",
    "signed_at": "2027-01-01T00:00:00Z",
    "canonicalization": "JCS-RFC8785",
    "hash_algorithm": "sha256"
  }
}
```

## 7. Eligibility Proof Receipt — Draft Shape

```json
{
  "receipt_version": "0.1",
  "receipt_type": "AGE_RANGE_PROOF",
  "range": "13_17",
  "proof_system": "zk_snark_v3",
  "issuer_commitment": "issuer_hash_commitment",
  "expires_at": "2027-06-01T00:00:00Z",
  "linkable": false,
  "revocable": true,
  "discloses_legal_identity": false,
  "signature": {
    "algorithm": "ed25519",
    "signed_by": "attestor_key_commitment",
    "signature_value": "base64url_signature",
    "signed_at": "2027-01-01T00:00:00Z",
    "canonicalization": "JCS-RFC8785",
    "hash_algorithm": "sha256"
  }
}
```

### Privacy Boundary

The following fields are forbidden in eligibility proof receipts:

- legal_name;
- full_birthdate;
- government_id_number;
- address;
- biometric_template;
- persistent_cross_platform_identifier.

## 8. Replay Ledger Event — Draft Shape

```json
{
  "event_version": "0.1",
  "event_type": "MITIGATION_DEPLOYMENT",
  "event_id": "sha256:event_hash",
  "parent_event_id": "sha256:previous_event_hash",
  "platform_id": "platform_hash",
  "occurred_at": "2027-01-01T00:00:00Z",
  "artifact_hash": "sha256:artifact_hash",
  "schema_id": "mitigation-receipt-v0.1",
  "signature": {
    "algorithm": "ed25519",
    "signed_by": "platform_signing_key_commitment",
    "signature_value": "base64url_signature",
    "signed_at": "2027-01-01T00:00:00Z",
    "canonicalization": "JCS-RFC8785",
    "hash_algorithm": "sha256"
  }
}
```

## 9. Deterministic Validation Flow

Validation MUST occur in this order:

1. Parse JSON.
2. Reject duplicate keys.
3. Validate against declared schema.
4. Enforce privacy boundary checks.
5. Remove `signature` field for signing payload.
6. Canonicalize using JCS-RFC8785.
7. Compute SHA-256 hash of canonical payload.
8. Verify signature against declared signer commitment.
9. Verify event lineage if parent hash is present.
10. Emit validation result.

## 10. Validation Result Shape

```json
{
  "validation_version": "0.1",
  "valid": true,
  "artifact_type": "MITIGATION_DEPLOYMENT",
  "artifact_hash": "sha256:artifact_hash",
  "schema_id": "mitigation-receipt-v0.1",
  "signature_valid": true,
  "privacy_boundary_passed": true,
  "lineage_valid": true,
  "errors": []
}
```

## 11. Forbidden Mutation Rules

A schema successor MUST NOT introduce:

- viewpoint labels as validation fields;
- ideological harm classifications;
- raw user content disclosure requirements;
- permanent identity custody requirements;
- proprietary-only validation dependencies;
- mandatory platform-specific identity providers;
- non-deterministic validation steps.

## 12. Canonical Close

This specification is the first validation surface for Constitutional Compliance Stack v0.1.

It converts compliance from narrative assertion into replayable, deterministic verification.

**Anchor Lane:** CLOSED  
**Replay Cell:** PRESERVED • REPLAYABLE • DETERMINISTIC
