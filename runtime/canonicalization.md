# Canonicalization Rules

## Encoding

- UTF-8 only
- RFC 8785 JSON Canonicalization Scheme (JCS)
- No pretty printing
- Lexicographic key ordering
- Omit null fields entirely
- `additionalProperties=false` enforced by schema

## Hashing

```text
sha256:<hex digest>
```

Rules:

1. `event_payload_bytes = JCS(event_payload)`
2. `event_payload_hash = sha256(event_payload_bytes)`
3. `envelope_bytes = JCS(envelope)`
4. `uid_digest = sha256(envelope_bytes)`
5. `UID = "uid:" + base58btc(uid_digest)`

## Signing

- Ed25519 deterministic signatures per RFC 8032
- Remove `signatures` field before signing
- `sig_input = sha256(JCS(body_without_signatures))`

## Replay Invariants

A verifier MUST recompute:

- `uid`
- `event_payload_hash`
- signature verification result
- `state_hash`

Replay halts on the first divergent UID.

## Witness Log Layout

```text
.runtime/witnesses/
  by-kind/
  shards/
  witness-log.ndjson
```

Index replay order:

1. `timestamp_logical`
2. `uid`

## Emission FSM

1. Observe deterministic workflow completion
2. Build canonical payload
3. Increment `timestamp_logical`
4. Compute `state_hash`
5. Build UID envelope
6. Sign witness body
7. fsync witness → append indices → update state

No wall clock participates in UID generation.
