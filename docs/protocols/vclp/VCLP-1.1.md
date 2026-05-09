# VCLP 1.1 — Source Binding Axes

**Status:** Live on master
**Verifier:** `docs/protocols/vclp/verify.sh`
**Effective:** 2026-05-08

## Core Principle

VCLP verifies **integrity and binding** — not truth. Claims are self-contained. Source binding is cryptographic, not normative.

## Required Fields for vclp-1.1 Entries

Every vclp-1.1 ledger entry **must** include:

```json
{
  "schema_version": "vclp-1.1",
  "claim_id": "unique-identifier",
  "claim_text": "The claim content",
  "prev_hash": "sha256:<hash of previous line>",
  "artifacts": {
    "text_hash": "sha256:<sha256(claim_text)>",
    "source_hash": "sha256:<raw source bytes>",
    "source_media_type": "application/pdf | text/plain | ..."
  }
}
```

## Verification Axes

The verifier outputs three axes per entry:

| Axis | Values | Meaning |
|------|--------|--------|
| `chain` | `ok` / `broken` | prev_hash matches previous line |
| `text` | `ok` / `mismatch` | text_hash matches claim_text |
| `source` | `legacy` / `bound` / `missing` | source binding status |

### Source Binding Values

- **`source=legacy`** – vclp-1.0 entry (no source_hash required)
- **`source=bound`** – vclp-1.1 entry with valid source_hash + media_type
- **`source=missing`** – vclp-1.1 entry missing source binding (fails verification)

## Summary Counters

```
VCLP_SOURCE source_bound=<n> source_legacy=<n> source_missing=<n>
VCLP_FAILURES invalid_json=<n> missing_required=<n> hash_mismatch=<n> chain_break=<n>
```

## Verdicts

| Verdict | Meaning |
|---------|--------|
| `PASS_STRONG` | All entries source-bound, no failures |
| `PASS_WITH_LEGACY_SOURCE_NAMED_ONLY` | Mixed legacy + bound, no failures |
| `FAIL` | Any failure detected |

## Legacy Policy

- **No backfill** – existing vclp-1.0 entries are preserved as-is
- **No mutation** – history is never rewritten
- **Forward only** – new entries must be vclp-1.1 with source binding

## Source Hash Definition

`source_hash = sha256(<raw source bytes>)`

- No normalization, no encoding conversion
- Exactly the bytes of the source document as stored
- Media type declares how to interpret those bytes

## Integrity, Not Truth

VCLP does NOT verify:
- Whether the claim is factually correct
- Whether the source document is authoritative
- Whether the source media type is appropriate

VCLP verifies:
- The claim text matches its declared hash
- The source bytes match their declared hash
- The chain of custody is unbroken
- Source binding is present when required

## Example vclp-1.1 Entry

```json
{
  "schema_version": "vclp-1.1",
  "claim_id": "example-001",
  "claim_text": "Water freezes at 0°C at sea level",
  "prev_hash": "sha256:60a1e54c56c9d43288289230d53830caeff4dda3eaab10d653b22ed3fa186731",
  "artifacts": {
    "text_hash": "sha256:9e107d9d372bb6826bd81d3542a419d6b9e4b85e8c5d6f4e6c3b5c4d3a2b1c0d",
    "source_hash": "sha256:eb7f5f4a8b2c3d1e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f",
    "source_media_type": "text/plain"
  }
}
```

## Upgrading from vclp-1.0

Not required. Legacy entries remain valid. To bind a legacy entry to its source, create a **new** vclp-1.1 entry with:

- Same `claim_text` (or updated version)
- `source_hash` + `source_media_type`
- Proper `prev_hash` chain to previous entry

This preserves provenance while adding binding.
