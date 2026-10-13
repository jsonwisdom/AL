# Boss Bre AL Checked-In Bytes Replay Board

UTC: 2026-08-25T23:53:23Z

## Status

- Scope: `checked-in AL Act 2025-251 PDF bytes plus claim/gate/snapshot/CI witnesses`
- Source PDF: `fixtures/al/sources/al_budget_act_2025_251.pdf`
- PDF hash: sha256:ecf65398c0a34307065aa78d0eafbfbfe4641405cc4a1a14d796058522a78206
- Claim hash: sha256:ecf65398c0a34307065aa78d0eafbfbfe4641405cc4a1a14d796058522a78206
- Hash status: HASH_OBSERVED_MATCH
- Extract status: EXTRACTED
- Anomaly leads: 9
- HIGH: 5
- MEDIUM: 2
- LOW: 2
- Leads hash: sha256:49a3eda4c5fc0af976d3a67f0fc18d28d1ce80e82affb7e9671d22c1b57ff0db

## Doctrine

Boss Bre publishes **audit leads**, not fraud verdicts.

- PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW
- HUMAN_REVIEW_REQUIRED: TRUE
- NO_FAKE_GREEN: ACTIVE
- CLAIM TYPE: ANOMALY_LEAD_ONLY
- authority: false
- AL PASS flipped: false
- fraud_verdict: false
- network_fetch: false

## Latest leads

```json
[
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "projects/mn-fiscal-replay/boss_bre/al_checked_in_replay/extracted/al_budget_act_2025_251.pdf.txt",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "Total 1523 The Department of Public Health will reimburse the Alabama Medicaid Agency the state 1524 match necessary to cover increased revenues for services as a result of fee 1525 increases. The Department of Public Health will be r",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "projects/mn-fiscal-replay/boss_bre/al_checked_in_replay/extracted/al_budget_act_2025_251.pdf.txt",
    "rule_id": "BBRISK_FRAUD_RISK_LANGUAGE",
    "severity": "HIGH",
    "label": "FRAUD_RISK_LANGUAGE_REQUIRES_REVIEW",
    "evidence_excerpt": "As provided in Section 27-2-39, Code of Alabama 1975. 1815 (4) Insurance Fraud Unit Fund 361,943 1816 As provided in Sections 27-12A-1 through 27-12A-42, Code of Alabama 1975. 1817 (5) Reduced Ciga",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "projects/mn-fiscal-replay/boss_bre/al_checked_in_replay/extracted/al_budget_act_2025_251.pdf.txt",
    "rule_id": "BBRISK_DEFICIT_SHORTFALL_VARIANCE",
    "severity": "HIGH",
    "label": "DEFICIT_SHORTFALL_OR_UNEXPLAINED_VARIANCE",
    "evidence_excerpt": "ee years of 1399 October 1, 2025, in a primary care service area with a deficit, or surplus 1400 of less than 2.0 primary-care physicians, as shown by the most-recent Status 1401 Report of the Alabama Primary Care Physician",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "projects/mn-fiscal-replay/boss_bre/al_checked_in_replay/extracted/al_budget_act_2025_251.pdf.txt",
    "rule_id": "BBRISK_PROGRAM_REDUCTION_OR_RESERVE_DRAW",
    "severity": "MEDIUM",
    "label": "PROGRAM_REDUCTION_OR_RESERVE_DRAW",
    "evidence_excerpt": "and judicial agencies of the State, 5 for other functions of government, for debt service, and for 6 capital outlay for the fiscal year ending September 30, 2026. 7 BE IT ENACTED BY THE LEGISLATURE OF ALABAMA: 8 Section 1. The monie",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "projects/mn-fiscal-replay/boss_bre/al_checked_in_replay/extracted/al_budget_act_2025_251.pdf.txt",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "84,749,919 84,749,919 1807 SOURCE OF FUNDS: 1808 (1) Center for Risk and 1,500,000 1809 Insurance Research Fund 1810 (2) Fire Marshal's Fund 728,198",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "fixtures/al/al_budget_2026_claim.json",
    "rule_id": "BBRISK_CLAIM_REPLAY_PENDING",
    "severity": "HIGH",
    "label": "EVIDENCE_CHAIN_CLAIM_STILL_PENDING",
    "evidence_excerpt": "claim.receipt.status=INDETERMINATE; claim.replay.status=PENDING; replay_passed=False; notes=Official source candidate selected. Awaiting frozen PDF commit, hash, and replay confirmation.; pdf_hash_status=HASH_OBSERVED_MATCH. Frozen PDF commit is present. This is a lead, not a PASS flip.",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "fixtures/al/sources/al_budget_snapshot_2026-05-03.txt",
    "rule_id": "BBRISK_PLACEHOLDER_SOURCE_PENDING",
    "severity": "MEDIUM",
    "label": "PLACEHOLDER_SNAPSHOT_STILL_PENDING",
    "evidence_excerpt": "Placeholder snapshot still self-declares OFFICIAL_SOURCE_PENDING while Act 2025-251 PDF bytes are checked in.",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "alms/national/national_root_ci_latest.json",
    "rule_id": "BBRISK_CI_PASS_VS_GATE",
    "severity": "HIGH",
    "label": "CI_AL_PASS_CONFLICTS_WITH_CLAIM_AND_GATE",
    "evidence_excerpt": "national_root_ci_latest.json records AL status=PASS while the claim receipt is INDETERMINATE and replay_passed=False. Hashable is not verified. No fraud is proven.",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  },
  {
    "utc": "2026-08-25T23:53:23Z",
    "lane": "AL",
    "source_path": "data/boss_bre_anomaly_rules.json",
    "rule_id": "BBRISK_RULE_COVERAGE_GAP",
    "severity": "LOW",
    "label": "LARGE_DOLLAR_RULE_MISSES_RAW_INTEGERS",
    "evidence_excerpt": "BBRISK_LARGE_DOLLAR_AMOUNT looks for '$N million/billion' language. Act 2025-251 uses raw integers such as 84,749,919. Coverage gap only.",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true,
    "authority": false,
    "fraud_verdict": false
  }
]
```
