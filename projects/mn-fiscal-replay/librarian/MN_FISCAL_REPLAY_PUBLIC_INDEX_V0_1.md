# MN Fiscal Replay — Public Lineage Index v0.1

**Status:** Public doorway, not raw evidence dump  
**Policy:** `NO_FAKE_GREEN_ACTIVE`  
**Rule:** `DISCOVERY_BEFORE_DELEGATION`  
**Current machine index:** `MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_3.json`

---

## Why this file exists

The raw Librarian JSON is a machine receipt. It proves that the system can identify sealed lanes and block public claims, but it is not the public product experience.

This document is the human-facing doorway for the Minnesota Fiscal Replay lane. A visitor should not be forced to inspect raw JSON, grep the repository, or rediscover months of project work. The index must summarize:

1. what exists,
2. where it lives,
3. what is sealed,
4. what is blocked,
5. what comes next.

---

## Current public-safe status

| Lane | Status | Public claim | Content delta? | Current ruling |
|---|---|---|---|---|
| `MN_001` | `MAINTENANCE_SAFE_BASELINE` | `BLOCKED` | `false` | Public content anomaly unproven |
| `MN_002` | `MAINTENANCE_SAFE_BASELINE` | `BLOCKED` | `false` | Public content anomaly unproven |

Both lanes are maintained as safe baselines. Hash drift and chunk drift were observed, but the reviewed differences were classified as PDF extraction/layout artifacts rather than proven fiscal content changes.

---

## Sealed evidence paths

### MN_001

- Source manifest: `_sources/MN_001/source_manifest.json`
- Final safe status: `projects/mn-fiscal-replay/live_fetch/MN_001/MN_001_FINAL_SAFE_STATUS_V0_1.json`
- Chunk verdict: `projects/mn-fiscal-replay/live_fetch/MN_001/chunks/MN_001.chunked_verdict.json`
- Human review: `projects/mn-fiscal-replay/reviews/MN_001_CHUNK_REVIEW_CLASSIFICATION_V0_1.md`

### MN_002

- Source manifest: `_sources/MN_002/source_manifest.json`
- Final safe status: `projects/mn-fiscal-replay/live_fetch/MN_002/MN_002_FINAL_SAFE_STATUS_V0_1.json`
- Chunk verdict: `projects/mn-fiscal-replay/live_fetch/MN_002/chunks/MN_002.chunked_verdict.json`
- Human review: `projects/mn-fiscal-replay/reviews/MN_002_CHUNK_REVIEW_CLASSIFICATION_V0_1.md`

---

## What the public should understand

This project does not say, “the state changed the document,” merely because a hash changed.

The replay lane separates:

- raw PDF hash drift,
- extracted text drift,
- normalized text drift,
- chunk-level drift,
- human-reviewed content change.

The first four can happen because PDF extraction tools read page markers, footnotes, tables of contents, and layout structure differently. A public content claim requires the last step: confirmed substantive fiscal content change.

For `MN_001` and `MN_002`, that claim is **not proven**. Therefore public claims remain blocked.

---

## Boss Bre gate

`NO_FAKE_GREEN_ACTIVE`

- No public claim without final safe status.
- No final status without chunk receipt.
- No chunk receipt without source manifest.
- No manual URL hunt when a Librarian index exists.
- No raw dump as the public click path.

---

## Librarian rule

`DISCOVERY_BEFORE_DELEGATION`

Before asking the operator to find a source, the system must search the sealed repo lineage first.

The machine index currently reports:

- `maintenance_safe_baselines = 2`
- `public_claims_blocked = 2`
- `manual_operator_file_search_required = false`

---

## Next target

`BOSS_BRE_V1_6_CLEANUP_OR_DISCOVER_NEXT_MANIFEST`

The next lane is not invented manually. The system must discover the next source manifest, or it must say that no next manifest is currently indexed.

---

## Public page instruction

Public-facing pages should link to this file first, then to the raw JSON and receipt files.

The raw JSON is evidence. This document is the doorway.
