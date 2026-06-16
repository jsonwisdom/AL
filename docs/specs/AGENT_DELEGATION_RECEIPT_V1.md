# AGENT_DELEGATION_RECEIPT_V1 Specification

## Version
- receipt_type: AGENT_DELEGATION_RECEIPT_V1
- receipt_version: 1.0.0

## Key Addition
Per-receipt identity material in `proof`:
- `public_key` (preferred, 64-char hex)
- `did` (optional, strict did:key decoder in V1.1)

## Resolution Order
1. proof.public_key
2. proof.did
3. V0 fallback key

## Errors
- FAIL: public key missing
- FAIL: public key invalid
- FAIL: did resolution unsupported
- FAIL: signature mismatch

## Fixtures
Valid: receipt-public-key-valid.json (real vector)
Invalid: missing-key, invalid-public-key, unsupported-did, tampered-signature

## V1.1 did:key Ed25519 decoding

V1.1 introduces a strict, replay-verifiable decoder for `did:key` identifiers representing Ed25519 public keys.

### Accepted form

A valid Ed25519 DID key must have the form:

```text
did:key:z<base58btc>
```

Where:

- `<base58btc>` decodes to exactly 34 bytes
- the first two bytes are the Ed25519 multicodec prefix `0xed 0x01`
- the remaining 32 bytes are the raw Ed25519 public key

### Decoding pipeline

The decoder performs the following steps:

1. Require prefix `did:key:z`
2. Extract the base58btc payload
3. Decode using base58btc
4. Require decoded length = 34 bytes
5. Require multicodec prefix = `ed01`
6. Return the final 32 bytes as the Ed25519 public key

No fallback. No inference. No normalization. No alternative multicodecs. No alternative multibase prefixes.

### Rejected forms

The decoder rejects:

- wrong-prefix: any DID not starting with `did:key:z`
- wrong-multibase: any DID using a multibase prefix other than `z`
- wrong-keytype: any multicodec prefix other than `ed01`
- truncated: base58btc payload decoding to fewer than 34 bytes
- extra-bytes: base58btc payload decoding to more than 34 bytes
- empty: empty string or empty payload after `did:key:`
- missing-z: `did:key:` followed directly by base58btc without the `z` multibase prefix

### Canonical decoder errors

V1.1 decoder errors are deterministic and enforced by CI in Python and JavaScript:

- `invalid did:key prefix`
- `missing base58btc payload`
- `invalid base58btc payload`
- `invalid multicodec length`
- `invalid multicodec prefix`

### Language parity

V1.1 requires strict Python and JavaScript parity:

- same valid inputs produce the same 32-byte output
- same invalid inputs produce the same error string
- no language-specific normalization
- no language-specific fallback behavior

Parity is enforced by CI using the canonical fixture corpus.

### Fixture corpus

The V1.1 decoder is tested against:

- one canonical valid fixture generated from a deterministic raw Ed25519 key
- seven invalid fixtures, each isolating a single failure mode

These fixtures are part of the V1.1 replay surface and must not be altered without a new replay loop.

Builds on #294. Part of #295 and #298.

Do not inherit trust. Replay it.
