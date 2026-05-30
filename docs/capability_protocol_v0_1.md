# Capability Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/capability_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Action Permission Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Capability Protocol v0.1 defines what replay objects are allowed to do without granting authority, mutating identity, or altering replay truth.

Capability is actionable permission.

Authority remains false.

Identity remains unchanged by capability changes.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "CAPABILITY_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Capability:** what an object can do as a permission set.
- **Authority:** system-wide false constraint, not a capability.
- **Identity:** what an object is; unchanged by capability changes.
- **Capability change:** logged permission update that does not grant authority over truth or admission.

---

## Capability Schema

```yaml
capability_v0_1:
  object_id: UUID
  object_type: receipt | branch | witness | snapshot | decision | operator_surface
  current_capabilities:
    - capability_token
  capability_history:
    - capability_event_id
  capability_namespace: inherent | assigned | suspended
```

---

## Capability Tokens by Object Type

| Object Type | Capability Tokens |
|---|---|
| `receipt` | `BIND_TO_WITNESS`, `LOG_TO_HISTORY`, `TAINT` |
| `branch` | `RECEIVE_DECISIONS`, `HOLD_DRIFT_METER`, `FORK`, `ARCHIVE` |
| `witness` | `PROPOSE_RECEIPT`, `SUGGEST_CATEGORY`, `REQUEST_REVIEW` |
| `snapshot` | `CAPTURE_STATE`, `COMPARE_BRANCHES`, `LOAD_FOR_INSPECTION` |
| `decision` | `CHANGE_SCOPE_STATUS`, `EMIT_JUSTIFICATION`, `CREATE_BRANCH` |
| `operator_surface` | `QUERY_READ_ONLY`, `INSPECT_SNAPSHOT`, `VIEW_LINEAGE` |

---

## Capability Namespaces

| Namespace | Meaning | Mutability |
|---|---|---|
| `inherent` | Born with capability | Immutable |
| `assigned` | Granted by Operator | Operator can change |
| `suspended` | Temporarily inactive | Operator can restore |

---

## Capability Event Schema

```yaml
capability_event:
  timestamp: ISO_8601
  previous_capabilities:
    - capability_token
  new_capabilities:
    - capability_token
  operation: GRANT | REVOKE | SUSPEND | RESTORE
  justification_receipt_id: receipt_id
  operator_initiated: boolean
```

---

## Rules

1. Inherent capabilities cannot be revoked.
2. Assigned capabilities require Operator decision and justification receipt.
3. Suspension preserves capability set and toggles active/inactive status.
4. No capability grants authority.
5. Capability to change scope status does not imply correctness.
6. Witnesses cannot grant capabilities.
7. Only the Observer-Operator may change assigned or suspended capabilities.

---

## Capability History Queries

Jay-only, read-only queries may:

- show current capabilities for any object
- show capability changes over time
- compare capabilities across branches for the same ID
- find all suspended capabilities system-wide

Queries must not:

- grant capabilities
- revoke capabilities
- resolve branch conflicts
- alter identity
- assign authority

---

## Drift Meter Integration

```json
{
  "capability_divergence": {
    "drift_delta": 1,
    "meaning": "same_object_id_different_assigned_capabilities_across_branches"
  },
  "authority": false
}
```

Capability divergence is observation-only.

It is not proof of error or authority breach.

---

## Integration

- Justification receipts must reference capability grants, revocations, suspensions, or restorations.
- Temporal snapshots capture capabilities as they existed at capture time.
- Capability changes do not affect identity.
- Capability changes do not affect replay truth.
- Capability changes do not alter authority status.
- Capability changes do not automatically change membrane state.

---

## Status

```json
{
  "artifact": "CAPABILITY_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
