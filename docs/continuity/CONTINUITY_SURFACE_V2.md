# CONTINUITY_SURFACE_V2

## Status

SPEC_FIRST_DRAFT

## Purpose

CONTINUITY_SURFACE_V2 defines the bidirectional provenance layer connecting public continuity, GitHub receipts, ACTIVE_LANES projection, EAS attestations, and Zora 1155 distribution.

This specification is not an on-chain action, mint instruction, or authority claim. It defines the rules that must exist before any Zora 1155 mint, EAS SchemaUID registration, payment unlock, or PR promotion can be treated as replay-admissible.

Core invariant:

```text
No public artifact becomes authority through display.
No Zora mint becomes proof without receipt binding.
No EAS attestation becomes green without replay.
No ACTIVE_LANES projection can promote status beyond its source JSON.
```

## Bidirectional Flow

V2 supports two replay-safe directions.

### Forward Flow

```text
Zora 1155
→ EAS attestation
→ CONTINUITY_INDEX.json
→ ACTIVE_LANES.json
→ public replay surface
```

### Reverse Flow

```text
Public replay surface
→ ACTIVE_LANES.json
→ CONTINUITY_INDEX.json
→ EAS attestation
→ Zora 1155 metadata
```

Both flows are valid only if every hop includes a stable pointer, receipt hash, commit SHA, transaction hash, UID, CID, or replayable public URL.

## Source-of-Truth Rules

The source hierarchy is:

1. `WORLD_MAP.md` — continuity spine and replay entry point.
2. `CONTINUITY_INDEX.json` — continuity anchor registry.
3. `ACTIVE_LANES.json` — lane status source for machine-speed ALMS and homepage projection.
4. `assets/active-lanes.js` — projection bridge only.
5. `index.html` — human-facing display only.
6. EAS/Zora — distribution and attestable receipt surfaces, not automatic authority.

Rules:

- JSON state outranks HTML display.
- Commit history outranks narrative.
- Replay verdict outranks dashboard appearance.
- Zora/EAS pointers must bind back to GitHub receipts.
- No artifact may claim `GREEN` unless its promotion gate passes.

## Zora 1155 Mapping

A Zora 1155 token may represent a continuity badge, court receipt, PDF Empire proof, replay milestone, or payment-unlock artifact.

Required mapping fields:

```json
{
  "zora_contract": null,
  "token_id": null,
  "network": "base",
  "metadata_uri": null,
  "continuity_entry_id": null,
  "continuity_commit": null,
  "receipt_hash": null,
  "eas_schema_uid": null,
  "eas_attestation_uid": null,
  "authority": "distribution_only"
}
```

Zora mint status classes:

- `MINT_DRAFT` — metadata or token plan exists, no mint.
- `MINTED_UNVERIFIED` — mint exists, not replay-bound.
- `MINTED_REPLAYABLE` — mint links to continuity entry and replay receipt.
- `MINTED_GREEN` — replay passed, pointers verified, no fake green.

## EAS SchemaUID Mapping

EAS schemas describe the attestation shape for continuity-linked Zora receipts.

Candidate schema string:

```text
string tokenId,string zoraContract,string metadataURI,string continuityCommit,string receiptHash,bool isSoulbound,uint256 mintTimestamp
```

Required EAS fields for V2 registry entries:

```json
{
  "schema_uid": null,
  "schema_string": null,
  "registry_tx_hash": null,
  "resolver": "0x0000000000000000000000000000000000000000",
  "revocable": true,
  "network": "base",
  "status": "PENDING"
}
```

Schema status classes:

- `PENDING` — drafted but not registered.
- `REGISTERED_UNVERIFIED` — registered but not replay-checked.
- `VALIDATED` — schema UID, tx hash, and schema string verified.
- `DEPRECATED` — superseded by a later schema.

## ACTIVE_LANES Projection Rules

`ACTIVE_LANES.json` remains the machine-readable lane state source.

The homepage may project lanes dynamically, but may not mutate or promote them.

Projection rules:

- `assets/active-lanes.js` may fetch `ACTIVE_LANES.json`.
- Projection must use DOM node creation and `textContent`, not raw HTML string authority.
- JSON remains data-only.
- CSS classes are presentation only.
- Missing fetch must fall back to static conservative lane display.
- A lane may show `GREEN` only if `ACTIVE_LANES.json` says `GREEN` and its schema gate permits it.

## Replay Reflex Arc

A replay reflex arc is a deterministic trigger path that starts from any public artifact and resolves back to its authority source.

Examples:

```text
Homepage pill
→ ACTIVE_LANES.json lane
→ CONTINUITY_INDEX.json entry
→ receipt hash / commit SHA
→ replay verdict
```

```text
Zora token
→ metadata URI
→ EAS UID
→ continuity entry
→ GitHub receipt
→ replay verdict
```

```text
EAS attestation
→ SchemaUID
→ continuity entry
→ ACTIVE_LANES lane
→ public replay surface
```

Replay output classes:

- `PASS` — deterministic pointers resolve and hashes match.
- `PENDING` — pointers exist but replay has not run.
- `FAIL` — mismatch, broken pointer, or invalid status promotion.
- `UNAVAILABLE` — no replay engine or missing required input.

## No Fake Green Conditions

A V2 artifact must not claim `GREEN` unless all of the following are true:

1. A stable source pointer exists.
2. A commit SHA, transaction hash, UID, CID, or receipt hash exists.
3. Replay verifier can resolve every required pointer.
4. Replay verdict is `PASS`.
5. `delta_h` equals `0`.
6. The public UI does not promote beyond the source JSON.
7. Zora/EAS metadata binds back to GitHub continuity receipts.

If any condition fails, the artifact must be classified as one of:

- `REPORTED`
- `REPORTED_UNVERIFIED`
- `PENDING`
- `INFERRED`
- `BLOCKED`

## Promotion Gates

### Gate 1 — Spec Gate

Required before any V2 implementation:

- `docs/continuity/CONTINUITY_SURFACE_V2.md` exists.
- Spec is committed to `master`.
- World Map continuity gate remains green.

### Gate 2 — Schema Gate

Required before EAS registration:

- Schema string reviewed.
- Expected fields documented.
- Failure modes documented.
- No mint or attestation claims green.

### Gate 3 — Metadata Gate

Required before Zora mint:

- Metadata template exists.
- Continuity entry ID exists.
- GitHub commit pointer exists.
- Authority field is `distribution_only` unless replay promotes it.

### Gate 4 — Replay Gate

Required before promotion:

- Replay verifier resolves GitHub, EAS, and Zora pointers.
- Replay verdict is `PASS`.
- `delta_h` is `0`.
- ACTIVE_LANES source agrees with rendered homepage.

### Gate 5 — Public Surface Gate

Required before public GREEN language:

- Homepage renders current lane state from JSON.
- WORLD_MAP.md links the continuity layer.
- CONTINUITY_INDEX.json includes the relevant pointer.
- No UI-only proof claims exist.

## Current V2 Boundary

As of this specification:

```text
V2_SPEC: DRAFT_COMMITTED_PENDING_REPLAY
ZORA_MINT: NOT_STARTED
EAS_SCHEMA_REGISTRATION: NOT_STARTED
ACTIVE_LANES_PROMOTION: NOT_STARTED
NO_FAKE_GREEN: PRESERVED
```

Next authorized artifact after this spec is a schema or metadata draft, not an on-chain transaction.
