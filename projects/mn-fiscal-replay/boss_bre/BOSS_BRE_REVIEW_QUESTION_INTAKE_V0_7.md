# Boss Bre Review Question Intake v0.7

## Reviewed Anomaly Lead Payload Question Intake

**Requires Human Review**  
**Source-Backed Fiscal Risk Signal Only**  
**PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW**  
**NO_FAKE_GREEN: ACTIVE**

## Purpose

This intake records reviewer questions about Boss Bre reviewed anomaly lead payloads and routes them to evidence-backed responses. It is review material only and does not authorize final public conclusions.

## Source Payload

```text
projects/mn-fiscal-replay/boss_bre/latest_lead_payload.json
```

Payload ID:

```text
9ebc3651-b198-4e93-97a0-b0ab869275ec
```

Primary reviewed high lead:

```text
BBRISK_MEDICAID_CMS_WITHHOLDING
```

Related artifacts:

```text
projects/mn-fiscal-replay/boss_bre/BOSS_BRE_DISTRIBUTION_LOG_V0_5.md
projects/mn-fiscal-replay/boss_bre/BOSS_BRE_ACKNOWLEDGMENT_RECEIPT_V0_6.md
```

## Intake Entry Format

Append one JSON object per reviewer question intake.

```json
{
  "intake_id": "UUID",
  "intake_utc": "ISO_TIMESTAMP",
  "payload_id": "9ebc3651-b198-4e93-97a0-b0ab869275ec",
  "payload_sha256": "sha256:FULL_PAYLOAD_HASH_FROM_V0_3",
  "reviewer": "Reviewer Name / Entity / Handle",
  "reviewer_contact": "email/handle if applicable",
  "questions": [
    {
      "question_id": "Q1",
      "question_text": "Exact reviewer question",
      "context": "Specific lead or artifact referenced"
    }
  ],
  "response_status": "Pending | Evidence_Provided | Clarification_Requested | Closed",
  "evidence_responses": [
    {
      "question_id": "Q1",
      "response_summary": "Concise evidence-backed answer. Review-only.",
      "source_references": [
        "sha256:SOURCE_HASH_OR_REPO_PATH"
      ],
      "response_utc": "ISO_TIMESTAMP"
    }
  ],
  "notes": "This intake records questions on a reviewed lead payload only. It does not authorize final public conclusions.",
  "distribution_version": "0.5",
  "receipt_version": "0.6",
  "intake_version": "0.7",
  "public_content_claim": "BLOCKED_PENDING_HUMAN_REVIEW",
  "claim_status": "REVIEW_QUESTION_INTAKE_ONLY",
  "human_review_required": true,
  "no_fake_green": true
}
```

## Current Status

- Awaiting first reviewer questions on Payload v0.3.
- All entries enforce: reviewed anomaly lead, source-backed fiscal risk signal, human review required.

## Response Status Values

Allowed values:

- Pending
- Evidence_Provided
- Clarification_Requested
- Closed

## Evidence Response Requirements

Every evidence response must include:

- Exact reviewer question being answered.
- Concise neutral response summary.
- One or more source references using repo paths or `sha256:` hashes.
- Response timestamp.
- Same blocked public-claim gate.

## Gates

PUBLIC_CONTENT_CLAIM: `BLOCKED_PENDING_HUMAN_REVIEW`  
CLAIM_STATUS: `REVIEW_QUESTION_INTAKE_ONLY`  
HUMAN_REVIEW_REQUIRED: `true`  
NO_FAKE_GREEN: `ACTIVE`
