# Measurement Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/measurement_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Metric Observation Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Measurement Protocol v0.1 defines how metrics are created, versioned, measured, compared, thresholded, and archived.

A measurement is an observation.

A measurement is not a conclusion.

A measurement does not create authority, legitimacy, or admission.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "MEASUREMENT_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Measurement:** quantitative or categorical observation.
- **Metric:** named measurement definition.
- **Threshold:** observation boundary that creates flags only.
- **Comparison:** relationship between two measurements.
- **Conclusion:** not produced by this protocol.
- **Authority:** false; measurements never decide.

---

## Measurement Schema

```yaml
measurement_v0_1:
  metric_id: UUID
  metric_name: string
  version: semantic_version
  namespace: drift | coherence | obligation | capability | temporal | custom
  value_type: integer | float | categorical | count | ratio
  unit: optional_string
  measurement_timestamp: ISO_8601
  lineage_id: lineage_id
  branch_id: branch_id
  snapshot_id: snapshot_id_or_null
  value: measured_value
  threshold_config: threshold_id_or_null
```

---

## Metric Lifecycle

| Phase | Action | Requirement |
|---|---|---|
| Creation | Operator defines metric name, type, namespace | Operator decision + justification |
| Versioning | Increment version on definition change | Operator decision + justification |
| Measurement | System or Operator records value | Observation only |
| Comparison | Compare prior/current values or thresholds | Observation only |
| Thresholding | Check whether value exceeds threshold | Observation only |
| Archival | Deprecate metric but preserve history | Operator decision + justification |

---

## Measurement Namespaces and Examples

| Namespace | Example Metrics |
|---|---|
| `drift` | `entropy_delta`, `trend_slope`, `identity_fragmentation_count` |
| `coherence` | `contradiction_count`, `gap_count`, `overlap_ambiguity_count` |
| `obligation` | `violation_count_per_cycle`, `compliance_ratio` |
| `capability` | `assigned_count`, `suspended_count`, `grant_frequency` |
| `temporal` | `snapshot_interval_ms`, `branch_age`, `archive_depth` |
| `custom` | Operator-defined metrics such as `witness_receipt_volume` |

---

## Threshold Schema

```yaml
threshold_v0_1:
  threshold_id: UUID
  metric_id: UUID
  level: WATCH | ALERT | CRITICAL
  condition: gt | lt | eq | between
  value: threshold_value
  operator_notification: boolean
  auto_action: NONE
```

---

## Threshold Rules

- Thresholds trigger observation flags only.
- Thresholds never trigger automatic action.
- Threshold crossing is not an admission decision.
- Threshold crossing is not proof.
- Thresholds are versioned independently of metrics.
- Operator may modify thresholds without changing the metric definition.

---

## Comparison Schema

```yaml
measurement_comparison_v0_1:
  comparison_id: UUID
  metric_id: UUID
  baseline_measurement_id: measurement_id
  current_measurement_id: measurement_id
  delta: computed_difference
  ratio: optional_ratio
  observation: increased | decreased | stable
  no_interpretation: true
```

---

## Measurement History Queries

Jay-only, read-only query surface may:

- show all measurements for a metric over time
- compare measurements across branches
- show threshold crossing history
- export measurement set for analysis
- view metric version evolution

The query surface must not:

- produce conclusions
- assign authority
- trigger admission
- alter legitimacy
- mutate lattice state

---

## Archival Rules

- Deprecated metric moves to `ARCHIVED_MEASUREMENT_SCOPE`.
- Archived metric preserves all historical values.
- New metric version may reuse the metric name with a different ID.
- Archival requires justification receipt.

---

## Restrictions

Measurement does not:

- change legitimacy status
- grant or revoke capabilities
- modify obligations
- alter state legitimacy
- trigger admission
- prove correctness
- create authority

Measurement does:

- feed Drift Meter readings
- appear on Operator Review Surface
- get preserved in Temporal Snapshots
- support trend line calculation
- support Protocol Coherence gap detection

---

## Integration

- Drift Meter consumes measurement values as primary input.
- Thresholds map to Drift Meter levels: WATCH, ALERT, CRITICAL.
- Justification receipts may cite measurements.
- Temporal snapshots capture measurement state.
- Protocol Coherence checks may use measurements to detect metric gaps.

---

## Status

```json
{
  "artifact": "MEASUREMENT_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
