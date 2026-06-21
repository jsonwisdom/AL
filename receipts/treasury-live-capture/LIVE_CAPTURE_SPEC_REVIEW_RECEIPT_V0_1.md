# Live Capture Spec Review Receipt v0.1

## Status

DRAFT_FOR_REVIEW

## Dependency Chain

TREASURY_VERIFIER_V0_2 = SEALED
WITNESS_KEY_ROTATION_V0_1 = SEALED
TRUST_ROOT_POLICY = LANDED
LIVE_CAPTURE_SPEC_V0_1 = DRAFT
REAL_GENESIS = BLOCKED
NO_FAKE_GREEN = ACTIVE

## First Test Vector

01_fetch_blocked_failure_receipt.json

## Expected Behavior

FETCH_BLOCKED -> FAILURE_RECEIPT_ALLOWED
FETCH_BLOCKED -> STRICT_FAIL
FETCH_BLOCKED -> PROMOTION_BLOCKED

## Ruling

The system may preserve blocked-fetch evidence.

The system must not convert blocked-fetch evidence into a real capture.

No fake green.
