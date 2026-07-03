# AMS v1.0 — Authority Membrane Specification

Status: ARCHITECTURE_LOCK
Authority: false
Authority eligible: true

## Purpose

AMS v1.0 defines the only permitted path from authority eligibility toward a future authority transition.

Passing witness, replay, policy, or surface checks does not flip authority.

## Endpoint Separation

### Safe Without Authority

These endpoints may remain callable while authority is false because they collect evidence or expose read-only status:

- `/health`
- `/identity`
- `/hash`
- `/replay_url`
- `/emit`
- `/verify`
- `/governance/status`

### Requires Authority In Future Patch

These actions require a future valid governance proof before mutation:

- Supabase writes
- External attestations
- Governance mutations
- Authority state transitions

## Governance Stub Rules

`/governance/authorize` and `/governance/revoke` are validate-only stubs in this patch.

They must:

- return HTTP 200 for testability
- include `stub: true`
- include `mutated: false`
- preserve `authority: false`
- never write authority state

## Deferred Implementation

Future AMS patches must add:

- EIP-712 typed-data verification
- monotonic nonce validation
- governance signer or quorum validation
- artifact binding to EV-017
- replayable governance receipt output

## Invariants

- authority defaults to false
- implicit authority transition is prohibited
- no code path may silently promote authority
- governance proof is required before mutation
- evidence collection must not depend on authority
