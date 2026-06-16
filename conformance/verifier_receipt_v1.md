# Verifier Receipt v1

**Artifact:** `VERIFIER_RECEIPT_V1`  
**Status:** `SEALED_SPEC_DRAFT`  
**Protocol Context:** `CBREv1 / VERIFIER v1.2+ / E2-STRICT-CANONICAL`

## Purpose

`VerifierReceiptV1` is the exact object emitted by a CBREv1 verifier and consumed by downstream evidence handlers such as `pending_claims_v1.py`.

It closes the trust seam between:

```text
CBRE VM -> Pending Handler
```

without allowing the verifier to adopt memory or interpret semantics.

## Constitutional Boundary

The verifier proves computation only.

It does not:

- write to `asset_lineage_events.jsonl`,
- write to `pending_asset_claims.jsonl`,
- resolve competing claims,
- parse SSD meaning,
- perform sovereign adoption,
- grant namespace exceptions.

## Required Receipt Shape

```json
{
  "receipt_type": "VERIFIER_RECEIPT_V1",
  "verifier_version": "CBREv1.2+",
  "opcode_table_id": "0x0001",
  "trace_hash": "sha256:<64hex>",
  "trace_status": "VERIFIED_TRACE",
  "output_commitment": "sha256:<64hex>",
  "rejection_reason": null,
  "verified_at_utc": "2026-05-07T00:00:00Z"
}
```

## Field Rules

### `receipt_type`

MUST equal:

```text
VERIFIER_RECEIPT_V1
```

### `verifier_version`

MUST equal the frozen verifier law:

```text
CBREv1.2+
```

### `opcode_table_id`

MUST equal:

```text
0x0001
```

### `trace_hash`

SHA-256 hash of the exact trace bytes submitted to the verifier.

Format:

```text
sha256:<64 lowercase hex chars>
```

### `trace_status`

Allowed values:

```text
VERIFIED_TRACE
REJECTED_TRACE
```

### `output_commitment`

For `VERIFIED_TRACE`, this MUST equal the committed output checked by `OP_COMMIT_OUTPUT`.

For `REJECTED_TRACE`, this MAY be null.

### `rejection_reason`

For `VERIFIED_TRACE`, this MUST be null.

For `REJECTED_TRACE`, this MUST be one of the frozen rejection states:

```text
INTEGRITY: FAILED
MULTIPLE_COMMITS
NO_COMMIT
NO_END
TRAILING_BYTES
DIRTY_STACK
COMMIT_ON_EMPTY_STACK
MALFORMED_PUSH
INVALID_OPCODE
```

### `verified_at_utc`

Timestamp of verifier execution in UTC.

Format:

```text
YYYY-MM-DDTHH:MM:SSZ
```

## Pending Handler Intake Contract

`pending_claims_v1.py` MUST only treat a claim as eligible for pending aggregation when:

```text
verifier_receipt.receipt_type == VERIFIER_RECEIPT_V1
verifier_receipt.verifier_version == CBREv1.2+
verifier_receipt.opcode_table_id == 0x0001
verifier_receipt.trace_status == VERIFIED_TRACE
claim.trace_hash == verifier_receipt.trace_hash
claim.output_commitment == verifier_receipt.output_commitment
```

If any condition fails:

```text
REJECTED_TRACE
```

The pending handler may aggregate evidence only after this contract passes.

## Non-Authority Clause

A valid `VerifierReceiptV1` does not mean:

```text
ADOPTED_MEMORY
VALID_ASSET_MAPPING
NAMESPACE_ACCEPTED
SEMANTIC_AGREEMENT
SOVEREIGN_APPROVAL
```

It means only:

```text
THE TRACE REPLAYED UNDER CBREv1.2+ AND MATCHED ITS COMMITTED OUTPUT.
```

## Core Law

```text
VerifierReceipt proves execution.
Pending Handler aggregates evidence.
Adoption Gate changes memory.
Lineage Log records sovereignty.
```

**VERIFIER_RECEIPT_V1: SEALED_SPEC_DRAFT**
