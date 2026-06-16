# VCLP 1.2 Threat Model

**Status:** Draft
**Target:** After `vclp-v1.1.0`
**Focus:** CRLF/LF equivalence, `source_text_hash`, and the integrity/authenticity boundary.

## Core Problem

VCLP 1.1 verifies:

- `text_hash` = SHA256 of `claim_text` as stored in JSON
- `source_hash` = SHA256 of raw observed source bytes
- chain integrity via `prev_hash`

Missing: the relationship between `claim_text` and the source document's extracted text.

## Attack Vector

An adversary could:

1. Bind a claim to a source document via `source_hash`.
2. Extract text from that source document.
3. Make a different claim than what the source actually says.
4. VCLP 1.1 would still report `source=bound` because it checks source byte binding, not semantic alignment.

## VCLP 1.2 Additions

### 1. `source_text_hash`

```json
{
  "artifacts": {
    "text_hash": "sha256:<claim_text>",
    "source_text_hash": "sha256:<canonical extracted source text>",
    "source_hash": "sha256:<raw source bytes>",
    "source_media_type": "text/plain"
  }
}
```

Purpose: bind the ledger entry to an extracted text projection of the source, not only the raw source bytes.

### 2. CRLF/LF Equivalence

Line-ending normalization test vector:

- source text extracted with CRLF (`\r\n`)
- same source text extracted with LF (`\n`)
- both produce the same `source_text_hash`

Implementation target: normalize to LF before hashing extracted text.

### 3. Integrity vs Authenticity Boundary

| Layer | VCLP 1.1 | VCLP 1.2 |
|---|---|---|
| Raw source bytes | `source_hash` | `source_hash` |
| Extracted text | not checked | `source_text_hash` |
| Claim text | `text_hash` | `text_hash` |
| Chain | `prev_hash` | `prev_hash` |

VCLP verifies integrity of binding: source bytes -> extracted text -> claim text.

VCLP does not verify truth, accuracy, or authenticity of the source document itself.

## Test Vector Requirements

For v1.2 adoption, entries with `schema_version: "vclp-1.2"` and textual source media types should:

1. Provide `source_text_hash`.
2. Demonstrate CRLF/LF equivalence with canonical LF-only hashing.
3. Define whether `claim_text` must be an exact match, substring, or structured assertion over the source text.

## Migration from 1.1

- No breaking change for existing v1.1 entries.
- New fields are additive.
- The verifier continues to accept v1.1 entries without `source_text_hash`.
- A future `PASS_STRONG_V1_2` verdict requires `source_text_hash` on all v1.2+ textual-source entries.

## Next Steps

1. Define extraction rules per media type: plain text, Markdown, HTML, JSON, PDF.
2. Specify canonical LF normalization.
3. Define claim-vs-source text policy: exact, substring, or structured assertion.
4. Implement CRLF/LF test vectors.
5. Extend CI only after the v1.2 verifier is implemented.

## Relationship to CI Gate

The current CI gate `.github/workflows/vclp-verify.yml` enforces VCLP 1.1.

VCLP 1.2 CI enforcement will be added only after `schema_version: "vclp-1.2"` verifier behavior and test vectors are implemented.
