# Family Node Attestation Tree v1

**Identity:** `jaywisdom.base.eth`  
**Standard:** `FAMILY_NODE_ATTESTATION_TREE_V1`  
**Project Line:** Meme MetaVerse / Jay’s Wisdom War Board  
**Status:** PUBLIC REPO CANON — GITHUB DIRECT

## Purpose

A Family Node is the parent-child attestation structure that keeps public records legible without falsely certifying every child surface as independently onchain.

The Family Node names the upper-level parent, the children, and the truth boundary between them.

## Core Rule

Parent reference makes the child legible.

Dedicated child attestation makes the child independently witnessed.

Do not confuse the two.

## Family Shape

```json
{
  "family_node_id": "WAR_BOARD_FAMILY_NODE_V0_2",
  "parent": {
    "type": "UPPER_LEVEL_EAS_REFERENCE",
    "uid": "0x...",
    "status": "REFERENCED"
  },
  "children": [
    {
      "child_id": "WAR_BOARD_SPEC_V0_2",
      "type": "REPO_SPEC",
      "status": "PUBLIC_REPO_CANON",
      "dedicated_eas_uid": null
    }
  ]
}
```

## Child Statuses

| Status | Meaning |
|---|---|
| `PUBLIC_REPO_CANON` | Child exists as public GitHub replay surface |
| `PARENT_REFERENCED` | Child is legible under a parent reference |
| `DEDICATED_SCHEMA_PENDING` | Child has planned schema but no verified UID |
| `DEDICATED_ATTESTATION_PENDING` | Child has planned attestation but no verified UID |
| `DEDICATED_ONCHAIN_VERIFIED` | Child has its own Observer-A-verified EAS UID |
| `REVOKED_VISIBLE` | Child or parent was revoked, and the revocation remains visible |

## Truth Boundary

A Family Node must expose:

- parent UID, if any
- parent revocation state, if known
- children list
- child dedicated UID, if any
- non-claims
- current classification

## Non-Claims

A Family Node does not imply:

- every child is onchain
- every child is Meta certified
- every child has a resolver contract
- parent revocability disappears

## Doctrine

The joke can fly. The receipt must land.

The family can grow. The lineage must stay readable.
