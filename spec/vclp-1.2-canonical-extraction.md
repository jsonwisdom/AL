# VCLP 1.2 Canonical Extraction

**Status:** Draft intent
**Baseline:** `vclp-v1.1.0`
**Scope:** byte-to-canonical-bytes extraction for TXT, HTML, and PDF source artifacts.

## 1. Scope and Non-goals

VCLP 1.2 defines a deterministic extraction layer from observed source bytes to canonical text bytes.

In scope:

- TXT canonical extraction
- HTML canonical extraction
- PDF canonical extraction
- deterministic canonical byte output
- `source_text_hash = sha256(canonical_bytes)`

Out of scope:

- truth verification
- source authenticity
- OCR
- layout reconstruction
- language detection
- semantic interpretation
- substring or positional claim binding

## 2. Normative Definitions

A compliant extractor MUST be deterministic for identical input bytes and declared media type.

A compliant extractor MUST emit one of:

- `OK`
- `INDETERMINATE`
- `TAINTED`

`INDETERMINATE` means the extractor cannot produce canonical bytes without implementation-dependent judgment.

`TAINTED` means the input uses a hostile, ambiguous, or prohibited construct that makes the extracted text unsafe for binding.

`INDETERMINATE` and `TAINTED` are protocol-level results, not implementation errors.

## 3. Class Selection

Class selection MUST be based on declared `source_media_type` and observed byte signatures.

- `text/plain`, `text/markdown`, and `text/csv` select TXT.
- `text/html` selects HTML.
- `application/pdf` selects PDF.

UTF-8 BOM MAY appear only for TXT-like classes and MUST be removed before canonical output.

Unknown or conflicting magic bytes MUST return `INDETERMINATE`.

## 4. Per-class Pipelines

### TXT

TXT extraction pipeline:

1. Validate bytes as UTF-8.
2. Remove UTF-8 BOM if present.
3. Apply global Unicode and whitespace normalization.
4. Emit canonical bytes.

Invalid UTF-8 MUST return `TAINTED`.

### HTML

HTML extraction pipeline:

1. Parse with a deterministic HTML5 parser profile.
2. Walk text-producing nodes in document order.
3. Decode entities deterministically.
4. Drop script/style/noscript content.
5. Apply global Unicode and whitespace normalization.
6. Emit canonical bytes.

Parser recovery that differs across compliant implementations MUST return `INDETERMINATE` until the parser profile is locked.

### PDF

PDF extraction pipeline:

1. Validate PDF header and object structure.
2. Require ToUnicode mappings for extracted glyph text.
3. Process pages in numeric page order.
4. Process content streams in declared stream order.
5. Permit only the extraction operator subset defined by the future PDF profile.
6. Apply global Unicode and whitespace normalization.
7. Emit canonical bytes.

PDFs requiring OCR MUST return `INDETERMINATE`.

PDFs without required ToUnicode mappings MUST return `INDETERMINATE`.

Hostile or self-modifying PDF constructs MUST return `TAINTED`.

## 5. Global Normalization and Whitespace

All class pipelines that reach canonical output MUST apply:

- UTF-8 output only
- no BOM
- Unicode NFC normalization
- LF line endings only
- no CRLF output
- no trailing spaces
- final newline normalized by profile rule

Whitespace collapse is class-specific and MUST be specified by the active extraction profile before enforcement.

## 6. Canonical Output and Hashing

For VCLP 1.2:

```text
source_text_hash = sha256(canonical_bytes)
```

The hash input MUST be exactly the emitted canonical bytes.

No rendered view, screenshot, PDF layout surface, or human summary is an acceptable hash input.

## 7. Failure Semantics

| Condition | Result | Verifier obligation |
|---|---|---|
| Invalid UTF-8 in TXT | TAINTED | REJECT |
| Unknown class conflict | INDETERMINATE | ACCEPT_WITH_FLAG or REJECT by policy |
| PDF requires OCR | INDETERMINATE | ACCEPT_WITH_FLAG or REJECT by policy |
| Missing PDF ToUnicode | INDETERMINATE | ACCEPT_WITH_FLAG or REJECT by policy |
| Hostile PDF construct | TAINTED | REJECT |
| Parser-dependent HTML recovery | INDETERMINATE | ACCEPT_WITH_FLAG or REJECT by policy |

## 8. Binding Policy Deferred

VCLP 1.2 canonical extraction does not define substring, positional, or semantic claim binding.

Until a binding anchor specification exists, the verifier MUST NOT claim that `claim_text` is semantically entailed by `source_text_hash`.

VCLP verifies integrity of binding, not truth.

## 9. Reference Profiles

Future reference profiles:

- `TXT-1.2-REF`
- `HTML-1.2-REF`
- `PDF-1.2-REF`

Each profile MUST provide:

- golden fixtures
- canonical outputs
- SHA256 hashes
- replay commands
- at least one independent implementation check before CI enforcement

## 10. Fixture Layout

Planned layout:

```text
_truth/extraction/fixtures/txt/
_truth/extraction/fixtures/html/
_truth/extraction/fixtures/pdf/
_truth/extraction/golden/txt/
_truth/extraction/golden/html/
_truth/extraction/golden/pdf/
```

The verifier remains unchanged until the extraction profiles and replay corpus are stable.
