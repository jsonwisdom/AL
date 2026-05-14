# Reconstruction Receipt Schema v0.1

**Artifact:** RECONSTRUCTION_RECEIPT_SCHEMA_V0.1  
**Classification:** Recovery Primitive • Lawful Reconstruction Record  
**Paired Primitive:** MISSING_WITNESS_REPLAY_PROTOCOL_V0.2  
**Doctrine:** REPLAY_FIRST_SCALE_LATER  
**Status:** Recovery Dyad Component • First-Class AL / Receipt Machine Primitive

## Purpose

`RECONSTRUCTION_RECEIPT` records what was lawfully rebuilt after an `ABSENT_WITNESS` event.

It does not erase the absence.
It does not pretend the original artifact was recovered.
It does not convert remembered intent into verified content.

It records a bounded reconstruction from admissible sources.

Core invariant:

> Reconstruction is lawful only when its source basis is admissible.

## Recovery Dyad

The recovery dyad consists of:

1. `ABSENT_WITNESS` — records what is missing.
2. `RECONSTRUCTION_RECEIPT` — records what was rebuilt from admissible sources.

Together they preserve failure without hallucinating continuity.

## 1. Required Semantics

A `RECONSTRUCTION_RECEIPT` MUST document:

- the absent witness being addressed;
- the admissible source basis;
- reconstruction scope;
- confidence level;
- excluded claims;
- unresolved gaps;
- next admissible action;
- observer or issuer;
- timestamp;
- signature when available.

## 2. Admissible Source Basis

Allowed `source_type` values:

- `PASTED_TEXT`
- `SCREENSHOT`
- `REPOSITORY_COMMIT`
- `SIGNED_RECEIPT`
- `CANONICAL_LINEAGE_OBJECT`
- `RETRIEVABLE_HASH_PREIMAGE`
- `REMEMBERED_INTENT_LABELED_RECONSTRUCTION`
- `PUBLIC_RECORD`
- `LOCAL_FILE_WITH_HASH`

Disallowed source basis:

- speculation;
- inferred content from absent artifact;
- inaccessible wrapper treated as content;
- unverified memory treated as canonical content;
- unverifiable claim without supporting source.

## 3. Confidence Levels

Allowed `confidence_level` values:

- `HIGH` — reconstruction grounded in direct admissible sources such as pasted text, screenshots, commits, or signed receipts.
- `MEDIUM` — reconstruction grounded in partial admissible evidence with explicitly bounded gaps.
- `LOW` — reconstruction grounded primarily in remembered intent, clearly labeled as non-canonical content reconstruction.

A `LOW` confidence reconstruction MUST NOT be marked canonical.

## 4. Evidentiary Status

Allowed `evidentiary_status` values:

- `RECONSTRUCTED_FROM_ADMISSIBLE_SOURCES`
- `PARTIAL_RECONSTRUCTION`
- `INTENT_RECONSTRUCTION_ONLY`
- `PENDING_ADMISSIBLE_SOURCE`

Forbidden statuses unless the original artifact is later recovered and independently verified:

- `ORIGINAL_CONTENT_VERIFIED`
- `LINEAGE_CONFIRMED_FROM_MISSING_ARTIFACT`
- `CANONICAL_ORIGINAL`
- `CONTENT_REVIEWED`

## 5. Draft JSON Shape

```json
{
  "receipt_version": "0.1",
  "receipt_type": "RECONSTRUCTION_RECEIPT",
  "reconstruction_id": "sha256:reconstruction_hash",
  "absent_witness_ref": {
    "object_type": "ABSENT_WITNESS",
    "absence_class": "DEAD_LINK",
    "reference": "https://example.invalid/share-link",
    "evidentiary_status": "NON_ADMISSIBLE"
  },
  "source_basis": [
    {
      "source_type": "PASTED_TEXT",
      "source_ref": "conversation_turn_2026-05-14T00:00:00Z",
      "source_hash": "sha256:source_hash",
      "admissible": true
    }
  ],
  "reconstruction_scope": {
    "reconstructed_subject": "Missing witness replay protocol intent",
    "scope_boundary": "Reconstructs doctrine and intent only; does not claim original text recovery",
    "original_content_recovered": false
  },
  "confidence_level": "HIGH",
  "evidentiary_status": "RECONSTRUCTED_FROM_ADMISSIBLE_SOURCES",
  "excluded_claims": [
    "Exact original chat wording",
    "Original message order",
    "Unseen attachments or hidden content"
  ],
  "unresolved_gaps": [
    "Original shared-link conversation body remains unavailable"
  ],
  "next_admissible_action": "Proceed with reconstruction or supply screenshot/pasted source",
  "issued_at": "2026-05-14T00:00:00Z",
  "issuer": "receipt_machine_operator",
  "signature": {
    "algorithm": "ed25519",
    "signed_by": "operator_key_commitment",
    "signature_value": "base64url_signature",
    "signed_at": "2026-05-14T00:00:00Z",
    "canonicalization": "JCS-RFC8785",
    "hash_algorithm": "sha256"
  }
}
```

