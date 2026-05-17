# AL Player Pack

This is the single-file fallback entrance for constrained agents, sandboxes, and humans that cannot rely on search, git clone, DNS, or raw fetch access.

## Repo

```text
https://github.com/jsonwisdom/AL
```

## Purpose

Play AL: THE REPLAY COURT.

The goal is not to admire the architecture.
The goal is to make drift observable.

## Core Rule

```text
No witness, no claim.
No receipt, no ratification.
No replay, no settlement.
```

## Primary Witness Files

If full repository access is available, read these first:

```text
README.md
GAME.md
VERIFY.md
docs/constitutional/service-primitives.md
```

Fallback browser URLs:

```text
https://github.com/jsonwisdom/AL/blob/master/README.md
https://github.com/jsonwisdom/AL/blob/master/GAME.md
https://github.com/jsonwisdom/AL/blob/master/VERIFY.md
https://github.com/jsonwisdom/AL/blob/master/docs/constitutional/service-primitives.md
```

Raw URLs, if raw fetch is available:

```text
https://raw.githubusercontent.com/jsonwisdom/AL/master/README.md
https://raw.githubusercontent.com/jsonwisdom/AL/master/GAME.md
https://raw.githubusercontent.com/jsonwisdom/AL/master/VERIFY.md
https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/constitutional/service-primitives.md
```

## Level 1 — Continuity Drill

### Goal

Generate a continuity receipt and update the receipt index.

### Primary Command

```bash
chmod +x scripts/root_continuity_checkpoint.sh
./scripts/root_continuity_checkpoint.sh
```

### Expected Result

A receipt JSON should be created and the receipt index should update.

Look for:

```text
[ROOT CONTINUITY CHECKPOINT]
[7] validating receipt JSON
[8] updating receipt index
[ROOT CONTINUITY CHECKPOINT COMPLETE]
```

### Honest Failure Examples

```text
script missing
receipt invalid JSON
index not updated
remote unreachable
mirror missing
restore doc missing
head mismatch
```

These are findings, not disasters.

## Level 2 — Receipt Replay

### Goal

Verify the generated receipt in current-tip and historical mode.

### Commands

```bash
LATEST=$(ls -t receipts/root-continuity/*.json | head -1)
echo "$LATEST"
python3 scripts/verify_root_continuity_receipt.py "$LATEST"
python3 scripts/verify_root_continuity_receipt.py --historical "$LATEST"
cat receipts/index.json | python3 -m json.tool
```

### Expected Result

Look for:

```text
RECEIPT_CONFIRMED
mode: current-tip
RECEIPT_CONFIRMED
mode: historical
```

## If You Cannot Execute

If the environment cannot clone, fetch raw files, or execute shell commands, report that as access drift.

Use this status:

```text
VERIFIER STATUS: UNOBSERVED
DRIFT CLASS: access drift
```

## Report Format

Return results exactly in this format:

```text
LEVEL RESULT:
PASS / FAIL

DRIFT FOUND:
<exact issue>

REPRODUCTION:
<commands, environment, or access conditions>

PATCH PROPOSAL:
<smallest bounded fix>

VERIFIER STATUS:
CONFIRMED / REJECTED / UNOBSERVED

ENVIRONMENT:
OS:
Python:
Shell:
Container or bare metal:
```

## Player Objective

Clone it.
Play it.
Break it.
Report the first honest failure.

The game is to make drift observable before drift becomes authority.
