# DTS Table I Normalization Spec v0.1

## Scope

This spec defines deterministic normalization for Treasury Can Audit v0.1.1.

Target source:

Daily Treasury Statement  
Table I — Operating Cash Balance

Canonical FiscalData endpoint:

`/v1/accounting/dts/operating_cash_balance`

This spec does not cover Table II, Table III, debt operations, deposits and withdrawals, policy analysis, benefit calculations, or congressional reporting claims.

## Authority Boundary

The normalized output is a shadow-audit observation only.

It is not an official Treasury audit.
It is not a policy claim.
It is not a dividend claim.
It is not a congressional report.

Authority may be marked `SHADOW_AUDIT` only when raw data capture, normalization, hashing, detached Ed25519 signature, and local verification all pass.

## Input Requirements

The input must be the raw API response bytes captured from the canonical FiscalData endpoint.

The raw snapshot must be saved before normalization.

The raw snapshot must be hashed with SHA-256 and recorded as:

`raw_input_hash`

If the source fetch fails, no normalized success receipt may be produced. The pipeline must emit a signed failure receipt with `replay_status: FETCH_BLOCKED`.

## Deterministic Ordering

Rows must be sorted by:

1. `record_date`
2. `src_line_nbr`
3. stable lexical fallback of the full row if required

No runtime-dependent ordering is allowed.

## Numeric Handling

No floats are allowed in canonical normalized JSON.

Numeric source values must be represented as integer dollars when possible.

If the source value is denominated in millions of dollars, convert by multiplying by 1,000,000 and store as an integer.

If a numeric field cannot be safely parsed, normalization must fail with:

`NORMALIZATION_FAILED`

Do not silently coerce malformed values.

## Canonical JSON

Canonical JSON must use:

- UTF-8
- sorted keys
- compact separators
- no insignificant whitespace

Python equivalent:

```python
json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
```

## Required Normalized Fields

Each normalized Table I receipt must include:

- `schema_version`
- `source_table`
- `record_date`
- `authority_level`
- `replay_status`
- `normalizer_version`
- `normalizer_code_hash`
- `raw_input_hash`
- `normalized_receipt_hash`
- `parent_receipt_hash`
- `rows`

Each row should preserve, when available:

- `record_date`
- `account_type`
- `src_line_nbr`
- `open_today_bal`
- `open_month_bal`
- `open_fiscal_year_bal`
- `close_today_bal`
- `close_month_bal`
- `close_fiscal_year_bal`

Normalized numeric balance fields should be represented as integer dollars, not floats.

## Normalizer Code Hash

`normalizer_code_hash` must hash the source text of the normalizer function or module, not Python bytecode.

Bytecode hashes are not stable across Python versions.

## Signature Boundary

The detached signature must sign the canonical normalized receipt payload.

The public key must be derived from the local private signing key and written into the receipt.

The public key must not be hardcoded.

Private keys must never be committed.

## Parent Chaining

The first successful receipt may use:

`parent_receipt_hash: null`

Later successful receipts should set `parent_receipt_hash` to the previous successful normalized receipt hash.

Failure receipts may also be chained, but must not be represented as successful audit observations.

## Replay Conditions

A Table I receipt is green only if:

1. raw snapshot hash matches
2. normalized receipt canonical hash matches
3. normalizer code hash is present
4. detached Ed25519 signature verifies
5. parent receipt hash is present or genesis-null
6. `replay_status` is `PASS`

If any check fails, the receipt is not green.

## Core Rule

No receipt = no authority.  
No signature = no authority.  
No replay = no audit claim.  
Failed fetch = signed failure.  
PASS receipt = admissible shadow observation.
