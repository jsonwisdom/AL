# GATE_7_RESOLVER_SPEC_V0_1

## STATUS: FAIL_CLOSED_SPEC_ADDED
## CHARACTER: Beige Brenda MN
## GATE: 7
## AUTHORITY: FALSE
## VERIFIED: FALSE
## PRODUCTION_GREEN: FALSE
## NO_FAKE_GREEN: TRUE

Gate 7 is the resolver status gate.

Brenda cannot fully enforce unless resolver status is observed and preserved.

## Required Witness

File:

`witnesses/brenda/resolver_status.json`

Required fields:

- `name`: `jaywisdom.eth` or `jaywisdom.base.eth`
- `txt_key`: `brenda.status`
- `txt_value`: `ACTIVE`
- `source`: resolver / mirror / manual witness
- `observed_at_utc`
- `authority: false`
- `verified: false`
- `no_fake_green: true`

## Rule

If resolver status witness is missing, malformed, expired, or not ACTIVE, verifier MUST fail closed.

## Boundary

A repo mirror is not the same thing as live L1 authority.

Production GREEN requires live resolver observation or separately accepted public anchor.
