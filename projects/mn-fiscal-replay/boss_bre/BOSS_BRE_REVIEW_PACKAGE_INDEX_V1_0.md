# Boss Bre Review Package Index v1.0

## Master Review-Only Package Manifest

**Rules v0.2 + Payload v0.3 + Full Review Chain v0.4 through v0.9**  
**Requires Human Review**  
**Source-Backed Fiscal Risk Signal Only**  
**PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW**  
**NO_FAKE_GREEN: ACTIVE**

## Purpose

This index links the Boss Bre review package into one portable handoff manifest. It is review material only and does not authorize final public conclusions.

## Package Contents

- Rules: `data/boss_bre_anomaly_rules.json` version `0.2`
- Lead Payload: `projects/mn-fiscal-replay/boss_bre/latest_lead_payload.json` version `0.3`
- Distribution Template: `projects/mn-fiscal-replay/boss_bre/BOSS_BRE_PAYLOAD_DISTRIBUTION_V0_4.md`
- Distribution Log Template: `projects/mn-fiscal-replay/boss_bre/BOSS_BRE_DISTRIBUTION_LOG_V0_5.md`
- Acknowledgment Receipt Template: `projects/mn-fiscal-replay/boss_bre/BOSS_BRE_ACKNOWLEDGMENT_RECEIPT_V0_6.md`
- Review Question Intake Template: `projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_QUESTION_INTAKE_V0_7.md`
- Evidence Response Packet Template: `projects/mn-fiscal-replay/boss_bre/BOSS_BRE_EVIDENCE_RESPONSE_PACKET_V0_8.md`
- Review Closeout Disposition Template: `projects/mn-fiscal-replay/boss_bre/BOSS_BRE_REVIEW_CLOSEOUT_DISPOSITION_V0_9.md`

## Payload Summary

Payload ID:

```text
9ebc3651-b198-4e93-97a0-b0ab869275ec
```

Rules version:

```text
0.2
```

High lead count:

```text
1
```

Selected high lead:

```text
BBRISK_MEDICAID_CMS_WITHHOLDING
```

## Manifest Entry Format

Append one JSON object per package release or package refresh.

```json
{
  "package_id": "UUID",
  "release_utc": "ISO_TIMESTAMP",
  "payload_id": "9ebc3651-b198-4e93-97a0-b0ab869275ec",
  "rules_version": "0.2",
  "full_chain_sha256": "sha256:MASTER_HASH_OF_ALL_ARTIFACTS",
  "components": [
    "v0.2_rules",
    "v0.3_payload",
    "v0.4_distribution",
    "v0.5_distribution_log",
    "v0.6_acknowledgment_receipt",
    "v0.7_review_question_intake",
    "v0.8_evidence_response_packet",
    "v0.9_review_closeout_disposition"
  ],
  "review_status": "Active_Review | Closed",
  "notes": "Complete reviewed anomaly lead package for human review only. Source-backed fiscal risk signals. No final public conclusion authorized.",
  "package_version": "1.0",
  "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
  "claim_status": "REVIEW_PACKAGE_INDEX_ONLY",
  "human_review_required": true,
  "no_fake_green": true
}
```

## Usage

Reference this index for full-package review distribution or handoff. Every component remains review-only and must preserve the blocked public-claim gate.

## Gates

PUBLIC_CONTENT_CLAIM: `BLOCKED_PENDING_HUMAN_REVIEW`  
CLAIM_STATUS: `REVIEW_PACKAGE_INDEX_ONLY`  
HUMAN_REVIEW_REQUIRED: `true`  
NO_FAKE_GREEN: `ACTIVE`
