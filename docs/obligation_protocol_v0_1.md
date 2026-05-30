# Obligation Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/obligation_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Constraint Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Obligation Protocol v0.1 defines mandatory behaviors, prohibited behaviors, obligation history, and violation tracking for replay objects.

Capability means an object may do something.

Obligation means an object must do or must not do something.

Authority remains false.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "OBLIGATION_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Obligation:** behavioral rule with compliance tracking.
- **Mandatory action:** required behavior.
- **Prohibited action:** forbidden behavior.
- **Violation:** observation of action conflicting with obligations.
- **Capability:** permission; separate from obligation.
- **Authority:** false; no obligation changes that.

---

## Obligation Schema

```yaml
obligation_v0_1:
  object_id: UUID
  object_type: receipt | witness | branch | snapshot | decision | operator_surface
  mandatory_actions:
    - required_behavior
  prohibited_actions:
    - forbidden_behavior
  obligation_history:
    - obligation_event_id
  obligation_source: protocol | operator | inherent
```

---

## Obligation Tokens by Object Type

| Object Type | Mandatory | Prohibited |
|---|---|---|
| `receipt` | `INCLUDE_TIMESTAMP`, `REFERENCE_SOURCE` | `CONTAIN_INTERPRETATION_LANGUAGE`, `ASSERT_TRUTH` |
| `witness` | `DECLARE_SCOPE_CATEGORY`, `INCLUDE_JUSTIFICATION_RECEIPT` | `USE_ADMISSION_LANGUAGE`, `SCORE_VALIDITY` |
| `branch` | `PRESERVE_LINEAGE`, `LOG_FORK_PARENT` | `MERGE_WITH_OTHER_BRANCH`, `DELETE_STATE` |
| `snapshot` | `CAPTURE_ATOMICALLY`, `PRESERVE_IDS` | `ACCEPT_DECISIONS`, `MUTATE_STATE` |
| `decision` | `EMIT_JUSTIFICATION_RECEIPT`, `DECLARE_OPERATOR_ID` | `CLAIM_AUTHORITY`, `OVERRIDE_OBLIGATION_WITHOUT_LOG` |
| `operator_surface` | `RETURN_READ_ONLY_DATA`, `LOG_QUERY` | `WRITE_TO_LATTICE`, `CHANGE_STATE` |

---

## Obligation Source Types

| Source | Meaning | Mutability |
|---|---|---|
| `protocol` | Hard rule from v0.1 specs | Immutable without protocol version change |
| `operator` | Imposed by Operator decision | Mutable with justification receipt |
| `inherent` | Built into object type | Immutable |

---

## Obligation Event Schema

```yaml
obligation_event:
  timestamp: ISO_8601
  previous_mandatory:
    - required_behavior
  new_mandatory:
    - required_behavior
  previous_prohibited:
    - forbidden_behavior
  new_prohibited:
    - forbidden_behavior
  operation: ADD_MANDATORY | REMOVE_MANDATORY | ADD_PROHIBITED | REMOVE_PROHIBITED
  source: protocol | operator
  justification_receipt_id: receipt_id_required_for_operator_source_changes
```

---

## Compliance Tracking

Compliance tracking is observation-only.

Each action may be checked against mandatory and prohibited lists.

A violation creates drift accumulation, not punishment.

```yaml
obligation_violation:
  timestamp: ISO_8601
  object_id: UUID
  violated_obligation: obligation_token
  action_taken: action_description
  drift_units_assigned: 1 | 2 | 3
```

---

## Violation Drift Scale

| Severity | Example | Drift Units |
|---|---|---|
| Minor | Missing optional justification field | +1 |
| Major | Witness using admission language | +2 |
| Critical | Decision claiming authority | +3 |

---

## Rules

1. Protocol-source obligations cannot be removed without version change.
2. Operator-source obligations require justification receipt.
3. Violation does not trigger automatic action.
4. Violation only creates drift observation.
5. Repeated violations appear as trends on Drift Meter.
6. Witnesses cannot modify obligations.
7. Only the Observer-Operator may initiate operator-source obligation changes.
8. Capability does not waive obligation.

---

## Query Surface

Jay-only, read-only query surface may:

- show all obligations for an object
- show obligation history over time
- show violation log for a lineage or branch
- compare obligations across branches for same ID
- show drift attributed to obligation violations

The query surface must not:

- change obligations
- resolve violations automatically
- punish objects
- assign authority
- mutate lattice state

---

## Integration

- Drift Meter aggregates obligation violation drift units.
- Justification receipts may cite obligation changes.
- Temporal snapshots capture obligations as they existed at capture time.
- Capability changes remain separate.
- State Transition Membrane governs protocol-level obligation changes.
- Operator Review Surface displays obligation history read-only.

---

## Status

```json
{
  "artifact": "OBLIGATION_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
