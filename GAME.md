# AL Game Map

AL is a public lab for replayable AI infrastructure.

This file makes the repo playable by humans and machines.
Each level has a goal, command, win condition, and failure condition.

## Core Rule

```text
No witness, no claim.
No receipt, no ratification.
No replay, no settlement.
```

## Level 1 — Continuity Drill

### Goal
Generate a root continuity receipt and update the receipt index.

### Command

```bash
chmod +x scripts/root_continuity_checkpoint.sh
./scripts/root_continuity_checkpoint.sh
```

### Win Condition

- receipt JSON is created under `receipts/root-continuity/`
- `receipts/index.json` is updated
- JSON parses cleanly

### Failure Condition

- script fails
- receipt is invalid JSON
- index does not update

## Level 2 — Receipt Replay

### Goal
Verify a generated receipt.

### Command

```bash
python3 scripts/verify_root_continuity_receipt.py <receipt.json>
python3 scripts/verify_root_continuity_receipt.py --historical <receipt.json>
```

### Win Condition

- verifier emits `RECEIPT_CONFIRMED`

### Failure Condition

- verifier emits `RECEIPT_REJECTED`
- current-tip and historical mode are confused

## Level 3 — Replay Oath

### Goal
Create a witness statement about receipt replay.

### Artifacts

- `docs/schemas/replay-oath-v0.1.json`

### Win Condition

- oath identifies receipt
- oath identifies witness
- oath records verification mode
- oath records receipt/output hashes

### Failure Condition

- oath claims more than the verifier observed
- oath lacks receipt reference

## Level 4 — Skill Boundary

### Goal
Use repo-local skills without granting imaginary authority.

### Artifacts

- `.agents/skills/witness-replay/SKILL.md`
- `.agents/skills/receipt-audit/SKILL.md`
- `.agents/skills/canonicalization-check/SKILL.md`
- `.agents/skills/anchor-readiness/SKILL.md`

### Win Condition

- skill names allowed inputs
- skill names allowed outputs
- skill names failure condition
- skill produces or references receipts

### Failure Condition

- skill makes claims without replay evidence
- skill invents authority

## Level 5 — Settlement Readiness

### Goal
Decide whether an operation is ready for optional x402 settlement.

### Rule

Settlement points to receipts.
Receipts do not depend on settlement.

### Win Condition

- receipt exists
- replay is confirmed
- oath exists or is explicitly pending
- settlement is optional and downstream

### Failure Condition

- payment is treated as legitimacy
- failed settlement invalidates replay truth

## Current Status

```text
Level 1: implemented
Level 2: implemented
Level 3: schema implemented
Level 4: skills implemented
Level 5: design-ready, not active
```

## Player Objective

Clone the repo.
Run Level 1.
Verify Level 2.
Report the first honest failure.

The game is not to win by narrative.
The game is to make drift observable.
