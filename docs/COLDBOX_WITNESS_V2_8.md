# ColdBox Witness v2.8

Purpose: provide a sovereignty-first third witness without pretending third-party decentralization exists yet.

## Invariants

- ColdBox key is separate from Jay and Node8 online keys.
- ColdBox signs only witness receipts, never semantic truth claims.
- `authority=false` is mandatory.
- No `v2.8-live` tag without a consensus attestation.

## Procedure

1. Copy the replay bundle to ColdBox using removable media.
2. Run replay verification offline.
3. Confirm `status=PASS`, `authority=false`, and state root matches local output.
4. Sign or prepare the EAS attestation payload offline.
5. Broadcast from an online relay without exposing the ColdBox private key.
6. Record the ColdBox attestation UID in the v2.8 manifest.

## Halt conditions

- State root mismatch.
- Missing witness UID.
- Any witness reports `authority=true`.
- Any witness reports non-PASS status.
- Threshold below 2-of-3.
