# Pending Claims Protocol v1

**Artifact:** `PENDING_CLAIMS_PROTOCOL_V1`  
**Status:** `SEALED_SPEC_DRAFT`  
**Context:** Lineage / CBREv1 / Sovereign Review

## Purpose

The pending claims log is an evidence aggregation layer. It records claims that passed initial mechanical gates but have not yet been sovereignly adopted into `asset_lineage_events.jsonl`.

The pending log is not sovereign memory.
The pending log is not a cache.
The pending log is an evidence record.

## Files

```text
lineage/pending_asset_claims.jsonl
lineage/asset_lineage_events.jsonl
```

`pending_asset_claims.jsonl` records received, verified, and coalesced claims.
`asset_lineage_events.jsonl` records adopted sovereign memory only.

## Core Rule

```text
VERIFIED_TRACE = PENDING_CLAIM
ADOPTION_SIGNAL = LINEAGE_BINDING
NO_ADOPTION = NO_PERMANENT_STATE_CHANGE
```

## Coalesce / Merge Protocol

When a claim arrives:

```text
IDENTICAL ASSET_HASH + NEW ORIGIN:
  → Skip CBRE verification if trace hash and output commitment are identical to an already verified pending claim.
  → Verify the new branch manifest signature independently.
  → Add the new branch as an additional attestor.
  → Preserve all attestors.
  → Return COALESCED.

IDENTICAL ASSET_HASH + IDENTICAL ORIGIN:
  → Treat as duplicate.
  → Do not add new evidence unless manifest_hash or signature differs.
  → Return DUPLICATE_CLAIM.

DIFFERENT ASSET_HASH + SAME ASSET_ID:
  → Do not overwrite.
  → Record as competing pending claim.
  → Return SOVEREIGN_REVIEW_REQUIRED.
```

## Why Coalescing Exists

Duplicate bytes from different branches are not duplicate evidence.
They are corroboration.

If Branch A and Branch B attest to the same asset hash, both attestations must remain visible. If one branch is later compromised, the other attestation may preserve evidentiary continuity.

## Pending Claim Shape

```json
{
  "asset_id": "doc:shared-research-042",
  "asset_hash": "sha256:<64hex>",
  "trace_hash": "sha256:<64hex>",
  "output_commitment": "sha256:<64hex>",
  "trace_status": "VERIFIED_TRACE",
  "trace_verified_at": "2026-05-07T10:00:00Z",
  "attestors": [
    {
      "branch_id": "E1-PRIME",
      "manifest_hash": "sha256:<64hex>",
      "signature": "<signature>",
      "timestamp_utc": "2026-05-07T10:00:00Z"
    }
  ],
  "adoption_status": "ELIGIBLE"
}
```

## Required Result States

```text
PENDING_CLAIM_CREATED
COALESCED
DUPLICATE_CLAIM
SOVEREIGN_REVIEW_REQUIRED
REJECTED_MANIFEST_SIGNATURE
REJECTED_TRACE
```

## Constitutional Boundary

The pending log may strengthen evidence.
It may not bind sovereign memory.

Only an explicit adoption signal may append to `asset_lineage_events.jsonl`.

## Final Law

```text
Corroboration is not duplication.
Verified math is not adoption.
Pending evidence is not sovereign memory.
```
