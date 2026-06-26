# Replay Envelope Signatures v0.1

## Purpose

Signature verification upgrades replay envelopes from deterministic inputs to attested evidence.

A valid signature proves authorship over the canonical envelope hash. It does not prove truth.

## Signature Block

Every `replay-envelope-v0.1` envelope MUST include:

```json
{
  "signature": {
    "signature_version": "envelope-signature-v0.1",
    "key_id": "KEY_example",
    "algorithm": "ECDSA_P256_SHA256_DER_V1",
    "signed_payload": {
      "field": "integrity.envelope_canonical_hash",
      "hash": "sha256:..."
    },
    "signature_encoding": "base64_der",
    "signature_value": "..."
  }
}
```

## Signing Rule

The signer signs the canonical envelope hash declared at:

```text
integrity.envelope_canonical_hash
```

The signature block must repeat the same hash at:

```text
signature.signed_payload.hash
```

If the two hashes differ, replay must be refused.

## Algorithm v0.1

```text
ECDSA_P256_SHA256_DER_V1
```

Verification uses:

```text
OpenSSL ECDSA P-256 public key
SHA-256 digest
DER signature bytes
base64 encoded signature transport
```

## Key Registry

Public keys are resolved from:

```text
contracts/keys/v0.1/registry.json
```

A `key_id` is admissible only if:

1. It appears in the registry.
2. It is marked `active: true`.
3. Its algorithm matches the envelope signature algorithm.
4. Its public key material can verify the signature.

## Refusal Conditions

Replay MUST be refused if:

- signature block missing
- key_id missing from registry
- key inactive
- algorithm mismatch
- signed payload hash mismatch
- malformed base64 signature
- OpenSSL verification fails

## Non-Authority Clause

A valid signature proves only that the registered key signed the envelope hash.

It does not prove the claim is true.

It does not prove the signer had legal authority.

It does not prove the fixture was semantically correct.

It only establishes chain-of-custody for the replay input.
