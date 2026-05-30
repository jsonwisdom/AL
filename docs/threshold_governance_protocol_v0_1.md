# Threshold Governance Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/threshold_governance_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Observation Reference Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Threshold Governance Protocol v0.1 defines how thresholds are created, versioned, inherited, conflicted, reviewed, and archived.

A threshold is a static reference boundary.

A threshold crossing is an observed event.

A threshold does not create action authority.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "THRESHOLD_GOVERNANCE_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Threshold:** configured reference boundary for a metric.
- **Threshold crossing:** observed measurement relative to a threshold.
- **Threshold level:** label such as WATCH, ALERT, or CRITICAL.
- **Threshold conflict:** multiple valid thresholds apply to same metric/context.
- **Authority:** false; thresholds never decide.

---

## Threshold Schema

```yaml
threshold_governance_v0_1:
  threshold_id: UUID
  metric_id: UUID
  version: semantic_version
  level: WATCH | ALERT | CRITICAL
  condition: gt | lt | eq | between
  value: threshold_value
  scope: global | lineage | branch | protocol | custom
  justification_receipt_id: receipt_id
  created_at_timestamp: ISO_8601
  status: ACTIVE | ARCHIVED | SUPERSEDED
  auto_action: NONE
```

---

## Rules

1. Thresholds create visibility only.
2. Thresholds do not create decisions.
3. Thresholds do not trigger automatic action.
4. Thresholds do not change legitimacy status.
5. Thresholds do not admit or reject artifacts.
6. Threshold crossings are observation events only.
7. Threshold conflicts preserve all valid thresholds until Operator review.
8. Threshold version changes require justification receipt.

---

## Inheritance

Thresholds may apply at different scopes:

- global
- lineage
- branch
- protocol
- custom

More specific thresholds may coexist with broader thresholds.

Coexistence is not contradiction unless values are declared mutually exclusive.

---

## Conflict Handling

When multiple thresholds apply:

```json
{
  "threshold_conflict": "OBSERVED",
  "resolution": "OPERATOR_REVIEW_REQUIRED",
  "auto_action": "NONE",
  "authority": false
}
```

Conflict does not invalidate either threshold.

Conflict does not choose a winner.

---

## Crossing Event Schema

```yaml
threshold_crossing_event:
  crossing_id: UUID
  threshold_id: UUID
  metric_id: UUID
  measurement_id: UUID
  timestamp: ISO_8601
  crossing_result: CROSSED | NOT_CROSSED | NOT_COMPARABLE
  level: WATCH | ALERT | CRITICAL
  auto_action: NONE
  authority: false
```

---

## Integration

- Measurement Protocol provides measured values.
- Forecast Protocol may reference thresholds as guidance only.
- Drift Meter displays threshold crossings as observation signals.
- Obligation and Capability Protocols remain separate.
- Legitimacy Protocol is not changed by threshold crossings.
- Operator Review Surface displays threshold history read-only.

---

## Status

```json
{
  "artifact": "THRESHOLD_GOVERNANCE_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
