# AL Checked-In Bytes Replay — Anomaly Leads

```text
CLAIM                    = ANOMALY_LEAD_ONLY
PUBLIC_CONTENT_CLAIM     = BLOCKED_PENDING_HUMAN_REVIEW
NO_FAKE_GREEN            = ACTIVE
authority                = false
fraud_verdict            = false
network_fetch            = false
AL_PASS_GATE             = INDETERMINATE
```

This report identifies leads from checked-in Alabama bytes. It does not prove fraud. It does not flip AL to PASS.

## Replay command

```bash
python3 scripts/boss_bre_al_checked_in_replay.py
```

Observed run: `2026-08-25T23:53:23Z`

## Observed hash layer

| Field | Value |
|---|---|
| Source | `fixtures/al/sources/al_budget_act_2025_251.pdf` |
| Computed PDF SHA-256 | `sha256:ecf65398c0a34307065aa78d0eafbfbfe4641405cc4a1a14d796058522a78206` |
| Claim hash | `sha256:ecf65398c0a34307065aa78d0eafbfbfe4641405cc4a1a14d796058522a78206` |
| Hash status | `HASH_OBSERVED_MATCH` |
| Extract status | `EXTRACTED` |
| Extract SHA-256 | `sha256:a86a25c4a6e23400936a23e1d4f3fff28bc088423d710a605e36cf8d626ca7c4` |

The extract hash also matches the already-checked-in 2026-07-09 sweep witness at `projects/mn-fiscal-replay/boss_bre/runs/2026-07-09T01-18-24Z/al_budget_act_2025_251.pdf.txt`.

Hashable is not verified. Hash match is not PASS.

## Lead counts

| Class | Count |
|---|---|
| Total | 9 |
| HIGH | 5 |
| MEDIUM | 2 |
| LOW | 2 |
| Leads hash | `sha256:49a3eda4c5fc0af976d3a67f0fc18d28d1ce80e82affb7e9671d22c1b57ff0db` |

## Content leads from Act 2025-251 text

These are first-match rule hits against extracted appropriations text. The matching word is not a finding.

| Severity | Rule | Observed excerpt meaning |
|---|---|---|
| HIGH | `BBRISK_MEDICAID_CMS_WITHHOLDING` | Public Health reimbursement / Alabama Medicaid Agency state match language |
| HIGH | `BBRISK_FRAUD_RISK_LANGUAGE` | Insurance Fraud Unit Fund appropriation cite, not an accusation |
| HIGH | `BBRISK_DEFICIT_SHORTFALL_VARIANCE` | Primary-care physician deficit/surplus threshold, not a budget-deficit verdict |
| MEDIUM | `BBRISK_PROGRAM_REDUCTION_OR_RESERVE_DRAW` | Ordinary "debt service" enactment language |
| LOW | `BBRISK_FORECAST_VOLATILITY` | Center for Risk and Insurance Research Fund label |

`BBRISK_LARGE_DOLLAR_AMOUNT` did not fire. The act uses raw integers such as `84,749,919` instead of `$N million` language.

## Evidence-chain leads

| Severity | Rule | Observation |
|---|---|---|
| HIGH | `BBRISK_CLAIM_REPLAY_PENDING` | Claim receipt remains `INDETERMINATE`, `replay.status=PENDING`, `replay_passed=false`, notes still say the frozen PDF commit is awaited |
| HIGH | `BBRISK_CI_PASS_VS_GATE` | `alms/national/national_root_ci_latest.json` records AL `PASS` while the claim receipt does not |
| MEDIUM | `BBRISK_PLACEHOLDER_SOURCE_PENDING` | `al_budget_snapshot_2026-05-03.txt` still self-declares `OFFICIAL_SOURCE_PENDING` |
| LOW | `BBRISK_RULE_COVERAGE_GAP` | Large-dollar rule misses raw integer appropriations |

The CI `PASS` label is a narrative/state gap. This report does not rewrite that historical CI artifact.

## What this replay refused

- Network fetch of `budget.alabama.gov`
- Flipping AL to `PASS`
- Promoting a public content claim
- Rewriting statewide Boss Bre receipts (`latest_anomaly_leads.jsonl`, `latest_sweep_summary.json`, `latest_anomaly_summary.json`)
- Treating Medicaid / Fraud / deficit word hits as proof of fraud

## Statewide receipts left untouched

The user-supplied Boss Bre lane card remains a historical witness, not this run's output:

```text
LANE                    = projects/mn-fiscal-replay/boss_bre/
SWEEP                   = 2026-07-09T01:18:24Z
RECORDS                 = 951
REPO_PDFS               = 946
BLOCKED_OR_MISSING      = 3
RUNS_OBSERVED           = 349
ANOMALY_SCAN            = 2026-06-22T18:04:47Z
LEADS                   = 34603
HIGH                    = 21199
MEDIUM                  = 851
LOW                     = 12553
LANES                   = 8
LEADS_HASH              = sha256:0f04316ed9093f4c61730a45b472b71c25651b7cdd02e931f9bd4a09308da406
```

Those files were not rewritten.

## Reproduction

```bash
python3 scripts/boss_bre_al_checked_in_replay.py
python3 -m pytest tests/test_boss_bre_al_checked_in_replay.py -q
```

A later replay changes `generated_utc` and therefore the leads JSONL hash. The PDF hash and extract hash must stay stable if the checked-in AL bytes did not change.
