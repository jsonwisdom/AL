# AGENT_DELEGATION_RECEIPT_V1 Specification

## Version
- receipt_type: AGENT_DELEGATION_RECEIPT_V1
- receipt_version: 1.0.0

## Key Addition vs V0
Per-receipt identity material in `proof`:
- `public_key` preferred, 64-char hex
- `did` optional, for example did:key

## Resolution
Verifiers resolve keys in this order:
1. `proof.public_key` if valid
2. `proof.did` through the V1 resolver stub
3. V0 fallback key only for V0 receipts

V0 fallback key:
`37e9edc1ca6c423ec0955156b9bd318e7581ef4492b28a92235ee900d53174cc`

## Error Strings
- FAIL: public key missing
- FAIL: public key invalid
- FAIL: did resolution unsupported
- FAIL: did resolution failed
- FAIL: signature mismatch

## Fixtures
`testdata/v1/valid/`:
- receipt-public-key-valid.json
- receipt-did-key-valid.json
- binding.json
- policy.json

`testdata/v1/invalid/`:
- receipt-missing-key.json
- receipt-invalid-public-key.json
- receipt-unsupported-did.json
- receipt-tampered-signature.json

## Current Status
As of the V1 branch:
- V1 fixtures are committed
- Python and Node verifiers support V1 key resolution
- Resolver behavior is stubbed for did:key
- V0 compatibility is preserved

## Links
- #295 V1 epic
- #294 V0 Ed25519 baseline

Don’t inherit trust. Replay it. 🧾🔁⚙️
