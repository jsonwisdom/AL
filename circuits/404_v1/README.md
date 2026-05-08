# 404_v1 Circuit Specification

Status: SPEC_ONLY_NOT_IMPLEMENTED

## Purpose

`404_v1` defines the minimal procedural integrity circuit for AGW / ALMS 404 Governance.

It proves that a URL fetch produced a bounded procedural outcome without making claims about motive, guilt, institutional intent, corruption, legitimacy, or blame.

This circuit is a pure procedural classifier.

## AllowedSurface v1

The public surface deliberately excludes `PAYWALL` and `AUTH_WALL` because those require contextual interpretation and may drift into institutional critique.

```text
FOUND
NOT_FOUND
VERSION_DRIFT
TOMBSTONED
MANIFEST_MISMATCH
REPLAY_FAIL
CRAWLER_BLOCKED
```

## Verdict Semantics

- `FOUND`: response is accessible and hash verifies when expected hash exists.
- `NOT_FOUND`: HTTP 404 observed.
- `VERSION_DRIFT`: HTTP 200 observed but body hash differs from declared manifest hash.
- `TOMBSTONED`: HTTP 410 observed.
- `MANIFEST_MISMATCH`: declared manifest and observed target metadata cannot be reconciled.
- `REPLAY_FAIL`: canonicalization or replay chain failed.
- `CRAWLER_BLOCKED`: automated verification could not proceed, including robots policy, 403, unexpected status, or crawler access failure.

`CRAWLER_BLOCKED` is a statement about the crawler verification attempt, not about institutional intent.

## Private Inputs

```text
url: felt252
http_status: u16
body_hash: felt252
manifest_hash: Option<felt252>
timestamp: u64
```

## Public Inputs

```text
track_id: felt252
allowed_surface_commitment: felt252
```

## Public Outputs

```text
verdict: felt252
receipt_commitment: felt252
```

## Constraints

```text
assert verdict in ALLOWED_SURFACE_SET

if http_status == 404:
    assert verdict == NOT_FOUND
elif http_status == 200 and manifest_hash.is_some() and body_hash != manifest_hash.unwrap():
    assert verdict == VERSION_DRIFT
elif http_status == 200:
    assert verdict == FOUND
elif http_status == 403:
    assert verdict == CRAWLER_BLOCKED
elif http_status == 410:
    assert verdict == TOMBSTONED
else:
    assert verdict == CRAWLER_BLOCKED

assert receipt_commitment == hash(url, http_status, body_hash, verdict, timestamp)
```

## Explicitly Absent Fields

The circuit must not expose or imply:

- responsible_party
- severity
- institutional_score
- trust_score
- guilt_score
- corruption_score
- intent
- motive
- blame
- liable
- human-readable interpretation

## Membrane Rule

The circuit may classify procedural fetch outcomes.

The circuit may not explain why the outcome occurred.

## Non-Claims

`404_v1` does not assert:

- hiding
- corruption
- misconduct
- guilt
- motive
- institutional legitimacy
- legal liability
- public-record completeness

## State

```json
{
  "circuit_id": "404_v1",
  "status": "SPEC_ONLY_NOT_IMPLEMENTED",
  "allowed_surface": "LOCKED_V1",
  "stark_layer": "NOT_IMPLEMENTED",
  "no_ghost_anchor": true
}
```
