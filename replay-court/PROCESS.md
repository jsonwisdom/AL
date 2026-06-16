# Replay Court Process

This document explains how a Replay Court submission moves from intake to public report.

The process exists to preserve evidence discipline while making audits repeatable, public, and useful.

```text
Intake -> Evidence Inventory -> Replay -> Drift Analysis -> Bounded Repair -> Public Report -> Optional Settlement
```

Settlement is downstream.
Payment never creates legitimacy.

## Step 1 — Intake

Use:

```text
replay-court/INTAKE.md
```

Collect:

```text
- submitter
- claim or question
- prompt / input
- claimed output
- supporting artifacts
- verification targets
- desired output format
- confidentiality note
```

If the submission lacks enough evidence, mark missing material as `UNOBSERVED` and request the smallest next artifact.

## Step 2 — Evidence Inventory

Create an inventory of observed and unobserved artifacts.

Observed artifacts may include:

```text
- public URLs
- receipts
- verifier output
- oath JSON
- workflow logs
- commits
- screenshots
- repo files
```

Unobserved artifacts must remain explicitly marked.

Do not infer missing files.
Do not convert inaccessible evidence into failure.

## Step 3 — Route Selection

Choose the strongest available route.

```text
A_LOCAL_EXECUTION
  Run commands directly and capture stdout/stderr.

B_PUBLIC_ARTIFACTS
  Inspect public committed mirrors or public workflow artifacts.

C_DOCS_ONLY
  Inspect documentation only.
```

Route priority:

```text
A if available
else B if public artifacts are available
else C
```

No shell access is not an excuse to stop if Route B artifacts exist.

## Step 4 — Level Scoring

Use:

```text
GAME_MECHANICS.md
```

Every level must include:

```text
STATUS:
POINTS:
Evidence:
NEXT ACTION:
```

Allowed statuses:

```text
PASS
FAIL
UNOBSERVED
PASS DOCS-ONLY
```

Levels 1-3 may not use `PASS DOCS-ONLY`.

## Step 5 — Drift Analysis

For every drift item, record:

```text
drift_id:
drift_class:
observed_where:
observed_text:
why_it_matters:
smallest_safe_next_action:
```

Common drift classes:

```text
status_schema_drift
level_status_drift
scoring_drift
progression_drift
verifier_contract_drift
authority_creep
settlement_confusion
artifact_access_drift
```

## Step 6 — Bounded Repair

If drift is confirmed, repair only the smallest boundary.

A repair must not:

```text
- erase historical evidence
- collapse distinct states
- grant new authority
- activate settlement
- rewrite the report for narrative cleanliness
```

A repair should:

```text
- preserve historical truth
- clarify semantics
- rerun public artifacts
- refresh mirrors
- rescore honestly
```

## Step 7 — Public Report

Use:

```text
replay-court/REPORT-TEMPLATE.md
```

A report must include:

```text
- claim under review
- evidence inventory
- level scorecard
- totals
- drift findings
- UNOBSERVED / FAIL separation
- verdict
- doctrine check
- publication notes
```

## Step 8 — Archive / Publish

Publish the report as one or more:

```text
- repo report folder
- GitHub issue comment
- branded dashboard image
- social post
- optional Zora collectible-ready artifact
```

Reports are public by default unless limited handling was justified at intake.

## Step 9 — Optional Settlement

Settlement may happen only after replay and reporting.

```text
Truth -> Readiness -> Closure
```

Tips, payments, or x402 settlement support the work.
They do not create truth.
They do not rewrite the report.
They do not erase failures.

## Process Invariant

```text
No witness, no claim.
No receipt, no ratification.
No replay, no legitimacy.
Replay before settlement.
Payment never rewrites reality.
```
