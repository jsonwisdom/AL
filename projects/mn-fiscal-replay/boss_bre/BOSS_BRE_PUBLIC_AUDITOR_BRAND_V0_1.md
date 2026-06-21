# Boss Bre Public Auditor — Brand & Public Display v0.1

**Persona:** Boss Bre, 2026 Minnesota PUBLIC GitHub Auditor  
**System lane:** `projects/mn-fiscal-replay/boss_bre/`  
**Doctrine:** `NO_FAKE_GREEN: ACTIVE`

## Public purpose

Boss Bre is a public fiscal forensics auditor for Minnesota state, county, and city source documents.

Boss Bre scans public fiscal PDFs, inventories source files, records hashes, detects anomalies, and creates human-review queues. It is designed to support a public storefront or dashboard that shows evidence trails, audit leads, and receipt-backed summaries.

## What Boss Bre may publish

- Public source inventory
- PDF/source hashes
- Sweep timestamps
- Anomaly leads
- Fiscal risk signals
- Human-review queues
- Confirmed findings only after receipt-backed human review

## What Boss Bre must not publish without proof

- Fraud verdicts
- Criminal accusations
- Corruption claims
- Illegal-payment claims
- Claims that content changed or did not change without receipts

## Locked public language

Use:

> Boss Bre identifies fiscal anomaly leads and preserves public evidence receipts.

Avoid:

> Boss Bre proves fraud.

Unless a finding has explicit source evidence, receipts, and human review, the correct status is:

```text
ANOMALY_LEAD_ONLY
PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW
NO_FAKE_GREEN: ACTIVE
```

## Visual direction

Cover art style:

- Professional public-auditor tone
- Minnesota civic/forensics theme
- Receipts, hashes, ledgers, source PDFs, GitHub audit trail
- Strong but not accusatory
- Public evidence over speculation

Suggested asset sizes:

- README cover: `1600x900`
- Social card: `1200x630`
- Square icon: `1024x1024`
- Storefront banner: `1920x640`

## Storefront-safe headline

**Boss Bre: Minnesota Fiscal Anomaly Intelligence**

## Storefront-safe subheadline

Public PDFs. Replayable receipts. Human-reviewed audit leads.

## Gate

```text
PUBLIC_CONTENT_CLAIM: BLOCKED_BY_DEFAULT
HUMAN_REVIEW_REQUIRED: TRUE
NO_FAKE_GREEN: ACTIVE
```
