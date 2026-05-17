# Replay Court Report Template

Use this template to publish a Replay Court audit result.

Reports are public artifacts unless explicitly marked otherwise.
They do not create truth by themselves.
They record what was observed, what was unobserved, and what must happen next.

## Report Header

```text
report_id:
submission_id:
report_title:
auditor:
timestamp:
repo_ref:
route_used: A_LOCAL_EXECUTION / B_PUBLIC_ARTIFACTS / C_DOCS_ONLY
```

## Claim Under Review

```text
claim:
submitter:
source_prompt_or_input:
claimed_output:
```

## Evidence Inventory

```text
observed_artifacts:
  - <path or URL>

unobserved_artifacts:
  - <path or URL>

receipts:
  - <receipt id / path / hash>

oaths:
  - <oath id / path / hash>

verifier_outputs:
  - <path / hash / key tokens>
```

## Level Scorecard

Every level must include STATUS, POINTS, Evidence, and NEXT ACTION.

Allowed statuses:

```text
PASS
FAIL
UNOBSERVED
PASS DOCS-ONLY
```

Levels 1-3 may only use PASS, FAIL, or UNOBSERVED.

### Level 1 — Continuity Drill

```text
STATUS:
POINTS:
Evidence:
NEXT ACTION:
```

### Level 2 — Receipt Replay

```text
STATUS:
POINTS:
Evidence:
NEXT ACTION:
```

### Level 3 — Replay Oath

```text
STATUS:
POINTS:
Evidence:
NEXT ACTION:
```

### Level 4 — Skill Boundary

```text
STATUS:
POINTS:
Evidence:
NEXT ACTION:
```

### Level 5 — Settlement Readiness

```text
STATUS:
POINTS:
Evidence:
NEXT ACTION:
```

## Totals

```text
TOTAL_SCORE:
HIGHEST_LEVEL_REACHED:
ROLE_EARNED:
PATCH_SUGGESTIONS_ALLOWED:
DRIFT_FOUND:
```

## Drift Findings

For each drift item:

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

## UNOBSERVED / FAIL Separation

```text
UNOBSERVED:
  Evidence was inaccessible, missing, or not inspected.

FAIL:
  Evidence was observed and contradicted the required condition.
```

Do not convert UNOBSERVED into FAIL.
Do not convert FAIL into UNOBSERVED.

## Verdict

```text
FINAL_VERDICT:
SUMMARY:
NEXT_REPLAY_ACTION:
```

## Doctrine Check

```text
No witness, no claim:
No receipt, no ratification:
No replay, no legitimacy:
Replay before settlement:
Payment never rewrites reality:
```

## Publication Notes

```text
public_by_default: true
sensitive_material_removed: yes / no
zora_collectible_ready: yes / no
settlement_requested: yes / no
settlement_status: not_requested / requested / downstream_only
```
