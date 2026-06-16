# ANTI_CROWN_INVARIANTS_001

## Purpose

Define the minimal constitutional constraints that prevent `$BATCH` or any witness surface from becoming an authority primitive.

## Core Reduction

```json
{
  "existence": "CHEAP",
  "lineage": "EXPENSIVE",
  "acceptance": "LINEAGE_ONLY",
  "authority": "IMPOSSIBLE"
}
```

## Forbidden Equivalences

```json
{
  "ownership_equals_authority": false,
  "visibility_equals_truth": false,
  "chain_equals_priesthood": false,
  "market_pressure_equals_governance": false,
  "receipt_equals_meaning": false,
  "indexer_event_equals_continuity": false
}
```

## Remaining Authority Surface

```json
{
  "semantic_authority": "LOCAL_REPLAY",
  "validation_surface": "DETERMINISTIC_REPLAY",
  "lineage_requirement": "CRYPTOGRAPHIC_RECOVERY",
  "participation_proof": "REPLAYABLE_RECEIPT_ONLY"
}
```

## Hard Rules

- Ownership generates no authority.
- Visibility generates no truth.
- Chain settlement generates no meaning.
- Market pressure generates no governance.
- Receipt existence generates no semantics.
- Indexer events generate no continuity.
- Witness scope may not expand authority.
- Governance override of replay is forbidden.
- Ambient authority inheritance is forbidden.
- Proof without replay is non-authoritative.
- Signature without recovery is invalid.
- Deterministic reconstruction is supreme.

## Doctrine

Proof may travel. Meaning stays replayable.
