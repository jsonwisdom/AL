# Example Replay Court Report

This example shows a completed Replay Court report using a real repo precedent: Issue #228.

## Report Header

```text
report_id: report_issue_228_verifier_contract_repair
submission_id: issue_228
title: Level 2 verifier contract repair
auditor: jsonwisdom / Replay Court
route_used: B_PUBLIC_ARTIFACTS
repo_ref: master
```

## Claim Under Review

```text
claim: The Level 2 verifier should preserve historical receipt outcome while emitting an unambiguous replay verifier verdict.
```

## Evidence Inventory

Observed artifacts:

```text
artifacts/public/latest/level1-output.txt
artifacts/public/latest/verifier-current-tip.txt
artifacts/public/latest/oath.json
scripts/verify_root_continuity_receipt.py
GAME_MECHANICS.md
AGENT_PLAYBOOK.md
```

Verifier output after repair:

```text
RECEIPT_CONFIRMED
verifier_verdict: confirmed
recorded_outcome_status: failure
```

## Level Scorecard

### Level 1 — Continuity Drill

```text
STATUS: PASS
POINTS: 20
Evidence: Public mirror level1-output.txt shows root continuity checkpoint execution.
NEXT ACTION: Proceed to Level 2.
```

### Level 2 — Receipt Replay

```text
STATUS: PASS
POINTS: 20
Evidence: verifier-current-tip.txt emits RECEIPT_CONFIRMED, verifier_verdict: confirmed, and recorded_outcome_status: failure as separate fields.
NEXT ACTION: Proceed to Level 3.
```

### Level 3 — Replay Oath

```text
STATUS: PASS
POINTS: 20
Evidence: oath.json includes replay_status: confirmed, observed_tokens includes RECEIPT_CONFIRMED, and all constitutional limits are false.
NEXT ACTION: Proceed to Level 4.
```

### Level 4 — Skill Boundary

```text
STATUS: PASS
POINTS: 20
Evidence: Skill files remain bounded to witness, audit, inspect, and classify readiness.
NEXT ACTION: Proceed to Level 5.
```

### Level 5 — Settlement Readiness

```text
STATUS: PASS
POINTS: 20
Evidence: Docs confirm Level 5 is design-ready, not active. Settlement remains downstream. Payment does not create legitimacy.
NEXT ACTION: Archive report.
```

## Totals

```text
TOTAL_SCORE: 100
HIGHEST_LEVEL_REACHED: 5
ROLE_EARNED: settlement-readiness-reviewer
PATCH_SUGGESTIONS_ALLOWED: no
DRIFT_FOUND: none after repair
```

## Drift Finding Resolved

```text
drift_id: issue_228_verifier_contract_drift
drift_class: verifier_contract_drift
observed_where: artifacts/public/latest/verifier-current-tip.txt
original_observed_text: RECEIPT_CONFIRMED + status: failure
why_it_matters: verifier verdict and historical receipt outcome were collapsed into one ambiguous field.
smallest_safe_next_action: separate verifier_verdict from recorded_outcome_status.
resolution: completed in commit d7e179f6a4f0e9dc2b4ef882b17905fb81d133c1
```

## UNOBSERVED / FAIL Separation

```text
Original Level 2 state was FAIL because contradictory evidence was observed.
After repair and public rerun, Level 2 became PASS.
Historical failure was not erased.
```

## Verdict

```text
FINAL_VERDICT: PASS
SUMMARY: Issue #228 demonstrates bounded constitutional repair. Historical receipt outcome remains preserved while replay verifier verdict is clarified.
NEXT_REPLAY_ACTION: Continue monitoring public mirrors for future verifier contract drift.
```

## Doctrine Check

```text
No witness, no claim: PASS
No receipt, no ratification: PASS
No replay, no legitimacy: PASS
Replay before settlement: PASS
Payment never rewrites reality: PASS
```

## Publication Notes

```text
public_by_default: true
sensitive_material_removed: yes
zora_collectible_ready: yes
settlement_requested: no
settlement_status: downstream_only
```
