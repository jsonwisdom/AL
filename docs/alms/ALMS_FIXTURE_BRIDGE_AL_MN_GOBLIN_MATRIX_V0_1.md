# ALMS_FIXTURE_BRIDGE_AL_MN_GOBLIN_MATRIX_V0_1

Classification: FIXTURE_BRIDGE  
Mode: FULL_VELOCITY_COMMIT  
Operational Root: jsonwisdom/AL  
Matrix: GOBLIN_MATRIX_V0_1  
Authority: false  
Verified: false  
No Fake Green: true

---

## Purpose

Bridge the current MN Matrix / Stearns narrative to actual fetchable ALMS fixture surfaces in `jsonwisdom/AL`.

This artifact does not accept pasted execution claims as verified. It separates:

1. Fetchable ALMS fixture evidence found in AL.
2. Newly asserted Stearns execution narrative that still requires its own receipt payload.

---

## Found ALMS Fixture Surfaces

A GitHub commit search and commit fetch located an existing ALMS audit/report fixture commit:

```json
{
  "commit_sha": "63a0e45dd656f4ee4ff02b418ecc82678efe9a9f",
  "message": "Add daily ALMS JSON audit report",
  "created_at": "2026-05-18T07:45:18Z",
  "repo": "jsonwisdom/AL"
}
```

The fetched commit contains a daily ALMS JSON audit report made of path/hash/byte records. Representative fixture families include:

```json
[
  {
    "family": "ALMS advisory",
    "example_paths": [
      "_truth/advisory/alms_advisory_20260428T052518Z/advisory.json",
      "_truth/advisory/alms_advisory_20260428T052518Z/manifest.json",
      "_truth/advisory/alms_advisory_20260428T052518Z/pinata_response.json"
    ]
  },
  {
    "family": "ALMS goblin court",
    "example_paths": [
      "_truth/alms/goblin-court/episode-002/alms-receipt.json"
    ]
  },
  {
    "family": "ALMS cards and EAS payloads",
    "example_paths": [
      "_truth/alms_cards/alms_trilogy_v1.json",
      "_truth/alms_cards/eas/alms_sequence_v1_payloads.json"
    ]
  },
  {
    "family": "ALMS anchors",
    "example_paths": [
      "_truth/anchors/ALMS_ATTESTATION_CLAIMS_LEDGER_2026-05-05.json",
      "_truth/anchors/ALMS_SCHEMA_ATTESTATION_CANDIDATE_2026-05-05.json",
      "_truth/anchors/alms_checkpoint_latest.json"
    ]
  },
  {
    "family": "MN county FIPS fixture",
    "example_paths": [
      "_truth/bigquery/mn_county_fips_87_manifest.json"
    ]
  }
]
```

---

## Existing ALMS Auto-Run Trail

A commit search also located a run trail of historical ALMS auto-run updates in `jsonwisdom/AL`, including:

```json
[
  {
    "sha": "295e72a19898a5dff8c1dc2486db155a90beece7",
    "message": "ALMS auto-run update",
    "created_at": "2026-05-19T02:22:01Z"
  },
  {
    "sha": "d236e3cd6e3d388541c5edec815585f64606d12c",
    "message": "ALMS auto-run update",
    "created_at": "2026-05-19T01:18:47Z"
  },
  {
    "sha": "26cb18a13c0e37e07ed27785ac2b40594bfe4bdb",
    "message": "ALMS auto-run update",
    "created_at": "2026-05-19T00:09:34Z"
  },
  {
    "sha": "218691d86116cf27744a389ed1243bf574812953",
    "message": "ALMS auto-run update",
    "created_at": "2026-05-18T23:38:17Z"
  },
  {
    "sha": "be17f87219f29392f8c16cb10b132cd22de9cd46",
    "message": "ALMS auto-run update",
    "created_at": "2026-05-18T23:08:49Z"
  }
]
```

These commits prove an ALMS auto-run trail exists. They do not by themselves prove the Stearns execution narrative.

---

## Current Claimed Payload Under Review

The following Stearns / Goblin Matrix payload was asserted in chat and must be classified as a claim until the referenced receipt bytes, hashes, and source documents are attached:

```json
{
  "surface_id": "MN_STEARNS_SEED_SURFACE_001",
  "matrix_version": "GOBLIN_MATRIX_V0_1",
  "claimed_status": "EXECUTED",
  "claimed_tombstone": "ARMED + VERIFIED",
  "claimed_linkage_hash": "39cb785",
  "claimed_budget_ref": "StCloud_2026_GovFunds_100.8M_Dec1_2025",
  "claimed_minutes_ref": "ADID_2311_Dec1_2025",
  "claimed_integrity": "VERIFIED",
  "classification": "UNPROVEN_CLAIM_PENDING_RECEIPT"
}
```

---

## Hard Downgrades Applied

```text
CLAIMED EXECUTED != EXECUTED
CLAIMED VERIFIED != VERIFIED
CLAIMED TOMBSTONE != TOMBSTONE
CLAIMED BUDGET LINK != RECEIPT BYTES
CLAIMED INTEGRITY != HASH-VERIFIED INTEGRITY
GREEN ACROSS THE BOARD != ADMISSIBLE STATUS
```

---

## Bridge Rule

A Stearns surface may bridge into ALMS only when it includes:

```json
{
  "required_for_bridge": [
    "source_url_or_file_path_for_dec_1_2025_minutes",
    "raw_receipt_object_bytes_or_verbatim_text",
    "sha256_of_receipt_object",
    "custodian_or_source_attribution",
    "timestamp_or_fetch_time",
    "storage_location_or_commit_sha",
    "replay_instructions"
  ]
}
```

---

## Current Machine State

```json
{
  "artifact": "ALMS_FIXTURE_BRIDGE_AL_MN_GOBLIN_MATRIX_V0_1",
  "state": "BRIDGE_CREATED_FIXTURES_FOUND_STEARNS_CLAIM_UNPROVEN",
  "ALMS_fixture_trail_found": true,
  "MN_87_county_fixture_found": true,
  "Stearns_execution_payload_verified": false,
  "Stearns_execution_payload_classification": "CLAIMED_NOT_VERIFIED",
  "authority": false,
  "verified": false,
  "no_fake_green": true,
  "next_gate": "ATTACH_STEARNS_RECEIPT_BYTES_AND_HASH"
}
```

---

## Goblin Ruling

ALMS fixtures found. MN county fixture found. Stearns execution narrative not yet proven. Full velocity does not override receipts. Green denied until bytes arrive.
