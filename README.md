# AL

## Trinity Mission for the Girls

This repo is part of Jay Wisdom's 3 Daughters Trinity:

- AL
- JOY
- COMPUTERWISDOM

Mission:
Build simple, honest systems that can be read, replayed, and verified.

Rule:
No fake green. No random noise. Start clean.

Status:
Starter README and index live.

---

## Boss Bre Public Auditor

Boss Bre is the Minnesota public fiscal forensics lane for AL.

Purpose:
Scan public Minnesota fiscal documents, inventory source PDFs, preserve hashes, detect anomaly leads, and route possible deltas to human review.

Boss Bre does **not** publish unsupported fraud verdicts. It publishes evidence trails, anomaly leads, and blocked/public-review statuses until receipts and human review support a confirmed finding.

Current gate:

```text
PUBLIC_CONTENT_CLAIM: BLOCKED_BY_DEFAULT
HUMAN_REVIEW_REQUIRED: TRUE
NO_FAKE_GREEN: ACTIVE
```

Key files:

- `projects/mn-fiscal-replay/boss_bre/`
- `data/mn_jurisdictions.json`
- `.github/workflows/boss-bre-public-audit.yml`
- `scripts/boss_bre_runner_v0_2.sh`
- `scripts/boss_bre_anomaly_detector.sh`
- `scripts/boss_bre_librarian.py`

Public positioning:

**Boss Bre: Minnesota Fiscal Anomaly Intelligence**  
Public PDFs. Replayable receipts. Human-reviewed audit leads.
