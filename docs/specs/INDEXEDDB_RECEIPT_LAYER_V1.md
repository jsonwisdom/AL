# IndexedDB Receipt Layer v1

Status: SPEC_DRAFT_V1
Root identity: jaywisdom.base
Applies to: Witness Stream UI, Agent Oracle V2, worker bee outputs, replay verifier, human challenge gate, export bundles.

## Core Insight

Vertical authority constraint is what makes horizontal scaling safe.

Bees may multiply horizontally because none of them can settle truth. They can only emit receipts, request replay, and propose synthesis.

## Build Position

This is the first implementation dependency after WIRING.md.

```text
Learning Lab / Witness Stream UI
-> IndexedDB Receipt Log
-> Agent Oracle V2
-> Human Accept / Challenge
-> MigrationGuard
-> EAS Anchor
```

## Receipt Schema

Every write to the local receipt store must satisfy this schema.

```json
{
  "receiptId": "sha256|keccak deterministic hash",
  "rootIdentity": "jaywisdom.base",
  "constitutionalRootUid": "bytes32_or_pending",
  "sessionId": "string",
  "beeId": "CoordinatorBee|ScoutBee|PatternBee|BuilderBee|AuditorBee|Human",
  "taskInput": {
    "raw": "string_or_object",
    "hash": "bytes32"
  },
  "output": {
    "raw": "string_or_object",
    "hash": "bytes32"
  },
  "timestamp": 0,
  "parentReceiptId": "bytes32_or_zero",
  "status": "pending|accepted|challenged|replayed|settled|rejected",
  "humanAction": null,
  "modelLineage": {
    "provider": "string_or_local",
    "model": "string_or_human",
    "modelVersion": "string_or_unknown",
    "temperature": "number_or_null"
  },
  "confidenceBounds": {
    "state": "SPECULATIVE|EXTERNAL_PENDING|REPLAYED|CHALLENGED|SETTLED",
    "restraintFlags": []
  },
  "challengeWindowEndsAt": 0,
  "previousReceiptHash": "bytes32_or_zero",
  "receiptHash": "bytes32"
}
```

## Required Fields

Minimum required fields:

```text
receiptId
beeId
taskInput
output
timestamp
parentReceiptId
status
humanAction
receiptHash
```

## Deterministic receiptId

The receiptId must be deterministic from the receipt content.

Recommended preimage:

```text
rootIdentity
sessionId
beeId
taskInput.hash
output.hash
timestamp
parentReceiptId
previousReceiptHash
```

`receiptHash` must be computed over the canonical receipt with `receiptHash` set to null.

## Status Rules

```text
pending      = written but not human accepted or replayed
accepted     = human accepted proposal or output
challenged   = human or Auditor Bee challenged output
replayed     = output replay was attempted and receipt hash verified
settled      = challenge window closed with accepted/replayed state
rejected     = output rejected or repair failed
```

## Human Action Rules

`humanAction` starts as null.

Allowed values after human intervention:

```text
ACCEPT
CHALLENGE
REQUEST_REPLAY
REJECT
SETTLE
```

No worker bee may write final settlement without human action.

## Write Boundary Invariants

The IndexedDB layer must reject writes when:

- `beeId` is missing
- `taskInput.hash` is missing
- `output.hash` is missing
- `timestamp` is missing
- `status` is not allowed
- `humanAction` is not null on initial worker bee write
- `receiptHash` does not recompute
- `parentReceiptId` points to a missing receipt, unless it is zero
- a worker bee attempts to write `settled`
- a worker bee attempts to overwrite an existing receipt

## Append-Only Rule

Receipts are append-only.

Corrections must create a new receipt that points back to the prior receipt.

```text
No mutation of history.
Correction is a new linked receipt.
```

## Stores

IndexedDB database name:

```text
jays-wisdom-receipts-v1
```

Object stores:

```text
sessions
receipts
messages
challenges
replays
exports
```

Primary key for receipts:

```text
receiptId
```

Indexes:

```text
sessionId
beeId
status
timestamp
parentReceiptId
receiptHash
```

## Export Bundle

The local receipt layer must export bundles for later anchoring.

```json
{
  "type": "AgentOracleV2ReceiptBundle",
  "rootIdentity": "jaywisdom.base",
  "constitutionalRootUid": "bytes32_or_pending",
  "sessionId": "string",
  "receiptCount": 0,
  "bundleHash": "bytes32",
  "receipts": []
}
```

## Constitutional Invariants

```text
No output without a receipt.
No synthesis without replay.
No settlement without human acceptance.
No worker bee owns authority.
No receipt may be silently mutated.
```

## Audit Verdict

INDEXEDDB_RECEIPT_LAYER_SPEC_READY

The receipt schema is now the spine for the Witness Stream, Replay Verifier, Agent Oracle V2 runtime, MigrationGuard export, and future EAS anchoring.
