# Boss Bre Minnesota Anomaly Board

UTC: 2026-06-21T09:27:05Z

## Status

- Anomaly leads: 2748
- HIGH: 1680
- MEDIUM: 89
- LOW: 979
- Unique lanes: 6
- Leads hash: sha256:f0a748b57fb9b8480c82655016ad61a7d2e25dee03af17753f3e29ecb2b1323f

## Doctrine

Boss Bre publishes **audit leads**, not fraud verdicts.

- PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW
- HUMAN_REVIEW_REQUIRED: TRUE
- NO_FAKE_GREEN: ACTIVE
- CLAIM TYPE: ANOMALY_LEAD_ONLY

## Latest leads

```json
[
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_ACKNOWLEDGMENT_RECEIPT_V0_6.md",
    "rule_id": "BBRISK_FRAUD_RISK_LANGUAGE",
    "severity": "HIGH",
    "label": "FRAUD_RISK_LANGUAGE_REQUIRES_REVIEW",
    "evidence_excerpt": "12:This receipt records reviewer acknowledgment or response to a Boss Bre reviewed anomaly lead payload. It does not authorize public fraud claims, criminal findings, confirmed corruption claims, illegal-payment claims, public accusations, or final determinations.",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_ACKNOWLEDGMENT_RECEIPT_V0_6.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "6:**Source-Backed Fiscal Risk Signal Only** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_DISTRIBUTION_LOG_V0_5.md",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "37:BBRISK_MEDICAID_CMS_WITHHOLDING",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_DISTRIBUTION_LOG_V0_5.md",
    "rule_id": "BBRISK_FRAUD_RISK_LANGUAGE",
    "severity": "HIGH",
    "label": "FRAUD_RISK_LANGUAGE_REQUIRES_REVIEW",
    "evidence_excerpt": "12:This log records distribution of Boss Bre reviewed anomaly lead payloads as review material only. It does not authorize public fraud claims, criminal findings, confirmed corruption claims, illegal-payment claims, or final determinations.",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_DISTRIBUTION_LOG_V0_5.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "6:**Source-Backed Fiscal Risk Signal Only** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_EVIDENCE_RESPONSE_PACKET_V0_8.md",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "29:BBRISK_MEDICAID_CMS_WITHHOLDING",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_EVIDENCE_RESPONSE_PACKET_V0_8.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "6:**Source-Backed Fiscal Risk Signal Only** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MACHINE_READABLE_PACKAGE_MANIFEST_V1_1.json",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "75: \"notes\": \"Machine-readable manifest for complete reviewed anomaly lead package. Review material only. Source-backed fiscal risk signals. No final public conclusion authorized.\",",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MACHINE_READABLE_PACKAGE_MANIFEST_V1_1_POPULATED.json",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "75: \"notes\": \"Machine-readable manifest for complete reviewed anomaly lead package. Review material only. Source-backed fiscal risk signals. No final public conclusion authorized.\",",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_PAYLOAD_DISTRIBUTION_V0_4.md",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "12:Selected High Lead: `BBRISK_MEDICAID_CMS_WITHHOLDING` ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_PAYLOAD_DISTRIBUTION_V0_4.md",
    "rule_id": "BBRISK_FRAUD_RISK_LANGUAGE",
    "severity": "HIGH",
    "label": "FRAUD_RISK_LANGUAGE_REQUIRES_REVIEW",
    "evidence_excerpt": "7:**No Public Fraud Verdict**",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_PAYLOAD_DISTRIBUTION_V0_4.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "6:**Source-Backed Fiscal Risk Signal** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_PUBLIC_AUDITOR_BRAND_V0_1.md",
    "rule_id": "BBRISK_FRAUD_RISK_LANGUAGE",
    "severity": "HIGH",
    "label": "FRAUD_RISK_LANGUAGE_REQUIRES_REVIEW",
    "evidence_excerpt": "25:- Fraud verdicts",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_PUBLIC_AUDITOR_BRAND_V0_1.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "19:- Fiscal risk signals",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_CLOSEOUT_DISPOSITION_V0_9.md",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "29:BBRISK_MEDICAID_CMS_WITHHOLDING",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_CLOSEOUT_DISPOSITION_V0_9.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "6:**Source-Backed Fiscal Risk Signal Only** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_PACKAGE_ARCHIVE_V1_4.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "6:**Source-Backed Fiscal Risk Signal Only** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_PACKAGE_INDEX_V1_0.md",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "49:BBRISK_MEDICAID_CMS_WITHHOLDING",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_PACKAGE_INDEX_V1_0.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "7:**Source-Backed Fiscal Risk Signal Only** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_QUESTION_INTAKE_V0_7.md",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "29:BBRISK_MEDICAID_CMS_WITHHOLDING",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_QUESTION_INTAKE_V0_7.md",
    "rule_id": "BBRISK_FORECAST_VOLATILITY",
    "severity": "LOW",
    "label": "FORECAST_VOLATILITY_LANGUAGE",
    "evidence_excerpt": "6:**Source-Backed Fiscal Risk Signal Only** ",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/REVIEW_DECISION_RECORD_TEMPLATE_V0_1.json",
    "rule_id": "BBRISK_FRAUD_RISK_LANGUAGE",
    "severity": "HIGH",
    "label": "FRAUD_RISK_LANGUAGE_REQUIRES_REVIEW",
    "evidence_excerpt": "50: \"must_preserve_no_fraud_verdict_without_source_and_human_review\": true",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/boss_bre_learning_state.json",
    "rule_id": "BBRISK_MISSING_PAYLOAD",
    "severity": "HIGH",
    "label": "EVIDENCE_CHAIN_BLOCKED",
    "evidence_excerpt": "12: \"Treat TODO or unreachable pdf_url as FETCH_BLOCKED\",",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/boss_bre_pdf_inventory.jsonl",
    "rule_id": "BBRISK_MISSING_PAYLOAD",
    "severity": "HIGH",
    "label": "EVIDENCE_CHAIN_BLOCKED",
    "evidence_excerpt": "842:{\"utc\":\"2026-06-21T09:02:09Z\",\"kind\":\"registry_pdf_url\",\"code\":\"MN_001\",\"name\":\"State of Minnesota\",\"url\":\"TODO_MN_STATE_BUDGET_FORECAST_PDF_URL\",\"status\":\"SOURCE_URL_MISSING\",\"http_status\":\"NA\",\"content_type\":\"UNKNOWN\",\"content_length\":\"UNKNOWN\",\"downloaded_sha256\":\"\",\"downloaded_path\":\"\",\"public_content_claim\":\"BLOCKED\",\"no_fake_green\":true}",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  },
  {
    "utc": "2026-06-21T09:27:05Z",
    "lane": "BOSS_BRE",
    "source_path": "projects/mn-fiscal-replay/boss_bre/latest_lead_payload.json",
    "rule_id": "BBRISK_MEDICAID_CMS_WITHHOLDING",
    "severity": "HIGH",
    "label": "MEDICAID_CMS_WITHHOLDING_OR_DISALLOWANCE_RISK",
    "evidence_excerpt": "15: \"BBRISK_MEDICAID_CMS_WITHHOLDING\"",
    "claim_status": "ANOMALY_LEAD_ONLY",
    "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
    "human_review_required": true,
    "no_fake_green": true
  }
]
```
