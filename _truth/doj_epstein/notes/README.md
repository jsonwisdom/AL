# `_truth/doj_epstein` – public-record intake lane

State: `SOURCE_PENDING`

This directory tree is a **scaffold only** for future ingestion of public-record artifacts related to DOJ-sourced materials.
No evidentiary content, no hashes, and no provenance claims are present in this state.

The intake lane is designed as an ALMS-style “airlock”:

- infrastructure and directory layout may evolve publicly
- evidentiary bytes enter **only** via explicit operator ingestion
- replay and verification discipline apply **after** ingestion

## Directory layout (scaffold only)

- `_truth/doj_epstein/sources/`
  - placeholder for raw public-record source artifacts
  - currently guarded by `.gitkeep` only

- `_truth/doj_epstein/receipts/`
  - placeholder for operator-authored receipts describing ingested artifacts
  - receipts will reference timestamps and cryptographic hashes once ingestion occurs

- `_truth/doj_epstein/manifests/`
  - placeholder for structured manifests that group receipts and sources
  - manifests will support deterministic replay and verification

- `_truth/doj_epstein/diffs/`
  - placeholder for machine-readable diffs between versions of manifests and/or receipts
  - intended for audit-grade change tracking

- `_truth/doj_epstein/notes/`
  - this README and future operator notes about process and governance
  - not an evidence or narrative layer

All non-README files in this scaffold are `.gitkeep` placeholders only.

## Doctrine and constraints

While `state = SOURCE_PENDING`, the following constraints apply:

1. **No source ingestion**
   - No DOJ documents, no transcripts, no media, no derived text.
   - No partial or redacted evidentiary content.

2. **No accusations**
   - This tree does not host accusations, arguments, or narrative framing.
   - Notes must remain procedural and structural.

3. **No claims of completeness**
   - No statements that the intake lane is exhaustive or final.
   - Manifests and receipts, once added, describe what is present, not what is absent.

4. **No invented hashes**
   - All future hashes must be computed from real bytes at ingestion time.
   - No placeholder, mock, or illustrative hash values.

5. **No Amelie root computation**
   - No higher-order or cross-corpus root calculations are performed at this stage.
   - This lane is local to `_truth/doj_epstein/*` until explicitly extended.

6. **No `MATCH_CONFIRMED` semantics**
   - No confirmation flags or match assertions are permitted in this state.
   - Future matching, if any, must be replay-verifiable and operator-authored.

## Valid next transition (external, operator-driven)

The next lawful transition out of `SOURCE_PENDING` is **external**:

- an operator ingests real public-record artifacts into `_truth/doj_epstein/sources/`
- the operator writes receipts with timestamps and hashes into `_truth/doj_epstein/receipts/`
- the operator updates manifests in `_truth/doj_epstein/manifests/` to reference those receipts

Only after those steps do ALMS replay and verification rules attach to this lane.
Until then, this scaffold remains a neutral, non-claim, public-record intake structure.
