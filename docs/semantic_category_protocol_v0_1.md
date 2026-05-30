# Semantic Category Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/semantic_category_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Meaning Label Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Semantic Category Protocol v0.1 defines how replay objects are categorized, re-categorized, and queried without affecting identity, lineage, replay truth, scope status, or authority.

Category is a semantic tag.

Identity is a permanent anchor.

Category change is not identity change.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "SEMANTIC_CATEGORY_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Identity:** what an object is as a permanent replay anchor.
- **Category:** what an object means in context as a mutable label.
- **Re-categorization:** logged change to category labels without changing object ID or replay truth.

---

## Category Schema

```yaml
semantic_category_v0_1:
  object_id: UUID
  current_categories:
    - category_label
  category_history:
    - category_event_id
  category_namespace: operator | witness | system | temporal
```

---

## Category Namespaces

| Namespace | Origin | Mutability |
|---|---|---|
| `operator` | Jay-defined during decision | Operator can change |
| `witness` | Proposed by witness receipt | Operator approval required |
| `system` | Assigned by protocol, such as ARCHIVED or ACTIVE | Protocol rules only |
| `temporal` | Snapshot-related marker | Read-only after capture |

---

## Category Evolution Rules

1. **Assignment:** an object can have multiple categories simultaneously.
2. **Re-categorization:** changes are logged with justification receipt reference.
3. **Removal:** category removed from `current_categories`, moved to history.
4. **Conflict:** contradictory categories are allowed; replay preserves both.

---

## Category History Event Schema

```yaml
category_event:
  timestamp: ISO_8601
  previous_categories:
    - category_label
  new_categories:
    - category_label
  operation: ADD | REMOVE | REPLACE
  justification_receipt_id: receipt_id_or_null
  witness_proposal_id: witness_proposal_id_or_null
```

---

## Query Surface

Jay-only, read-only query surface may:

- find all objects with category X at current state
- find all objects with category X at snapshot T1
- show category evolution for an object over time
- compare category assignments across branches for the same ID

The query surface must not:

- change identity
- mutate lineage
- alter replay truth
- grant authority
- change scope status
- auto-resolve category conflict

---

## Separation Rules

Category change does not:

- change object identity
- create a new branch
- alter replay truth
- grant authority to a witness
- change scope status

Category change does:

- log an event in category history
- feed Drift Meter as neutral unless contradiction policy says otherwise
- require justification receipt if Operator-initiated

---

## Integration

- Witnesses may propose category changes.
- Witness proposals are drift-neutral and require Operator approval.
- Operator-approved category changes require justification receipts.
- Temporal snapshots capture categories as they existed at capture time.
- Drift Meter tracks category divergence across branches as observation-only signal.
- Object Identity Protocol remains authoritative for ID continuity, not meaning.

---

## Status

```json
{
  "artifact": "SEMANTIC_CATEGORY_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
