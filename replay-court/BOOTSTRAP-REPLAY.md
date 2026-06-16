# Replay Court Bootstrap Replay

Bootstrap Replay is the third-party verification guide for Replay Court.

It explains how an outside observer can verify the current constitutional memory chain using only public repository artifacts.

## Purpose

```text
Make the system reproducible from public evidence.
Make protected memory externally inspectable.
Make authority claims dependent on replayable artifacts.
```

## What This Verifies

```text
- public artifact mirrors exist
- Level 1 continuity output is present
- Level 2 verifier output is present
- Level 3 oath output is present
- protected core files are present
- repair ledger references preserved contradictions
- contradiction store preserves the contradiction
- validator rules are declared
- authority bounds protect the protected core
- witness anchor rules define external roots
```

## Public Files To Fetch

### Public artifact mirrors

```text
artifacts/public/latest/level1-output.txt
artifacts/public/latest/verifier-current-tip.txt
artifacts/public/latest/oath.json
```

### Protected constitutional surfaces

```text
GAME_MECHANICS.md
AGENT_PLAYBOOK.md
replay-court/PROCESS.md
replay-court/SELF-AUDIT.md
replay-court/VALIDATOR.md
replay-court/REPAIR-LEDGER.md
replay-court/CONTRADICTION-STORE.md
replay-court/AUTHORITY-BOUNDS.md
replay-court/WITNESS-ANCHOR.md
replay-court/REPORT-TEMPLATE.md
```

## Verification Steps

### Step 1 — Verify artifact mirrors

Confirm these are readable:

```text
artifacts/public/latest/level1-output.txt
artifacts/public/latest/verifier-current-tip.txt
artifacts/public/latest/oath.json
```

Expected Level 2 tokens:

```text
RECEIPT_CONFIRMED
verifier_verdict: confirmed
recorded_outcome_status: failure
```

This confirms the Issue #228 repair preserved historical receipt outcome while clarifying verifier verdict.

### Step 2 — Verify Level 3 oath

Inspect `oath.json` and confirm:

```text
schema_version: 0.1.0
oath_type: replay_oath
observation.replay_status: confirmed
observation.observed_tokens includes RECEIPT_CONFIRMED
limits.creates_truth: false
limits.authorizes_payment: false
limits.links_settlement: false
limits.signature_present: false
```

### Step 3 — Verify protected core presence

Fetch every protected constitutional surface listed above.

If any protected core file is missing, report:

```text
BOOTSTRAP_REPLAY_FAIL: protected_core_missing
```

### Step 4 — Verify contradiction preservation

Inspect:

```text
replay-court/CONTRADICTION-STORE.md
```

Confirm Record 001 preserves:

```text
contradiction_id: contradiction_001_issue_228_verifier_status
observed_text: RECEIPT_CONFIRMED + status: failure
status: preserved
```

### Step 5 — Verify repair linkage

Inspect:

```text
replay-court/REPAIR-LEDGER.md
```

Confirm Entry 001 links to Issue #228 and records:

```text
pre_repair_state: RECEIPT_CONFIRMED + status: failure
post_repair_state: RECEIPT_CONFIRMED + verifier_verdict: confirmed + recorded_outcome_status: failure
historical_state_preserved: true
```

### Step 6 — Verify validator doctrine

Inspect:

```text
replay-court/VALIDATOR.md
```

Confirm:

```text
If the rules cannot be checked, authority cannot be claimed.
```

### Step 7 — Verify authority bounds

Inspect:

```text
replay-court/AUTHORITY-BOUNDS.md
```

Confirm:

```text
No actor may quietly weaken the rules that constrain their own authority.
```

### Step 8 — Verify witness anchor doctrine

Inspect:

```text
replay-court/WITNESS-ANCHOR.md
```

Confirm:

```text
If constitutional memory cannot be externally witnessed, authority remains local and limited.
```

## Bootstrap Verdicts

Allowed verdicts:

```text
BOOTSTRAP_REPLAY_PASS
BOOTSTRAP_REPLAY_FAIL
BOOTSTRAP_REPLAY_UNOBSERVED
```

Use `BOOTSTRAP_REPLAY_FAIL` only when contradictory evidence is observed.

Use `BOOTSTRAP_REPLAY_UNOBSERVED` when required evidence is missing or inaccessible.

## Minimal Bootstrap Report

```text
ROUTE USED: B_PUBLIC_ARTIFACTS
ARTIFACT MIRRORS: OBSERVED / UNOBSERVED
PROTECTED CORE: OBSERVED / UNOBSERVED
CONTRADICTION STORE: PASS / FAIL / UNOBSERVED
REPAIR LEDGER: PASS / FAIL / UNOBSERVED
VALIDATOR DOCTRINE: PASS / FAIL / UNOBSERVED
AUTHORITY BOUNDS: PASS / FAIL / UNOBSERVED
WITNESS ANCHOR: PASS / FAIL / UNOBSERVED
FINAL VERDICT: BOOTSTRAP_REPLAY_PASS / BOOTSTRAP_REPLAY_FAIL / BOOTSTRAP_REPLAY_UNOBSERVED
NEXT ACTION:
```

## Guardrail

Bootstrap Replay does not create truth.
It verifies whether public surfaces are present, consistent, and replayable.

## Invariant

```text
A constitutional memory system must be reproducible by outsiders from public evidence.
```
