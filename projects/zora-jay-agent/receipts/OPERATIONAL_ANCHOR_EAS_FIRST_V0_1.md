# OPERATIONAL_ANCHOR_EAS_FIRST_V0_1

## STATUS: DECISION_RECEIPT_DRAFT
## TRUTH_STATE: YELLOW
## NO_FAKE_GREEN: ACTIVE
## EXECUTED_ONCHAIN: FALSE

```json
{
  "receipt": "OPERATIONAL_ANCHOR_EAS_FIRST_V0_1",
  "repo": "jsonwisdom/AL",
  "lane": "projects/zora-jay-agent",
  "decision": "ANCHOR_FIRST_SCRIPT_LATER",
  "path_chosen": "EAS_TYPED_WITNESS_FIRST",
  "fallback_path": "L1_ENS_TEXT_RECORD",
  "seal_identity": "jaywisdom.eth",
  "engine_identity": "jaywisdom.base.eth",
  "identity_sync_file": "identity_sync_v0.1.json",
  "challenge_period_seconds": 604800,
  "finalized": false,
  "no_fake_green": true
}
```

## Dual-Core Split

- `jaywisdom.eth` is the Seal: L1, immutable, non-repudiation, long-term anchor.
- `jaywisdom.base.eth` is the Engine: L2, mutable, high-velocity custody, state logs.
- `identity_sync_v0.1.json` remains the bridge object between Seal and Engine.
- `challenge_period: 604800` is accepted as the seven-day optional dispute gate.

## Chosen Anchor Path

The first operational anchor should be EAS-first, not ENS-text-first.

Reason: typed witnesses are cleaner than plain text hashes. EAS gives schema-bound fields, revocation, off-chain pointers, state-machine compatibility, and better `NO_FAKE_GREEN` separation between `ATTESTED`, `CHALLENGED`, and `FINALIZED`.

## Proposed Schema

```graphql
string anchor_type, bytes32 aggregate_hash, uint256 block_height_l2, uint256 timestamp, string commit_sha, uint256 challenge_period, bool finalized
```

Schema name:

```text
JAYWISDOM Operational Anchor v0.1
```

## Corrected Execution Notes

- Schema registration belongs on the SchemaRegistry contract for the target chain.
- Attestation belongs on the EAS contract for the target chain.
- If the anchor is on Base, use the Base RPC for Base contract calls.
- `jaywisdom.eth` is an ENS name, not an EAS recipient address by itself. The attestation must use an address field, while ENS identity linkage should be represented by resolver proof, signed message, or referenced identity sync JSON.
- No transaction hash is claimed in this receipt.
- No schema UID is claimed in this receipt.
- No finality is claimed in this receipt.

## YELLOW Receipt Template After Execution

```json
{
  "state": "YELLOW",
  "reason": "ANCHOR_PENDING_CHALLENGE",
  "chain": "Base",
  "schema_uid": "0x...",
  "attestation_uid": "0x...",
  "aggregate_hash": "0x...",
  "commit_sha": "<git_commit>",
  "challenge_period": 604800,
  "challenge_ends": "<unix_timestamp>",
  "finalized": false,
  "NO_FAKE_GREEN": "ACTIVE"
}
```

## Ruling

```text
ANCHOR FIRST: TRUE
SCRIPT LATER: TRUE
EAS FIRST: TRUE
L1 TEXT FALLBACK: TRUE
CURRENT STATE: YELLOW_DECISION_ONLY
NO_FAKE_GREEN: ACTIVE
```
