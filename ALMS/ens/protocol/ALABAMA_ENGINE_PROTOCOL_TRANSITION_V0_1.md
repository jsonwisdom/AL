# ALABAMA_ENGINE_PROTOCOL_TRANSITION_V0_1

STATUS: TRANSITION_LAW
TRUTH_STATE: YELLOW
AUTHORITY: FALSE
NO_FAKE_GREEN: TRUE

## PURPOSE

This file defines when Alabama ALMS Engine states may transition.

YELLOW is not authority.
YELLOW is not verification.
YELLOW is only a time-bounded repair state.

## STATE MODEL

UNKNOWN = no current classification
RED = missing required records without valid pending_update receipt
YELLOW = missing required records with valid unexpired pending_update receipt
GREEN = required records byte-match resolver artifact
RED_EXPIRED = pending_update expired before GREEN
SIGNATURE_INVALID = RED
WITNESS_REVOKED = RED
INFINITE_YELLOW_LOOP = RED

## CURRENT ENGINE RECORDS

Subject:

jaywisdom.base.eth

Required TXT records:

- alms.packet.cid
- alms.packet.sha256
- alms.matrix.hash

## TRANSITION RULES

UNKNOWN -> RED:
Required TXT records missing and no pending_update receipt exists.

RED -> YELLOW:
Allowed only if a new pending_update receipt exists, has no_fake_green true, and expires in the future.

YELLOW -> GREEN:
Allowed only if all required TXT records byte-match a resolver artifact.

YELLOW -> RED_EXPIRED:
Mandatory if expires_at_utc is in the past.

RED_EXPIRED -> YELLOW:
Blocked unless a new pending_update receipt contains a different commit SHA and a new reason.

YELLOW -> YELLOW:
Blocked if used only to reset the timer.

GREEN -> YELLOW:
Allowed only when a new divergence is detected and receipted.

GREEN -> RED:
Required if resolver artifact is contradicted, signature invalid, or witness revoked.

## MAX WINDOWS

Operational TXT missing: 24 hours target.
Legacy human repair: 72 hours maximum.
Signature mismatch: 4 hours maximum.
Key rotation: separate public rotation notice required.

## GREEN REQUIREMENTS

GREEN requires:

1. Resolver artifact snapshot
2. Required TXT records present
3. Byte-for-byte match
4. Checker output
5. Workflow run receipt
6. Commit SHA
7. NO_FAKE_GREEN true

## OUTSIDE AUDIT RULING

Outside reviewers classified the system as YELLOW:
honest structure, incomplete external verifiability.

## FINAL RULING

ENGINE_STATE: YELLOW
TEMPORARY_AUTHORITY: FORBIDDEN
INFINITE_YELLOW_RESET: FORBIDDEN
GREEN: BLOCKED
NO_FAKE_GREEN: ACTIVE
