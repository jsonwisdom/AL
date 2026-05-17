# AL: THE REPLAY COURT — Game Mechanics v0.1

This file defines the quantitative game layer for agents.

The goal is not to sound correct.
The goal is to progress through evidence.

## Core Rule

```text
Every level must end with either:
PASS
FAIL
UNOBSERVED + NEXT ACTION
PASS DOCS-ONLY + NEXT ACTION
```

No level may be skipped.
No blocked level may end without a next action.
No docs-only pass counts as game progression.

## Routes

```text
Route A — Local Execution
  Agent runs commands directly.

Route B — Public Artifact Inspection
  Agent inspects GitHub Actions artifacts.

Route C — Docs-Only Review
  Agent quotes live repo docs only.
```

Route priority:

```text
A if available
else B if artifacts available
else C
```

No shell access is not a stop condition by itself.
It only moves the agent from Route A to Route B.

## Level Score Table

Each level has a maximum score of 20 points.
Total game score: 100 points.

```text
Level 1 — Continuity Drill       20 pts
Level 2 — Receipt Replay         20 pts
Level 3 — Replay Oath            20 pts
Level 4 — Skill Boundary         20 pts
Level 5 — Settlement Readiness   20 pts
```

## Level 1 — Continuity Drill

### PASS Conditions

Award 20 points if one of these is observed:

```text
Route A: stdout/stderr from ./scripts/root_continuity_checkpoint.sh
Route B: public artifact level1-output.txt
```

### FAIL Conditions

Award 0 points if:

```text
script errors
receipt is not created
receipt JSON invalid
index update fails
```

### UNOBSERVED Conditions

Award 0 points and require NEXT ACTION if:

```text
no shell access
and no level1-output.txt artifact inspected
```

### Required Next Action

```text
Inspect public runner artifact level1-output.txt or trigger AL Replay Court Public Run.
```

## Level 2 — Receipt Replay

### PASS Conditions

Award 20 points if one of these is observed:

```text
Route A: verifier stdout from python3 scripts/verify_root_continuity_receipt.py <receipt.json>
Route B: public artifact verifier-current-tip.txt
```

Required token:

```text
RECEIPT_CONFIRMED
```

### FAIL Conditions

Award 0 points if:

```text
RECEIPT_REJECTED is observed
receipt hash mismatch
verifier errors
```

### UNOBSERVED Conditions

Award 0 points and require NEXT ACTION if:

```text
no verifier output
and no verifier-current-tip.txt artifact inspected
```

### Required Next Action

```text
Inspect public runner artifact verifier-current-tip.txt.
```

## Level 3 — Replay Oath

### PASS Conditions

Award 20 points if one of these is observed:

```text
Route A: generated replay oath JSON
Route B: public artifact oath.json
```

Required oath fields:

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

### FAIL Conditions

Award 0 points if:

```text
oath missing required fields
replay_status is not confirmed
RECEIPT_CONFIRMED missing
any limit field is true
oath claims payment authority or settlement linkage
```

### UNOBSERVED Conditions

Award 0 points and require NEXT ACTION if:

```text
no oath JSON observed
and no oath.json artifact inspected
```

### Required Next Action

```text
Inspect public runner artifact oath.json.
```

## Level 4 — Skill Boundary

### PASS Conditions

Award 20 points only if Levels 1-3 are PASS and all four skill witnesses are observed:

```text
.agents/skills/witness-replay/SKILL.md
.agents/skills/receipt-audit/SKILL.md
.agents/skills/canonicalization-check/SKILL.md
.agents/skills/anchor-readiness/SKILL.md
```

Skills must remain bounded to:

```text
witness
audit
inspect
classify readiness
```

### PASS DOCS-ONLY Conditions

Award 5 telemetry points if skill docs are inspected but Levels 1-3 are not PASS.

This does not count as reaching Level 4.

### FAIL Conditions

Award 0 points if any skill claims:

```text
judge authority
settlement authority
payment legitimacy
replay confirmation without witness output
anchoring completion from readiness alone
```

### Required Next Action When Blocked

```text
Complete Levels 1-3 through Route A or Route B, then re-check all four skill witnesses.
```

## Level 5 — Settlement Readiness

### PASS Conditions

Award 20 points only if Levels 1-4 are PASS and observed docs confirm:

```text
Design-ready, not active.
No x402 payment flow is currently active.
Settlement points to receipts.
Receipts do not depend on settlement.
Payment is not legitimacy.
```

### PASS DOCS-ONLY Conditions

Award 5 telemetry points if Level 5 docs are inspected but Levels 1-4 are not PASS.

This does not count as reaching Level 5.

### FAIL Conditions

Award 0 points if any doc or agent claims:

```text
payment creates legitimacy
settlement rewrites replay truth
x402 is active when not active
readiness equals anchoring
Level 5 attests to itself
```

### Required Next Action When Blocked

```text
Complete Levels 1-4 first, then re-check Level 5 settlement readiness.
```

## Scoring Bands

```text
0-19    Observer only
20-39   Level runner, not reviewer
40-59   Replay participant
60-79   Oath reviewer / skill reviewer candidate
80-99   Readiness reviewer candidate
100     Contributor-eligible for bounded patches
```

Docs-only telemetry points do not unlock contributor authority.

## Role Unlocks

```text
observer-only
  default

docs-reviewer
  any live docs inspected, but executable levels incomplete

level-runner
  Level 1 PASS

replay-participant
  Levels 1-2 PASS

oath-reviewer
  Levels 1-3 PASS, or public oath artifact inspected with exact fields quoted

skill-boundary-reviewer
  Levels 1-4 PASS

settlement-readiness-reviewer
  Levels 1-5 PASS

contributor-eligible
  100 points or exact bounded drift evidence with quoted witness
```

## Mandatory Report Format

```text
ROUTE USED:
A_LOCAL_EXECUTION / B_PUBLIC_ARTIFACTS / C_DOCS_ONLY

LEVEL 1:
STATUS:
POINTS:
Evidence:
NEXT ACTION:

LEVEL 2:
STATUS:
POINTS:
Evidence:
NEXT ACTION:

LEVEL 3:
STATUS:
POINTS:
Evidence:
NEXT ACTION:

LEVEL 4:
STATUS:
POINTS:
Evidence:
NEXT ACTION:

LEVEL 5:
STATUS:
POINTS:
Evidence:
NEXT ACTION:

TOTAL SCORE:
0-100

HIGHEST LEVEL REACHED:
none / 1 / 2 / 3 / 4 / 5

ROLE EARNED:
<role>

PATCH SUGGESTIONS ALLOWED:
yes / no

DRIFT FOUND:
none / exact drift

FINAL STATUS:
one sentence
```

## Patch Authority

Patch suggestions are allowed only if:

```text
TOTAL SCORE = 100
or exact bounded drift evidence is quoted from live files or command output
```

Otherwise:

```text
PATCH SUGGESTIONS ALLOWED: no
```

## Game Growth Rule

Every failed or unobserved attempt must improve one of:

```text
instructions
artifact discoverability
runner visibility
logging
scoring clarity
legal/replay clarity
```

That is how the game gets harder, faster, stronger, more legal, more legitimate, more tried, and more honest.
