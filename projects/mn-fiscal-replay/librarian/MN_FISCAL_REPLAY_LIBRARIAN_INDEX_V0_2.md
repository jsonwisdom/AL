# MN Fiscal Replay Librarian Index v0.2

`DISCOVERY_BEFORE_DELEGATION`

## Public Page Rule

A visitor must never be asked to rediscover Jay's project history manually. The page must surface lineage first: what exists, where it lives, what is sealed, what is blocked, and what comes next.

## Counts

- `source_manifests`: `2`
- `replay_receipts`: `2`
- `enriched_baselines`: `2`
- `final_safe_status_receipts`: `1`
- `chunk_review_docs`: `1`
- `boss_bre_run_dirs`: `24`
- `mn_live_fetch_lanes`: `5`

## Component Index

| Component | Manifest | Replay | Enriched | Final Status | Public Verdict | Next |
|---|---|---|---|---|---|---|
| `MN019_DAKOTA` | `missing` | `missing` | `missing` | `missing` | `PENDING` | `review candidate` |
| `MN027_HENNEPIN` | `missing` | `missing` | `missing` | `missing` | `PENDING` | `review candidate` |
| `MN062_RAMSEY` | `missing` | `missing` | `missing` | `missing` | `PENDING` | `review candidate` |
| `MNCI_MPLS` | `missing` | `missing` | `missing` | `missing` | `PENDING` | `review candidate` |
| `MN_001` | `_sources/MN_001/source_manifest.json` | `projects/mn-fiscal-replay/replay/MN_001.replay.json` | `projects/mn-fiscal-replay/enriched/MN_001.enriched.json` | `projects/mn-fiscal-replay/live_fetch/MN_001/MN_001_FINAL_SAFE_STATUS_V0_1.json` | `PUBLIC_CONTENT_ANOMALY_UNPROVEN` | `maintenance / safe baseline` |
| `MN_002` | `_sources/MN_002/source_manifest.json` | `projects/mn-fiscal-replay/replay/MN_002.replay.json` | `projects/mn-fiscal-replay/enriched/MN_002.enriched.json` | `missing` | `NO_ANOMALY` | `run from existing manifest` |

## Boss Bre Gate

`PUBLIC_CONTENT_CLAIM = BLOCKED`

Source discovery does not equal a public claim. Evidence must still pass replay, classification, and Boss Bre review.

## Next Best Target

`MN_002_FROM_EXISTING_SOURCE_MANIFEST`

## No Fake Green

`manual_operator_file_search_required = false`

If this index cannot find the lineage, the system must say so explicitly instead of sending the operator to hunt.
