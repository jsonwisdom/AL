# Witness Signer Interface v0.1

The capture tool must not handle secret signing material directly.

## Command

witness_signer sign \
  --key-id <prod-witness-id> \
  --message-hash sha256:<receipt_hash> \
  --purpose live_capture_attestation

## Response

key_id: prod-witness-001
algorithm: ed25519
message_hash: sha256:<receipt_hash>
signature: base64:<signature>
signed_at_utc: <iso8601>
signer_backend: offline | age_encrypted | hsm | kms

## Boundary

Signer must reject revoked, simulated, staging, unknown, inactive, or unauthorized keys.
