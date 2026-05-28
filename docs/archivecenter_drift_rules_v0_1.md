# ArchiveCenter Drift Rules V0.1

## Core Invariant
URL_IS_LOCATOR_HASH_IS_IDENTITY

## Kill Switch
NO_SYNTHETIC_POINTER_RECONSTRUCTION

## Rules
1. URL is not identity.
2. Hashes outrank pointers.
3. Missing pointer does not imply missing record.
4. Reindexing is observable drift.
5. Rediscovery requires a new receipt.
6. No synthetic pointer reconstruction.

## Enforcement
- All drift events must emit receipts.
- All receipts must be replay-verifiable.
- No unverified continuity may be inferred.

## Repository Rule
NO_UNVERIFIED_CLAIM_PROMOTION

Meaning:
No jurisdiction, pointer, source, or continuity claim may be promoted unless grounded in repo bytes, source hash, or explicit receipt.

Failure Class:
DRIFT_PROMOTION

Required Behavior:
FAIL_CLOSED
