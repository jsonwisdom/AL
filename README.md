# AL — Public Lab for Replayable AI Infrastructure

**AL is not a framework. It is a public lab.**

A living collection of primitives that make AI systems auditable, replayable, and settlement-ready once they touch reality.

This repo is structured as a game:

```text
clone it
play it
break it
extend it
```

## Start Here

👉 [`GAME.md`](./GAME.md) — machine-readable game loop and current levels.

## Current Level Status

```text
Level 1 — Continuity Drill      stable
Level 2 — Receipt Replay        stable
Level 3 — Replay Oath           schema live
Level 4 — Skill Boundary        implemented
Level 5 — x402 Settlement       design-ready, not active
```

## Quickstart

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
chmod +x scripts/root_continuity_checkpoint.sh
./scripts/root_continuity_checkpoint.sh
```

Then verify the receipt:

```bash
LATEST=$(ls -t receipts/root-continuity/*.json | head -1)
python3 scripts/verify_root_continuity_receipt.py "$LATEST"
python3 scripts/verify_root_continuity_receipt.py --historical "$LATEST"
cat receipts/index.json | python3 -m json.tool
```

## What You Should See

The drill should:

- check the repo continuity state
- emit a receipt JSON
- validate the receipt JSON
- update `receipts/index.json`

The verifier should emit either:

```text
RECEIPT_CONFIRMED
```

or:

```text
RECEIPT_REJECTED: <reason>
```

Honest failure is useful. Drift is a finding.

## What You Will Find Inside

```text
GAME.md                                game loop / levels
VERIFY.md                              public replay law
scripts/root_continuity_checkpoint.sh  Level 1 drill
scripts/verify_root_continuity_receipt.py Level 2 verifier
scripts/update_receipt_index.py        receipt registry updater
receipts/index.json                    lightweight receipt registry
docs/schemas/receipt-v0.2.json         receipt schema
docs/schemas/replay-oath-v0.1.json     replay oath schema
docs/constitutional/service-primitives.md plain-language primitives
.agents/skills/                        bounded repo-local agent skills
docs/forensic/                         forensic memory
Dockerfile.replay                      replay chamber
```

## Core Loop

```text
operation
→ receipt
→ index
→ replay verification
→ oath
→ optional settlement
```

## Current Doctrine

```text
No witness, no claim.
No receipt, no ratification.
No replay, no settlement.
```

Settlement is downstream from receipts.
Payment does not create legitimacy.

## How to Play

1. Run Level 1.
2. Verify the receipt with Level 2.
3. Report the first honest failure or success.
4. Extend a skill, receipt type, or verifier.
5. Keep claims bounded by what replay proves.

## What This Is Not

This is not a token launch.
This is not a finished protocol.
This is not a claim of universal truth.

It is an operational lab for making AI-adjacent systems more replayable, auditable, and honest about their own state.

## Operating Principle

```text
No irreversible gods.
Only recoverable continuity.
```

Clone → run → verify → extend.
