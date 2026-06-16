# RENDER_LAYER_V0_1

Status: DRAFT_READY
Authority: false
Membrane: HOLDS

## Purpose

The render layer converts locked receipts, specifications, reports, and public-facing summaries into human-readable export surfaces such as HTML, PNG, social cards, civic explainers, or publication-ready pages.

It is a presentation layer only.

## Core Rule

Receipts first. Render second.

A rendered page, image, card, or export must never create truth, authority, verification, or proof by appearance alone.

## Allowed Inputs

- Locked receipt records
- Draft specifications clearly marked as draft
- Public reports with source references
- Anomaly observations with authority false
- Governance or replay summaries with stated status

## Forbidden Promotions

The render layer must not silently promote:

- OBSERVATION to CLAIM
- CLAIM to RECEIPT
- RECEIPT to VERIFIED_RECEIPT
- DISPUTED_RECORD to RESOLVED_RECORD
- UNKNOWN to FACT
- Presentation quality to evidentiary strength

## Required Render Metadata

Each rendered artifact should preserve or display:

- artifact_id
- source_record or source_path
- render_version
- generated_at, when known
- authority: false
- evidence_state
- verification_state
- source_hash, when available

## Tool Fit

HTML Anything may be used as a local-first render tool for producing HTML, PNG, or platform-specific exports.

Tool posture:

```json
{
  "tool": "HTML Anything",
  "layer": "render",
  "truth_source": false,
  "authority": false,
  "best_use": [
    "receipt cards",
    "public reports",
    "civic explainers",
    "social export surfaces",
    "documentation previews"
  ],
  "membrane": "HOLDS"
}
```

## Invariant

Pretty output is not proof.

If the underlying record is incomplete, disputed, unknown, or unverified, the rendered artifact must preserve that state visibly.
