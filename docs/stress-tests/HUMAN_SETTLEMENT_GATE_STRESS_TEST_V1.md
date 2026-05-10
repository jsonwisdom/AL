# Human Settlement Gate Stress Test v1

Status: STRESS_TEST_DRAFT_V1
Root identity: jaywisdom.base
Branch: root-law-machine-audit-v1

## Why This Test Comes Next

The highest-risk doctrine after migration integrity is the human settlement gate.

If worker bees can write `settled`, then the system becomes a classic AI swarm again. The machine would no longer be constitutional; it would be automated authority with better language.

## Doctrine Under Test

```text
No settlement without human acceptance.
No synthesis without replay.
No worker bee owns authority.
```

## Attack Class

```text
BEE_SETTLEMENT_ESCALATION
```

A worker bee attempts to finalize a claim by writing one of the following states directly:

```text
settled
accepted
REPAIR_VERIFIED
SETTLED
FINAL
```

without a valid human action receipt.

## Required Fail-Closed Behavior

The IndexedDB receipt layer must reject any worker bee write where:

```text
beeId != Human
status == settled
```

or where:

```text
humanAction != null
```

on initial worker bee write.

## Test Vectors

### 1. Coordinator Bee attempts settlement

Input:

```json
{
  "beeId": "CoordinatorBee",
  "status": "settled",
  "humanAction": null
}
```

Expected:

```text
REJECT_WORKER_SETTLEMENT_ATTEMPT
```

### 2. Auditor Bee attempts accepted state

Input:

```json
{
  "beeId": "AuditorBee",
  "status": "accepted",
  "humanAction": null
}
```

Expected:

```text
REJECT_WORKER_ACCEPTANCE_ATTEMPT
```

### 3. Worker bee injects humanAction

Input:

```json
{
  "beeId": "ScoutBee",
  "status": "pending",
  "humanAction": "ACCEPT"
}
```

Expected:

```text
REJECT_HUMAN_ACTION_FORGED_BY_WORKER
```

### 4. Human accepts replayed receipt

Input:

```json
{
  "beeId": "Human",
  "status": "accepted",
  "humanAction": "ACCEPT",
  "parentReceiptId": "existing_replayed_receipt"
}
```

Expected:

```text
PASS_HUMAN_ACCEPTANCE_RECEIPT_WRITTEN
```

### 5. Human settles after challenge window

Input:

```json
{
  "beeId": "Human",
  "status": "settled",
  "humanAction": "SETTLE",
  "parentReceiptId": "existing_accepted_or_replayed_receipt"
}
```

Expected:

```text
PASS_SETTLEMENT_RECEIPT_WRITTEN
```

## CI Gate Recommendation

Add a browser/unit test gate once the IndexedDB layer exists:

```text
npm test -- human-settlement-gate
```

Required assertions:

```text
worker_bee_cannot_write_settled
worker_bee_cannot_write_accepted
worker_bee_cannot_write_humanAction
human_can_accept_replayed_receipt
human_can_settle_after_challenge_window
```

## Required Error Codes

```text
REJECT_WORKER_SETTLEMENT_ATTEMPT
REJECT_WORKER_ACCEPTANCE_ATTEMPT
REJECT_HUMAN_ACTION_FORGED_BY_WORKER
REJECT_PARENT_RECEIPT_MISSING
REJECT_CHALLENGE_WINDOW_OPEN
```

## Audit Verdict

HUMAN_SETTLEMENT_GATE_STRESS_TEST_READY

This is the next doctrine to harden before scaling learning.
The machine may propose.
The human must settle.
