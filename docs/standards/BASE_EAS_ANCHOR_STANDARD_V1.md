# Base EAS Anchor Standard V1

Status: ACTIVE
Applies to: ALMS / AL147-style receipts and settlement artifacts

## Purpose

Define the repository standard for anchoring settled artifacts without requiring ENS text-record writes or HSM signing.

This standard exists because repeated anchor workflows drifted into ENS TXT record writes, HSM/EIP-712 handoff, or external mirror dependencies before the causal artifact had a simple Base transaction witness.

## Canonical Rule

For ALMS settlement artifacts, the default sovereign anchor is a Base EAS attestation.

ENS TXT records are optional discovery pointers.
HSM signatures are optional higher-assurance signatures.
Arweave and Filecoin are optional/deferred mirror layers unless explicitly required by a versioned policy.

No workflow may require ENS TXT payment before attempting the Base EAS anchor path when an existing verified schema is available.

## Existing Base Mainnet Schema

Use the existing schema when the artifact can be represented by identity, root, CID, commit, and archive hash.

Chain: Base Mainnet
Chain ID: 8453
EAS Contract: `0x4200000000000000000000000000000000000021`
Schema Registry: `0x4200000000000000000000000000000000000020`
Schema UID: `0xfa94377476d86a25585e7da7889adf60f5a34fe09e1744f98626ad66bb686baa`
Schema string:

```text
string identity,bytes32 root,string cid,string commit,bytes32 archiveSha256
```

Repository source:

```text
contracts/eas/base.config.json
```

## Required Attestation Fields

For each anchored artifact, populate:

```text
identity       = human or ENS/Basename identity, e.g. jaywisdom.base.eth
root           = 0x-prefixed SHA-256 of the attested artifact bytes
cid            = content-addressed artifact CID or bundle CID
commit         = full 40-character Git commit containing the receipt/artifact
archiveSha256  = 0x-prefixed SHA-256 of the archive/artifact being attested
```

If no separate ZIP/archive exists locally, `archiveSha256` may equal `root`, but only when the attested artifact itself is the archive of record. The receipt must state this explicitly.

## Required Receipt Pattern

Before attestation, create:

```text
receipts/<protocol>/<version>/eas/<protocol>_eas_attestation_payload.pending.json
```

After attestation, create:

```text
receipts/<protocol>/<version>/eas/<protocol>_eas_attestation_result.final.json
```

The final receipt must include:

```json
{
  "base_tx_hash": "0x...",
  "eas_attestation_uid": "0x...",
  "schema_uid": "0x...",
  "status": "BASE_EAS_ATTESTED",
  "anchor_executed": true
}
```

## Verification Requirements

An anchor is not complete until all are true:

1. The final receipt is committed and pushed to GitHub.
2. The Base transaction hash exists.
3. The EAS attestation UID exists.
4. The schema UID in the receipt matches the on-chain event schema.
5. The attested fields match the pending payload.
6. The receipt states `BASE_EAS_ATTESTED` and `anchor_executed: true`.

## Forbidden Claims

Do not claim:

```text
ENS_POINTER_WRITTEN
HSM_SIGNED
ARWEAVE_PERSISTED
FILECOIN_PERSISTED
3_OF_3_PERSISTENCE_COMPLETE
```

unless the corresponding transaction, UID, CID, or receipt exists.

## AL147 v147.3 Reference Implementation

Final receipt:

```text
receipts/al147/v147_3/eas/al147_eas_attestation_result.final.json
```

Base transaction:

```text
0x19d7ac87ec3fd3d2def7d0e3478d12166de9bd603425726d54802a391750c70a
```

EAS attestation UID:

```text
0xd46120790f74e9f6937324cab3e713f13c4958148fa01c980e9c857904312479
```

Schema UID:

```text
0xfa94377476d86a25585e7da7889adf60f5a34fe09e1744f98626ad66bb686baa
```

Result:

```text
AL147 v147.3 = BASE_EAS_ATTESTED
ENS TXT = NOT REQUIRED
HSM = NOT REQUIRED
GHOST FINALITY = ELIMINATED
```
