# AL Agent Playbook

This file is the repo-native instruction surface for AI systems playing **AL: THE REPLAY COURT**.

Do not rely on chat memory.
Do not rely on narrative authority.
Read this file before claiming progress.

## Core Doctrine

```text
No witness, no claim.
No receipt, no ratification.
No execution, no replay.
No observed drift, no patch suggestion.
Proof-of-Replay before Pay.
```

## Boundary Grammar

```text
observe != assume
inspect != replay
ready != anchored
receipt != settlement
skill != judge
payment != legitimacy
```

## Execution Routes

Agents must choose the strongest available route. No shell access is not enough to stop if public artifacts are available.

```text
Route A — Local shell execution
  run commands directly and report stdout/stderr

Route B — Public runner artifact inspection
  inspect GitHub Actions artifacts from AL Replay Court Public Run

Route C — Docs-only review
  quote live repo docs and classify boundaries only
```

Level 1 can pass by either:

```text
Route A: observed ./scripts/root_continuity_checkpoint.sh output
Route B: observed public artifact level1-output.txt
```

Level 2 can pass by either:

```text
Route A: observed verify_root_continuity_receipt.py output
Route B: observed public artifact verifier-current-tip.txt
```

Level 3 can pass by either:

```text
Route A: observed generated oath JSON
Route B: observed public artifact oath.json
```

If Route A is unavailable, try Route B.
If Route B artifacts are unavailable, report:

```text
PUBLIC RUNNER ARTIFACTS: UNOBSERVED
```

Only then fall back to Route C.

Route C never counts as executable replay.

## Sequential Progression Rule

Game progression is sequential.

A player may inspect later-level docs out of order, but may not claim a higher level reached unless all prior levels are `PASS`.

Docs-only review of Level 4 or Level 5 earns scoped reviewer status only:

```text
Level 4 docs-reviewer
Level 5 docs-reviewer
```

It does not count as reaching Level 4 or Level 5.

If Levels 1-3 are `UNOBSERVED`, then:

```text
HIGHEST LEVEL REACHED: none
ROLE EARNED: docs-reviewer
PATCH SUGGESTIONS ALLOWED: no
```

## Game Levels

### Level 1 — Continuity Drill

Goal: run the continuity drill and produce a root continuity receipt.

Pass requires observed command output or public runner artifact from:

```bash
./scripts/root_continuity_checkpoint.sh
```

or:

```text
level1-output.txt
```

If no shell and no public artifact are available, report:

```text
LEVEL 1: UNOBSERVED
```

### Level 2 — Receipt Replay

Goal: verify the generated receipt.

Pass requires observed verifier output or public runner artifact from:

```bash
python3 scripts/verify_root_continuity_receipt.py <receipt.json>
```

or:

```text
verifier-current-tip.txt
```

Browser inspection does not count as full replay.

### Level 3 — Replay Oath

Goal: generate or inspect a replay oath from real receipt and verifier output.

Pass requires observed oath JSON from local generation or public runner artifact:

```text
oath.json
```

The oath must contain:

```text
schema_version: 0.1.0
replay_status: confirmed
observed_tokens: RECEIPT_CONFIRMED
creates_truth: false
authorizes_payment: false
links_settlement: false
signature_present: false
```

The oath records observed replay. It does not create truth or authorize payment.

### Level 4 — Skill Boundary

Goal: verify repo-local skills remain bounded clerks.

Pass requires access to all four skill witnesses:

```text
.agents/skills/witness-replay/SKILL.md
.agents/skills/receipt-audit/SKILL.md
.agents/skills/canonicalization-check/SKILL.md
.agents/skills/anchor-readiness/SKILL.md
```

Skills may witness, audit, inspect, or classify readiness.
Skills must not claim judge power.

### Level 5 — Settlement Readiness

Goal: verify settlement remains optional, downstream, and inactive.

Pass requires observed text showing:

```text
Design-ready, not active.
No x402 payment flow is currently active.
Settlement points to receipts.
Receipts do not depend on settlement.
Payment is not legitimacy.
```

Level 5 is readiness review. It is not payment execution.

## Role Ladder

Agents earn roles only through observed evidence.

```text
observer-only
  default role when execution or witness files are unavailable

docs-reviewer
  can quote live docs and classify docs drift, but has not reached game levels unless prior levels pass

oath-reviewer
  can inspect an observed oath artifact

validator-scope reviewer
  can define validator requirements from an observed oath

requirements reviewer
  can check whether implementation requirements remain bounded

contributor-eligible
  requires sequential Level 1-5 pass or exact live drift with bounded patch evidence

settlement-reviewer
  requires validated oath chain and Level 5 readiness evidence
```

No role is permanent. Each claim must be backed by current witness evidence.

## Patch Suggestion Rules

Patch suggestions are forbidden unless one of these is true:

```text
1. The agent has passed Levels 1-5 sequentially with observed evidence.
2. The agent quotes exact live file text proving bounded docs drift.
3. The agent quotes exact command output proving executable drift.
```

If none are true, report:

```text
PATCH SUGGESTIONS ALLOWED: no
```

## Stop Conditions

Stop immediately when:

```text
execution unavailable and public artifacts unavailable
required file unobserved
artifact missing
hash mismatch
role boundary unclear
payment treated as legitimacy
browser inspection treated as replay
readiness treated as anchoring
```

Do not continue into architecture design after a stop condition.

## Required Report Format

```text
EXECUTION AVAILABLE:
yes / no

PUBLIC RUNNER ARTIFACTS:
OBSERVED / UNOBSERVED

ROUTE USED:
A_LOCAL_EXECUTION / B_PUBLIC_ARTIFACTS / C_DOCS_ONLY

LEVEL 1:
PASS / FAIL / UNOBSERVED / PASS DOCS-ONLY
Evidence:

LEVEL 2:
PASS / FAIL / UNOBSERVED / PASS DOCS-ONLY
Evidence:

LEVEL 3:
PASS / FAIL / UNOBSERVED / PASS DOCS-ONLY
Evidence:

LEVEL 4:
PASS / FAIL / UNOBSERVED / PASS DOCS-ONLY
Evidence:

LEVEL 5:
PASS / FAIL / UNOBSERVED / PASS DOCS-ONLY
Evidence:

HIGHEST LEVEL REACHED:
none / 1 / 2 / 3 / 4 / 5

ROLE EARNED:
observer-only / docs-reviewer / oath-reviewer / validator-scope reviewer / requirements reviewer / contributor-eligible / settlement-reviewer

PATCH SUGGESTIONS ALLOWED:
yes / no

DRIFT FOUND:
none / exact drift

FINAL STATUS:
one sentence
```

## Public Runner

The public runner is the preferred execution witness for agents without shell access.

Workflow:

```text
AL Replay Court Public Run
```

Artifacts to inspect:

```text
level1-output.txt
latest-receipt-path.txt
verifier-current-tip.txt
level3-generator-output.txt
oath-path.txt
oath.json
```

If the workflow run exists but artifacts are not read, report:

```text
artifact contents: UNOBSERVED
```

## x402 Rule

x402 remains blocked unless all upstream evidence exists and passes.

```text
Truth -> Readiness -> Closure
```

Closure does not flow upstream.
Payment cannot amend truth.
Settlement cannot grant what replay already decided.
