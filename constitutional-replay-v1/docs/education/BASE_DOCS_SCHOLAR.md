# Base Docs Scholar — constitutional-replay-v1

Curated study map for understanding how Base can support AL receipts without becoming replay authority.

This is an education document, not executable verifier code.

## Core Boundary

```text
Local replay proves meaning.
Base witnesses commitment.
```

Base helps builders publish, discover, and challenge commitments.

Base does not mutate policy, interpreter, or replay semantics.

## Required Upstream Protocol

Before any Base witness integration, builders must satisfy:

```text
constitutional-replay-v1/docs/LOCAL_REPLAY_PROTOCOL.md
```

Kernel rule:

```text
If it cannot replay locally, it does not count.
```

## What To Study First

### 1. Transactions

Study how Base transactions are identified, included, and referenced.

AL mapping:

- transaction hash → `execution_ref`
- block number → optional witness metadata
- event log → optional discovery surface

### 2. Smart Wallets

Study wallet-controlled execution and account abstraction patterns.

AL mapping:

- wallet action → `emitReceipt()`
- refused wallet action → `emitRefusal()`
- wallet signature → receipt binding evidence
- delegated capability → `delegateCapability()`

### 3. Paymasters

Study gas sponsorship and gas abstraction.

AL mapping:

- paymaster pays gas
- paymaster does not authorize semantic meaning
- policy hash remains the authority boundary

### 4. Events

Study event logs as public discovery signals.

AL mapping:

- event can reveal a receipt summary hash
- event can reveal a Merkle root
- event cannot replace full local replay

### 5. Attestations / EAS

Study attestations as optional public witness records.

AL mapping:

- attestation UID → optional witness reference
- attester → optional accountability surface
- payload hash → must match local receipt commitment
- attestation does not decide meaning

### 6. x402

Study payment-trigger flow and signed authorization.

AL mapping:

- request quote → `input_hash`
- signed authorization → `economic_authority_hash`
- settlement transaction → `execution_ref`
- AL receipt → semantic replay object

## v0.1 Rule

Do not integrate Base in v0.1.

v0.1 proves:

- local canonicalization
- local SHA-256 receipt binding
- local policy interpretation
- local refusal replay
- local batch construction
- static dashboard viewing

## v0.2 Rule

Add only read-only witness verification:

```text
BASE_RPC_URL=... npm run verify:base
```

Allowed v0.2 checks:

- transaction exists
- Merkle root exists
- event log exists
- attestation UID exists
- payload hash matches local commitment

Forbidden v0.2 claims:

- Base proves policy meaning
- Base ratifies semantic truth
- Base overrides local replay
- Base fixes missing receipts

## Scholar Exercise

Given a Base transaction hash and a local receipt:

1. Verify the local receipt first.
2. Compute the receipt hash.
3. Check whether the hash appears in the local batch.
4. Check whether the batch root was witnessed on Base.
5. Confirm the Base marker points to the same root.
6. Report witness status separately from replay status.

Expected output shape:

```json
{
  "replay_status": "REFUSAL_CONFIRMED",
  "witness_status": "BASE_TX_CONFIRMED",
  "semantic_authority": "LOCAL_REPLAY"
}
```

## Privacy Discipline

Do not put sensitive action context into public metadata.

Use:

- fixed refusal enums
- context hashes
- local full receipts
- selective disclosure during replay or challenge

Avoid:

- free-text refusal reasons
- raw resource URLs
- private customer data
- unnecessary descriptions
- secrets in calldata or event logs

## JayWisdom.eth Builder Rule

Build in this order:

1. Local replay.
2. Golden vectors.
3. Refusal integrity.
4. Batch root.
5. Static dashboard.
6. Read-only Base witness.
7. x402 trigger.
8. Smart Wallet automation.
9. Optional EAS witness.

## Final Line

Base is powerful because it can witness commitments cheaply and publicly.

AL remains powerful because replay meaning survives without Base.
