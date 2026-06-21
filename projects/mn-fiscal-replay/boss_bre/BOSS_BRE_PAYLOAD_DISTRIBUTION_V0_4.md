# Boss Bre Payload Distribution v0.4

## Reviewed Anomaly Lead Payload v0.3

**Requires Human Review**  
**Source-Backed Fiscal Risk Signal**  
**No Public Fraud Verdict**

Payload ID: `9ebc3651-b198-4e93-97a0-b0ab869275ec`  
Rules Version: `0.2`  
High Lead Count: `1`  
Selected High Lead: `BBRISK_MEDICAID_CMS_WITHHOLDING`  
Generated: `2026-06-21T08:25:39Z`

## Distribution Note

This is a reviewed lead payload for human review only. It identifies source-backed fiscal risk signals under active Boss Bre rules. No public fraud verdict, criminal finding, confirmed corruption finding, or final legal determination is made.

Full payload artifact:

```text
projects/mn-fiscal-replay/boss_bre/latest_lead_payload.json
```

## Allowed Language

- Reviewed anomaly lead payload
- Requires human review
- Source-backed fiscal risk signal
- Audit lead
- Anomaly lead
- No public fraud verdict

## Blocked Language Without Further Review

- Fraud proven
- Criminal finding
- Confirmed corruption
- Illegal payment
- Final determination

## Review Instructions

Reviewers must examine selected high leads against primary sources and supporting receipts before any further action. Distribution of this template does not authorize public accusations or final claims.

## Gates

PUBLIC_CONTENT_CLAIM: `BLOCKED_PENDING_HUMAN_REVIEW`  
CLAIM_STATUS: `LEAD_PAYLOAD_ONLY`  
HUMAN_REVIEW_REQUIRED: `true`  
NO_FAKE_GREEN: `ACTIVE`
