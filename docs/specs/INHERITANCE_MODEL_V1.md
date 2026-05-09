# Inheritance Model v1

**Identity:** `jaywisdom.base.eth`  
**Standard:** `INHERITANCE_MODEL_V1`  
**Applies To:** Family Node Attestation Trees, War Board, Meme MetaVerse, Daily Docker Dockets  
**Status:** PUBLIC REPO CANON — GITHUB DIRECT

## Purpose

This specification defines how parent, family, and child nodes inherit legibility without falsely inheriting onchain certification.

The law comes before the map.

A renderer may display inheritance only according to this model.

## Core Doctrine

Parent reference makes a child legible.

Dedicated child attestation makes a child independently witnessed.

A visual edge is not a certification event.

A green node must be backed by a verified receipt.

A gray node must remain visibly pending.

## Node Classes

| Node Class | Meaning |
|---|---|
| `PARENT_ANCHOR` | Upper-level EAS or receipt reference |
| `FAMILY_NODE` | Doctrine layer that defines parent-child inheritance |
| `CHILD_SURFACE` | Repo document, dashboard, receipt, schema candidate, UI, or docket |
| `DEDICATED_CHILD_ANCHOR` | Child surface with its own verified UID or receipt |

## Edge Classes

| Edge Class | Visual | Meaning |
|---|---|---|
| `LEGIBILITY_EDGE` | dashed gray | Parent makes child discoverable / readable |
| `WITNESS_EDGE` | solid green | Child has verified dedicated witness |
| `PENDING_EDGE` | dotted amber | Planned attestation or schema exists but not verified |
| `REVOKED_EDGE` | red struck line | Prior witness exists but is revoked or superseded |

## Renderer Law

A renderer MUST NOT show a child as independently onchain unless that child has one of:

1. Observer-A-verified EAS UID
2. verified schema UID
3. committed receipt with explicit verification proof

A renderer MAY show a child as parent-referenced if it appears in a valid Family Node index.

A renderer MUST expose non-claims wherever a child is only parent-referenced.

## Status Mapping

| Status | Color | Meaning |
|---|---|---|
| `PUBLIC_REPO_CANON` | white | Exists in public repo canon |
| `PARENT_REFERENCED` | gray | Legible under parent reference only |
| `DEDICATED_SCHEMA_PENDING` | amber | Schema planned but UID absent or unverified |
| `DEDICATED_ATTESTATION_PENDING` | amber | Attestation planned but UID absent or unverified |
| `DEDICATED_ONCHAIN_VERIFIED` | green | Dedicated child UID verified |
| `REVOKED_VISIBLE` | red | Revoked or corrected, still visible |

## Required Truth Boundary

Every Family Node renderer must surface:

```json
{
  "parent_reference": true,
  "family_node_navigation_enabled": true,
  "dedicated_child_attestations": "PENDING_OR_VERIFIED_PER_CHILD",
  "non_claims_visible": true
}
```

## Non-Claims

A parent reference does not mean:

- the child is independently onchain
- the child is Meta certified
- the child has a resolver contract
- the child is immutable
- the child cannot later be corrected or revoked

## Constitutional Rule

The map is a servant of the law.

No color, edge, or badge may imply a receipt that does not exist.

The joke can fly. The receipt must land.
