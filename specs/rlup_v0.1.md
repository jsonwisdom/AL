# Restricted Layer Unlock Protocol v0.1

Status: DESIGN_SPEC_NOT_OPERATIONAL

## Purpose

The Restricted Layer Unlock Protocol (RLUP) defines a membrane-safe access protocol for sensitive public-record mirrors used by AGW / ALMS systems.

RLUP is designed to provide:

- public verifiability
- private or restricted access where required
- no single keyholder
- purpose-bound unlock requests
- audit-visible access decisions
- no ghost anchors
- no implied disclosure

RLUP is not a moderation system, accusation system, leak engine, or authority surface.

## Layers

### Public Layer

The public layer may contain:

- receipt hashes
- verdict codes
- replay status
- Merkle roots
- proof blobs
- public inputs
- non-sensitive metadata

### Restricted Layer

The restricted layer may contain encrypted mirrors of public-record materials such as:

- court PDFs
- docket manifests
- FOIA responses
- canonicalized public records
- versioned restricted manifests

The restricted layer is not a public dropbox and must not accept arbitrary user uploads.

### Unlock Layer

The unlock layer governs controlled access using:

- m-of-n threshold approval
- purpose-bound unlock requests
- requester credentials when applicable
- unlock audit logs
- coercion-visible failure modes

## Unlock Request Shape

```json
{
  "artifact": "RLUP_UNLOCK_REQUEST_V0_1",
  "investigation_id": "string",
  "requester_id": "string",
  "requester_credential_ref": "string",
  "purpose_binding_statement": "string",
  "target_receipt_id": "string",
  "target_ciphertext_ref": "string",
  "requested_scope": "string",
  "request_hash": "sha256:...",
  "state": "REQUESTED"
}
```

## Unlock Verification Requirements

An unlock request may advance only when:

- target receipt exists
- target ciphertext reference exists
- purpose binding is present
- requester credential reference is present where required
- requested scope matches the receipt/ciphertext boundary
- threshold policy is satisfied
- no coercion or emergency lock state is active

## Unlock Decision States

```json
[
  "REQUESTED",
  "UNDER_REVIEW",
  "APPROVED_FOR_THRESHOLD",
  "DENIED_WITH_REASON",
  "REFUSED_INSUFFICIENT_CREDENTIALS",
  "REFUSED_SCOPE_MISMATCH",
  "REFUSED_COERCION_LOCK",
  "UNLOCKED_FOR_PURPOSE",
  "EXPIRED"
]
```

## Coercion Visibility Rule

A coercion event must not silently unlock restricted material.

If coercion lock state is triggered, RLUP may emit a public non-content disclosure:

```json
{
  "artifact": "RLUP_COERCION_VISIBILITY_EVENT_V0_1",
  "target_receipt_id": "string",
  "event_hash": "sha256:...",
  "state": "COERCION_LOCK_ACTIVE",
  "what_was_not_disclosed": ["restricted_content"]
}
```

## Public Audit Log

RLUP public logs may disclose:

- request hash
- target receipt id
- decision state
- timestamp or epoch reference
- threshold status
- what was not concluded

RLUP public logs must not disclose restricted content.

## Non-Claims

RLUP does not assert:

- requester legitimacy as moral fact
- document truth
- guilt
- corruption
- completeness
- entitlement to disclosure
- legal finality

## State

```json
{
  "RLUP": "DESIGN_SPEC_NOT_OPERATIONAL",
  "restricted_unlocks": "BLOCKED_UNTIL_IMPLEMENTED_AND_OPERATOR_APPROVED",
  "no_ghost_anchor": true
}
```
