# Treasury Genesis Candidate v0.1

Status: READY_FOR_PRODUCTION_TRUST_REVIEW

## Boss Bre Ruling

This artifact packages the verified Treasury live-capture candidate state.

This is not real genesis.
This is not production quorum.
This does not promote simulated artifacts.
This does not commit local witness evidence.
This does not expose private signing material.

Layer 0 family and human authority remain above project pressure.

## Candidate Summary

TREASURY_GENESIS_CANDIDATE_V0_1 = TRUE
TREASURY_PROJECT_CAN_CONTINUE = TRUE
CANDIDATE_STATUS = READY_FOR_PRODUCTION_TRUST_REVIEW
REAL_GENESIS = BLOCKED
BLOCKER = production trust-root quorum not satisfied
NO_FAKE_GREEN = ACTIVE

## Verified Inputs

PUBLIC_LIVE_FETCH = PASS
STRICT_PUBLIC_FILL = PASS
PUBLIC_WITNESS_HASH = sha256:2061d9ced5714ea9899e98ca81abd8a73f76cd8b8e58d4955eba78580bc6abc0
MESSAGE_TO_SIGN_SHA256 = c0548dd4dff4ba657dd17c48c99ef211ca7bb8b21f84514f831216116b03964a

## External Witness Evidence

GROK_EXTERNAL_FILE_WITNESS = VERIFIED

Grok external file-level witness metadata:

KEY_ID = witness-prod-witness-002
SIGNED_AT_UTC = 2026-06-21T03:43:35Z
GROK_PUBLIC_KEY_SHA256 = 51466390000f62918ba3fc216335f114924361457f48804869a3d48f13020517
GROK_SIGNATURE_SHA256 = 6bb147c3fbdd55d48ce7ec670b63ef228e5dcbd695f4ed844b349e990f66670a
SIGNED_FILE_SHA256 = c0548dd4dff4ba657dd17c48c99ef211ca7bb8b21f84514f831216116b03964a
FILE_LEVEL_SIGNATURE = VERIFIED
TRUST_ROOT_REGISTERED = FALSE
PRODUCTION_QUORUM = FALSE

## Disclosed Non-Production Evidence

SELF_CONTROLLED_LAB_SIGNATURES = PASS_DISCLOSED

The self-controlled lab signatures prove local cryptographic mechanics only.
They do not count as independent production quorum.

DEEPSEEK_SIGNING_WITNESS = SIGNING_NOT_AVAILABLE

DeepSeek first returned a fake/demo signature, which was rejected.
DeepSeek then corrected the record and stated cryptographic signing was not available.
This is recorded as a rejection/non-capability receipt, not a signing witness.

## Witness Class Policy Dependency

WITNESS_CLASS_POLICY_V0_1 = SEALED

The sealed witness class policy separates:

- production witnesses
- external file-level witnesses
- external hash-only witnesses
- self-controlled lab signatures
- signing-not-available receipts

Under that policy, external file-level witness evidence is admissible and allows the Treasury project to continue as a candidate package.

It does not unlock real genesis unless production trust-root quorum is satisfied.

## IP Boundary

Local evidence remains local.

The following are not committed by this candidate receipt:

- local witness evidence directories
- local signing keys
- private signing material
- raw local secret files
- self-controlled lab key material

This public receipt records hashes, status, and evidence boundaries only.

## Candidate Acceptance

This candidate is accepted for production trust review because:

1. Treasury live-source fetch passed.
2. Strict public-fill verification passed.
3. Message-to-sign hash is sealed.
4. External Grok file-level witness verified.
5. DeepSeek fake signature was rejected.
6. DeepSeek signing limitation was disclosed.
7. Witness classes are now policy-separated.
8. Real genesis remains blocked.

## Final Candidate Ruling

TREASURY_GENESIS_CANDIDATE_V0_1 = SEALED_CANDIDATE_PENDING_PR
PUBLIC_LIVE_FETCH = PASS
STRICT_PUBLIC_FILL = PASS
GROK_EXTERNAL_FILE_WITNESS = VERIFIED
DEEPSEEK_SIGNING_WITNESS = SIGNING_NOT_AVAILABLE
SELF_CONTROLLED_LAB_SIGNATURES = PASS_DISCLOSED
WITNESS_CLASS_POLICY_V0_1 = SEALED
PRODUCTION_QUORUM = FALSE
REAL_GENESIS = BLOCKED
TREASURY_PROJECT_CAN_CONTINUE = TRUE
NO_FAKE_GREEN = ACTIVE