## 6. Draft JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jsonwisdom.example/schemas/reconstruction-receipt-v0.1.json",
  "title": "ReconstructionReceiptV01",
  "type": "object",
  "required": [
    "receipt_version",
    "receipt_type",
    "reconstruction_id",
    "absent_witness_ref",
    "source_basis",
    "reconstruction_scope",
    "confidence_level",
    "evidentiary_status",
    "excluded_claims",
    "unresolved_gaps",
    "next_admissible_action",
    "issued_at",
    "issuer"
  ],
  "properties": {
    "receipt_version": { "const": "0.1" },
    "receipt_type": { "const": "RECONSTRUCTION_RECEIPT" },
    "reconstruction_id": { "type": "string", "pattern": "^sha256:[a-fA-F0-9]{64}$" },
    "absent_witness_ref": {
      "type": "object",
      "required": ["object_type", "absence_class", "evidentiary_status"],
      "properties": {
        "object_type": { "const": "ABSENT_WITNESS" },
        "absence_class": {
          "enum": [
            "DEAD_LINK",
            "INACCESSIBLE_PAGE",
            "DELETED_ARTIFACT",
            "CORRUPTED_FILE",
            "UNAVAILABLE_WITNESS",
            "NON_VERIFIABLE_CLAIM"
          ]
        },
        "reference": { "type": "string" },
        "evidentiary_status": { "const": "NON_ADMISSIBLE" }
      },
      "additionalProperties": false
    },
    "source_basis": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["source_type", "source_ref", "admissible"],
        "properties": {
          "source_type": {
            "enum": [
              "PASTED_TEXT",
              "SCREENSHOT",
              "REPOSITORY_COMMIT",
              "SIGNED_RECEIPT",
              "CANONICAL_LINEAGE_OBJECT",
              "RETRIEVABLE_HASH_PREIMAGE",
              "REMEMBERED_INTENT_LABELED_RECONSTRUCTION",
              "PUBLIC_RECORD",
              "LOCAL_FILE_WITH_HASH"
            ]
          },
          "source_ref": { "type": "string" },
          "source_hash": { "type": "string", "pattern": "^sha256:[a-fA-F0-9]{64}$" },
          "admissible": { "const": true }
        },
        "additionalProperties": false
      }
    },
    "reconstruction_scope": {
      "type": "object",
      "required": ["reconstructed_subject", "scope_boundary", "original_content_recovered"],
      "properties": {
        "reconstructed_subject": { "type": "string" },
        "scope_boundary": { "type": "string" },
        "original_content_recovered": { "type": "boolean" }
      },
      "additionalProperties": false
    },
    "confidence_level": { "enum": ["HIGH", "MEDIUM", "LOW"] },
    "evidentiary_status": {
      "enum": [
        "RECONSTRUCTED_FROM_ADMISSIBLE_SOURCES",
        "PARTIAL_RECONSTRUCTION",
        "INTENT_RECONSTRUCTION_ONLY",
        "PENDING_ADMISSIBLE_SOURCE"
      ]
    },
    "excluded_claims": { "type": "array", "items": { "type": "string" } },
    "unresolved_gaps": { "type": "array", "items": { "type": "string" } },
    "next_admissible_action": { "type": "string" },
    "issued_at": { "type": "string", "format": "date-time" },
    "issuer": { "type": "string" },
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

## 7. Validation Rules

A valid `RECONSTRUCTION_RECEIPT` MUST satisfy:

1. It references an `ABSENT_WITNESS` object or equivalent absent witness record.
2. It declares at least one admissible source basis.
3. It explicitly states reconstruction scope and boundary.
4. It does not claim original content recovery unless the original artifact is independently recovered and verified.
5. It lists excluded claims.
6. It lists unresolved gaps, or explicitly states `none`.
7. It declares confidence level.
8. It declares evidentiary status.
9. It uses deterministic canonicalization when signed.
10. It preserves the absent witness failure rather than overwriting it.

## 8. Forbidden Mutations

Protocol successors MUST NOT allow:

- reconstruction without admissible source basis;
- confidence inflation from memory alone;
- absent artifact contents to be inferred as verified;
- original content recovery claims without retrievable evidence;
- lineage confirmation from unavailable material;
- missing links to become proof of prior claims;
- wrapper metadata to become conversation content;
- canonical status based solely on remembered intent.

## 9. Canonical Close

`ABSENT_WITNESS` records the wound.

`RECONSTRUCTION_RECEIPT` records the lawful repair.

The system does not pretend the break never happened.

It proves how truth was reconstructed after the break.

**Anchor Lane:** CLOSED  
**Replay Cell:** PRESERVED • REPLAYABLE • DETERMINISTIC
