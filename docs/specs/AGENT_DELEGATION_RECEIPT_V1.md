# AGENT_DELEGATION_RECEIPT_V1 Specification

## Version
- receipt_type: AGENT_DELEGATION_RECEIPT_V1
- receipt_version: 1.0.0

## Key Addition
Per-receipt identity material in `proof`:
- `public_key` (preferred, 64-char hex)
- `did` (optional, stub for now)

## Resolution Order
1. proof.public_key
2. proof.did (did:key stub)
3. V0 fallback key

## Errors
- FAIL: public key missing
- FAIL: public key invalid
- FAIL: did resolution unsupported
- FAIL: signature mismatch

## Fixtures
Valid: receipt-public-key-valid.json (real vector)
Invalid: missing-key, invalid-public-key, unsupported-did, tampered-signature

Builds on #294. Part of #295.

Do not inherit trust. Replay it.
