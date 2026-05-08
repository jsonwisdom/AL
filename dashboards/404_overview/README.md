# 404 Overview Dashboard

Status: STATIC_OBSERVATION_LAYER

## Constitutional Constraints

This dashboard renders only:

- values from the 404 runtime AllowedSurface subset
- raw receipt fields
- raw counts
- links to raw receipt JSON

This dashboard must not:

- compute or display scores
- apply color-coding that implies good or bad judgment
- show trend arrows
- add concern, risk, suspicion, blame, or priority language
- rank or compare domains by anything except raw count
- summarize motive, intent, guilt, corruption, legitimacy, or institutional worth

## Data Sources

- `receipts/**/*.json` where `circuit_id == "404_v1"`

## Display Elements

### Daily Verdict Counts

- Source: raw receipt verdict counts by day
- Sort: chronological
- Semantics: raw count only

### CRAWLER_BLOCKED by Domain

- Source: raw `CRAWLER_BLOCKED` receipts
- Columns: domain, count, latest_timestamp, latest_receipt_id
- Sort: count descending
- Semantics: crawler state only, not institutional intent

### Recent Receipts

- Columns: timestamp, domain, verdict, receipt_id
- Sort: reverse chronological
- Verdict column renders raw AllowedSurface string

### Raw Receipt Viewer

- JSON only
- No summarization
- No interpretation layer

## State

```json
{
  "dashboard": "STATIC_OBSERVATION_LAYER",
  "allowed_surface": "404_RUNTIME_SUBSET_ONLY",
  "scores": "FORBIDDEN",
  "interpretation": "FORBIDDEN",
  "mainnet_authority": "NOT_ACTIVE"
}
```
