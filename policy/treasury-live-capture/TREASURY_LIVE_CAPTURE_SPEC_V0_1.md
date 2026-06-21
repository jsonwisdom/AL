# Treasury Live Capture Spec v0.1

## Status

DRAFT_FOR_REVIEW

## Dependencies

TREASURY_VERIFIER_V0_2 = SEALED
WITNESS_KEY_ROTATION_V0_1 = SEALED
TRUST_ROOT_POLICY = LANDED
PROD_WITNESS_QUORUM = 2-of-N
NO_FAKE_GREEN = ACTIVE

## Purpose

Define the live Treasury capture flow from external source payload to normalized payload, signed receipt, witness quorum verification, and strict promotion eligibility.

## Non-Negotiable Boundary

No source fetch means no real capture.

No real capture means no real genesis.

A blocked or failed fetch may produce a failure receipt, but it must not produce a real capture receipt.

## Flow

external_source
  -> raw_payload
  -> raw_payload_hash
  -> deterministic_normalizer
  -> normalized_payload
  -> normalized_payload_hash
  -> unsigned_receipt_canonical_json
  -> witness_keystore_sign(receipt_hash, key_id)
  -> signed_receipt
  -> trust_bundle_verify(policy/witnesses/witnesses.yaml)
  -> quorum_check(2-of-N)
  -> treasury-verifier strict
  -> PASS = eligible_real_capture_receipt
  -> FAIL = failure_receipt_only

## Strict Verification Must Fail If

- source fetch is missing
- fetch status is FETCH_BLOCKED or FETCH_ERROR
- raw payload hash is missing for REAL mode
- normalized payload hash is missing for REAL mode
- receipt hash mismatch occurs
- trust bundle is missing
- quorum is not satisfied
- any signing key is revoked
- any signing key is simulated or staging
- witness public key is not active
- signature verification fails
- timestamp drift exceeds configured limit

## Audit Mode

Audit mode may preserve failed capture evidence.

Audit mode must not promote.

## Acceptance

LIVE_CAPTURE_SPEC_V0_1 = REVIEWED
TRUST_BUNDLE_LOADED = TRUE
PROD_WITNESS_KEYS_ONLY = TRUE
QUORUM = 2-of-N
FETCH_BLOCKED_STRICT_FAIL = TRUE
FAILURE_RECEIPTS_ALLOWED = TRUE
REAL_GENESIS = BLOCKED_UNTIL_FIRST_STRICT_PASS
NO_FAKE_GREEN = ACTIVE
