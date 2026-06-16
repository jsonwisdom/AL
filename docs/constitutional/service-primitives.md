# Constitutional Service Primitives

## Purpose

This document defines the current working primitives in plain language.
It is not a manifesto. It describes what the repository can actually do today.

## Atomic Pattern

```text
operation -> receipt -> replay verification -> oath
```

This is the smallest useful constitutional service loop.

## Receipt

A receipt is a point-in-time claim about an operation.

It records:

- what operation was attempted
- what checks were performed
- what state was observed
- what result was produced
- whether the operation reported success or failure

A receipt does not prove eternal truth.
It proves what was observed at the time it was generated.

Old receipts may drift from current repository state. That is expected.
Historical verification exists to check internal consistency without requiring old state to equal current state.

## Replay Verification

Replay verification re-runs a verifier against a receipt.

It can return:

- `RECEIPT_CONFIRMED`
- `RECEIPT_REJECTED`

Current-tip verification checks whether the receipt still matches the current repository state.
Historical verification checks whether the receipt is internally consistent as a point-in-time artifact.

## Replay Oath

A replay oath is a witness statement about verification.

It records:

- which receipt was checked
- which verifier was used
- what the verifier observed
- what verdict was produced
- what hashes bind the receipt, verifier, and output

A receipt says: "this operation happened."
An oath says: "I replayed the receipt and observed this verdict."

## Index

The receipt index is a lightweight registry.

It maps:

```text
receipt_id -> path -> operation -> status -> head_commit
```

The index is not the source of truth by itself.
Receipt files remain the source artifacts.
The index exists so receipts can be discovered without scanning every file manually.

## Current Working Loop

The current root continuity loop is:

```bash
./scripts/root_continuity_checkpoint.sh
python3 scripts/verify_root_continuity_receipt.py <receipt.json>
python3 scripts/verify_root_continuity_receipt.py --historical <receipt.json>
python3 scripts/update_receipt_index.py <receipt.json>
```

The checkpoint script now updates the index automatically.

## What This Proves

The current loop proves:

- the drill script can execute
- the receipt JSON is valid JSON
- the receipt can be replay-checked
- the index can track generated receipts
- historical and current-tip checks are different operations

## What This Does Not Yet Prove

The current loop does not yet prove:

- cryptographic signature validity
- third-party witness execution
- CI witness execution
- full JCS canonicalization enforcement
- external settlement or anchoring
- universal correctness of the operation

## Boundary Rule

Do not claim more than the witnesses prove.

No witness, no claim.
No receipt, no ratification.
No replay, no settlement.

## Current Status

```text
drill              = implemented
receipt            = implemented
index              = implemented
verifier           = implemented
historical mode    = implemented
replay oath schema = implemented
signing            = pending
CI witness         = pending
external witness   = pending
```

## Operating Principle

No irreversible gods.
Only recoverable continuity.
