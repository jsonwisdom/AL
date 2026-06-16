# GATE_SPEC_v1

## STATUS: GATE_SPEC_ADDED
## CHARACTER: Beige Brenda MN
## ROLE: Boundary Enforcer / Evidence Membrane Operator
## AUTHORITY: FALSE
## VERIFIED: FALSE
## PRODUCTION_GREEN: FALSE
## NO_FAKE_GREEN: TRUE

Brenda is not byte-by-byte verified until all seven gates pass.

If a valid signed veto exists with `veto: true`, the checker MUST exit RED. No GREEN possible.

## Seven Gates

1. DID present: `witnesses/brenda/brenda.did.json`
2. Manifest signature verifies over `emission-<id>.json`
3. External bundle exists and matches manifest hash
4. Unpacked external files match declared hashes
5. Reported binding verifies
6. Veto file and signature are checked
7. Expiry and resolver status are checked

## Expiry Rules

- `expires_at` must be ISO8601 UTC
- max duration is 168 hours from `created_at`
- max extensions is 2
- if expired, state is `RED_EXPIRED`

## Replay Command

./verify-brenda.sh <emission_id>

## Exit Codes

0 = all gates pass, Brenda enforcing
1 = ordinary gate fail, Brenda witness-only
2 = signed veto active, hard RED
3 = expired, hard RED

## Current State

YELLOW_BRENDA_WITNESS_ONLY

## Ruling

Brenda is not an enforcement gate until the verifier can fail promotion.
