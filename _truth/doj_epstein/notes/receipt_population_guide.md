# Receipt Population Guide — DOJ Epstein Public Records

This guide explains how to populate:

```text
_truth/doj_epstein/receipts/receipt.template.json
```

## Core rule

Populate fields only from observed public artifacts and observed operator actions.

Do not infer.
Do not summarize beyond observed content.
Do not claim replay parity before replay exists.

## Field guidance

### `receipt_id`

- Operator-assigned identifier.
- Must uniquely identify the receipt within this lane.

### `status`

Allowed early states:

- `SOURCE_PENDING`
- `INDETERMINATE`
- `INGESTED`

Do not use `MATCH_CONFIRMED` here.

### `source`

Populate only from public references:

- `type`
- `url`
- `docket_reference`
- `retrieved_at_utc`

### `artifact`

Populate from captured bytes only:

- `path`
- `media_type`
- `sha256`
- `byte_length`

No placeholder hashes.

### `description`

Descriptions must remain neutral:

- no accusations
- no narrative framing
- no claims of completeness
- no inferred intent

### `provenance`

Populate only with observed operator actions:

- capture method
- operator identifier
- archive URL if applicable

### `verification`

Before replay exists:

```json
{
  "verdict": "INDETERMINATE",
  "match_confirmed": false
}
```

Do not set stronger verdicts without replay evidence.

## Forbidden actions

- inventing hashes
- inventing timestamps
- inventing URLs
- inventing source content
- using assistant-authored witness bytes
- asserting MATCH_CONFIRMED without replay parity
