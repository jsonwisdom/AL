# American History 3-D Navigation Schema v0.1

**Working title:** From Civil War to Civic War  
**Classification:** Draft historical navigation architecture  
**Authority:** false  
**Promotion:** blocked

## Purpose

Define a three-axis map for navigating American history while preserving source bytes, provenance, jurisdiction, and constitutional authority as separate layers.

## Coordinate System

```text
US3D://<TIME>/<GEOGRAPHY>/<AUTHORITY>/<OBJECT_CLASS>/<OBJECT_ID>@<VERSION>
```

### X — Time

```text
YYYY | YYYY-MM | YYYY-MM-DD | INTERVAL:<start>..<end> | UNKNOWN | DISPUTED
```

### Y — Geography

```text
US
US-FEDERAL
US-<STATE>
US-<STATE>-<COUNTY>
US-<STATE>-<COUNTY>-<MUNICIPALITY>
US-TERRITORY-<NAME>
```

Directional values:

```text
NORTHBOUND | SOUTHBOUND | EASTBOUND | WESTBOUND
INBOUND | OUTBOUND | CENTER_TO_EDGE | EDGE_TO_CENTER | CROSS_BORDER
```

### Z — Authority

```text
CONSTITUTIONAL_TEXT
AMENDMENT
FEDERAL_STATUTE
STATE_CONSTITUTION
STATE_STATUTE
EXECUTIVE_ACT
JUDICIAL_DECISION
ADMINISTRATIVE_RULE
MILITARY_ORDER
TREATY
ELECTION_RESULT
PUBLIC_PETITION
UNPROVEN_CLAIM
```

Authority state:

```text
CLAIMED | OBSERVED | CONTESTED | UPHELD | OVERRULED
REPEALED | EXPIRED | SUPERSEDED | UNPROVEN | NONE
```

## Depth Layers

```text
Z0 SOURCE_BYTES
Z1 DOCUMENT_IDENTITY
Z2 PROVENANCE_AND_CUSTODY
Z3 FORMAL_AUTHORITY_CLAIM
Z4 JURISDICTION
Z5 IMPLEMENTATION
Z6 EFFECT
Z7 LATER_REVIEW
Z8 INTERPRETATION
```

No node may move from source bytes directly to interpretation without declaring unresolved intermediate gates.

## Historical Spine

```text
FOUNDING_CONTEST        1763..1789
FEDERAL_FORMATION       1787..1803
EXPANSION_AND_REMOVAL   1803..1854
SECTIONAL_RUPTURE       1854..1861
CIVIL_WAR               1861..1865
RECONSTRUCTION          1865..1877
POST_RECONSTRUCTION     1877..1954
CIVIL_RIGHTS_REORDERING 1954..1968
DIGITAL_STATE           1990..present
CIVIC_WAR               conceptual comparison layer only
```

`CIVIC_WAR` is a descriptive comparison layer for conflicts involving legitimacy, records, representation, institutional trust, access, and competing public claims. It is not an official period label and does not imply armed conflict.

## Route Families

```text
ROUTE-US3D-UNION
ROUTE-US3D-LIBERTY
ROUTE-US3D-SOVEREIGNTY
ROUTE-US3D-PEOPLE
ROUTE-US3D-RECORD
ROUTE-US3D-AUTHORITY
```

## Edge Types

```text
AMENDS
REPEALS
SUPERSEDES
IMPLEMENTS
RESISTS
OVERRULES
AFFIRMS
CITES
COPIES_BYTES_FROM
DERIVES_FROM
CONFLICTS_WITH
DEPENDS_ON
LIMITS
TRANSFERS_CUSTODY
PRESERVES
INTERPRETS
```

Every edge must declare direction, evidence, and confidence.

```json
{
  "edge_id": "EDGE-...",
  "from": "US3D://...",
  "to": "US3D://...",
  "type": "CITES",
  "direction": "OUTBOUND",
  "evidence_refs": [],
  "authority": false,
  "confidence": "UNASSESSED"
}
```

## Byte Packet

```json
{
  "packet_version": "US3D-PACKET-v0.1",
  "object_id": "HIST-...",
  "source_uri": null,
  "captured_at": null,
  "media_type": null,
  "byte_size": null,
  "sha256": null,
  "merkle_root": null,
  "custody_before_capture": "UNPROVEN",
  "claimed_author": null,
  "claimed_authority": null,
  "coordinate": "US3D://...",
  "gate_status": {
    "integrity": "UNTESTED",
    "identity": "UNPROVEN",
    "authorship": "UNPROVEN",
    "authority": "UNPROVEN",
    "truth": "UNPROVEN"
  }
}
```

## Naming Conventions

```text
NODE-<ERA>-<JURISDICTION>-<CLASS>-<SEQUENCE>
EDGE-<FROM>-TO-<TO>-<RELATION>-<SEQUENCE>
ROUTE-US3D-<THEME>-v<MAJOR>.<MINOR>
CAPTURE-<OBJECT_ID>-<UTC_TIMESTAMP>-<HASH_PREFIX>
RECEIPT-US3D-<OBJECT_ID>-<GATE>-<SEQUENCE>
CLAIM-UNRESOLVED-<JURISDICTION>-<SEQUENCE>
```

Names locate records. They may not prejudge legality, guilt, validity, or historical meaning.

## Navigation Commands

```text
MOVE_TIME_FORWARD
MOVE_TIME_BACKWARD
MOVE_GEOGRAPHY
MOVE_AUTHORITY_UP
MOVE_AUTHORITY_DOWN
FOLLOW_EDGE
TRACE_LINEAGE
COMPARE_BYTES
OPEN_GATE
HALT_ON_UNRESOLVED
RETURN_TO_SOURCE
```

## Constitutional Bridge Questions

```text
WHO_CLAIMS_AUTHORITY
WHAT_SOURCE_IS_CITED
WHERE_JURISDICTION_BEGINS_AND_ENDS
HOW_RECORDS_ARE_CREATED
WHO_CONTROLS_CUSTODY
HOW_THE_RECORD_MAY_BE_CHALLENGED
WHAT_APPEAL_PATH_EXISTS
WHAT_EVIDENCE_CAN_REVERSE_THE_CLAIM
```

## Doctrine

```text
BYTE_EQUALITY = INTEGRITY_ONLY
INCLUSION_PROOF != AUTHORSHIP
ROUTE_EXISTENCE != AUTHORITY
DOCUMENT_EXISTENCE != TRUTH
INTERPRETATION != ADJUDICATION
```

## Fail-Closed Rules

```text
NO_SOURCE_BYTES       -> NO_INTEGRITY_PASS
NO_PROVENANCE         -> NO_AUTHORSHIP_PASS
NO_AUTHORITY_EVIDENCE -> NO_AUTHORITY_PASS
NO_EDGE_EVIDENCE      -> NO_PATH_COMPLETION
CONFLICTING_RECORDS   -> FORK_DO_NOT_COLLAPSE
MISSING_HISTORY       -> GAP_DO_NOT_INVENT
```

## State

```text
ARTIFACT                = AMERICAN_HISTORY_3D_NAVIGATION_SCHEMA_v0.1
HISTORICAL_VERIFICATION = NOT_PERFORMED
EXECUTION_AUTHORITY     = FALSE
AUTHORITY_EXPANSION     = FALSE
GATE_1                  = BYTE_CAPTURE_PAIR_REQUIRED
PROMOTION               = BLOCKED
INTERPRETATION          = LOCKED
```
