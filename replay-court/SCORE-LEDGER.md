# Replay Court Score Ledger

The Score Ledger preserves Replay Court scoring as a first-class constitutional memory surface.

Scores are not vibes.
Scores are replayable claims about observed evidence.

## Purpose

```text
Make scoring inspectable.
Make progression claims replayable.
Make score changes traceable.
Prevent score laundering.
Prevent progression inflation.
```

## Core Rule

```text
No score without evidence.
No progression without prior PASS states.
No score repair without preserved contradiction.
```

## Score Entry Schema

Each score entry should include:

```text
score_id:
created_at:
report_id:
submission_id:
route_used:
artifact_refs[]:
level_1_status:
level_1_points:
level_1_evidence_hash:
level_2_status:
level_2_points:
level_2_evidence_hash:
level_3_status:
level_3_points:
level_3_evidence_hash:
level_4_status:
level_4_points:
level_4_evidence_hash:
level_5_status:
level_5_points:
level_5_evidence_hash:
total_score:
highest_level_reached:
role_earned:
drift_found:
linked_report_ref:
linked_repair_ref:
linked_contradiction_ref:
previous_score_hash:
score_hash:
```

## Valid Status / Point Mapping

```text
PASS: 20
FAIL: 0
UNOBSERVED: 0
PASS DOCS-ONLY: 5
```

Levels 1-3 may only use:

```text
PASS
FAIL
UNOBSERVED
```

Levels 4-5 may use `PASS DOCS-ONLY` only as telemetry when prior executable levels are incomplete.

## Highest Level Rule

```text
highest_level_reached = highest sequential level where all prior levels are PASS and that level is PASS
```

A later observed document or artifact does not increase `highest_level_reached` if an earlier level is FAIL or UNOBSERVED.

## Score Repair Rule

A score may be corrected only by adding a new score entry.

Do not edit old score entries to make history clean.

A score correction must reference:

```text
- prior score_id
- contradiction_ref
- repair_ref if applicable
- reason for correction
```

## Entry 001 — Issue #228 post-repair full pass

```text
score_id: score_001_issue_228_post_repair
created_at: 2026-05-17T12:28:17Z
report_id: report_issue_228_verifier_contract_repair
submission_id: issue_228
route_used: B_PUBLIC_ARTIFACTS
artifact_refs:
  - artifacts/public/latest/level1-output.txt
  - artifacts/public/latest/verifier-current-tip.txt
  - artifacts/public/latest/oath.json
level_1_status: PASS
level_1_points: 20
level_1_evidence_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
level_2_status: PASS
level_2_points: 20
level_2_evidence_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
level_3_status: PASS
level_3_points: 20
level_3_evidence_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
level_4_status: PASS
level_4_points: 20
level_4_evidence_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
level_5_status: PASS
level_5_points: 20
level_5_evidence_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
total_score: 100
highest_level_reached: 5
role_earned: settlement-readiness-reviewer
drift_found: none after repair
linked_report_ref: replay-court/example-report/README.md
linked_repair_ref: repair_001_issue_228_verifier_contract
linked_contradiction_ref: contradiction_001_issue_228_verifier_status
previous_score_hash: GENESIS
score_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
```

## Validation Rules

A score entry is invalid if:

```text
- any status is outside allowed values
- any point value violates the status / point mapping
- Levels 1-3 use PASS DOCS-ONLY
- total_score does not equal the sum of level points
- highest_level_reached ignores an earlier FAIL or UNOBSERVED
- evidence hash is missing for a claimed PASS
- score correction lacks contradiction_ref
```

## Doctrine

```text
Scores record observed replay posture.
Scores do not create truth.
Scores do not authorize settlement.
Scores do not erase drift.
Scores do not replace receipts.
```

## Invariant

```text
A score is legitimate only if it can be replayed from evidence.
```
