# ALMS Pointer v1 Boundary Contract

## Scope

This contract defines the public external verifier boundary for the ALMS ENS pointer layer.

The pointer layer is reference-only. It does not include ALMS receipts, MSW witness records, private keys, generated runtime state, or internal execution context.

## Public Signature Invariant

Ed25519 signatures verify over the ASCII bytes of the payload SHA-256 hex string.

- Message: literal ASCII characters of `.payload_sha256`
- Signature field: `.signature.signature`
- Signer field: `.signature.signer`
- Payload hash rule: `jq -cS <payload> | sha256sum | awk '{print $1}'`

No binary hash message.  
No detached signature.  
No alternate field paths.  
No reinterpretation of ENS TXT fields.

## Canonical External Verifier Model

1. Resolve ENS TXT records.
2. Fetch IPFS packet ZIP from `alms.packet.cid`.
3. Verify packet ZIP SHA-256 against `alms.packet.sha256`.
4. Extract pointer artifacts from the packet.
5. Verify canonical payload hashes for status, badge, and metadata.
6. Verify embedded Ed25519 signatures over ASCII `.payload_sha256` strings.
7. Verify matrix hash agreement against `alms.matrix.hash`.

## Required ENS TXT Records

```text
alms.packet.cid
alms.packet.sha256
alms.matrix.hash
```

## Required Packet Pointer Artifacts

```text
ALMS-v20-behavioral-chain-packet/anchors/
  ens_pointer_status.json
  ens_pointer_status_envelope.json
  ens_pointer_badge.json
  ens_pointer_badge_envelope.json
  ens_pointer_metadata.jsonld
  ens_pointer_metadata_envelope.json
```

## External Replica Expected Files

```text
expected/
  ens_root.txt
  packet_sha256.txt
  status_envelope_hash.txt
  badge_envelope_hash.txt
  metadata_envelope_hash.txt
  matrix_hash.txt
  pubkey.pem
```

## Explicit Exclusions

The external verifier must not require:

- ALMS receipts
- MSW witness records
- private keys
- generated runtime files
- detached signatures
- renamed ENS fields
- binary hash message verification
- repo-local assumptions

## Success Condition

```text
REPLICA_OK root=<ens_root>
```

## Failure Semantics

Failures must be explicit and attributable, including:

```text
ENS_MISSING ...
PACKET_HASH_MISMATCH ...
STATUS_ENV_HASH_MISMATCH ...
BADGE_ENV_HASH_MISMATCH ...
METADATA_ENV_HASH_MISMATCH ...
ENV_PAYLOAD_HASH_MISMATCH ...
ENV_SIGNATURE_INVALID ...
MATRIX_HASH_MISMATCH ...
```

## Final Boundary

Pointer layer = reference-only surface.  
Proof surfaces = out-of-scope.  
Signature scope = metadata-only, hash-only, ASCII-only.
