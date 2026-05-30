# Forecast Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/forecast_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Projection Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Forecast Protocol v0.1 defines how projections are created, tracked, compared, archived, and separated from measurements, legitimacy, admission, and authority.

A forecast is a projection.

A forecast is not an observation.

A forecast is not a decision.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "FORECAST_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Measurement:** observed value.
- **Forecast:** projected future or possible state based on stated inputs.
- **Confidence category:** qualitative label for forecast support level, not proof.
- **Forecast basis:** measurements, snapshots, assumptions, and lineage used to generate a projection.
- **Authority:** false; forecasts never decide.

---

## Forecast Schema

```yaml
forecast_v0_1:
  forecast_id: UUID
  metric_id: UUID_or_null
  forecast_name: string
  forecast_window: ISO_8601_duration_or_range
  basis_measurements:
    - measurement_id
  basis_snapshots:
    - snapshot_id
  assumptions:
    - assumption_marked_as_assumption
  projection_value: value_or_category
  confidence_category: LOW | MEDIUM | HIGH | UNRATED
  forecast_timestamp: ISO_8601
  lineage_id: lineage_id
  branch_id: branch_id
  authority: false
```

---

## Confidence Categories

| Category | Meaning |
|---|---|
| `UNRATED` | Forecast exists but confidence is not assessed. |
| `LOW` | Sparse basis, uncertain trend, or incomplete measurements. |
| `MEDIUM` | Some stable basis measurements and coherent trend. |
| `HIGH` | Multiple stable basis measurements and low contradiction, still not proof. |

Confidence is not correctness.

Confidence is not authority.

---

## Forecast Lifecycle

| Phase | Meaning |
|---|---|
| `PROPOSED` | Forecast created for review. |
| `ACTIVE` | Forecast is visible for guidance. |
| `COMPARE_READY` | Actual later measurement exists for comparison. |
| `COMPARED` | Forecast compared against later measurement. |
| `ARCHIVED` | Forecast preserved and no longer active. |
| `TAINTED` | Forecast basis found invalid or contaminated. |

---

## Forecast Comparison Schema

```yaml
forecast_comparison_v0_1:
  comparison_id: UUID
  forecast_id: UUID
  actual_measurement_id: measurement_id
  projected_value: value_or_category
  actual_value: measured_value
  delta: computed_difference_or_null
  comparison_result: OVER | UNDER | MATCH | NOT_COMPARABLE
  no_authority_effect: true
```

---

## Rules

1. Forecasts are guidance vectors only.
2. Forecasts never prove future state.
3. Forecasts never trigger automatic action.
4. Forecasts never change legitimacy status.
5. Forecasts never admit or reject artifacts.
6. Forecasts never grant or revoke capabilities.
7. Forecasts must cite basis measurements, snapshots, or explicit assumptions.
8. Forecast assumptions must be marked as assumptions.
9. Forecast comparison is diagnostic only.

---

## Separation Rules

Forecast does not:

- change measurement values
- change legitimacy status
- trigger admission
- create authority
- prove correctness
- resolve collisions
- mutate branch state

Forecast does:

- appear on Operator Review Surface
- feed Drift Meter as observation-only guidance
- support trend review
- support later comparison against measurements
- preserve projection lineage

---

## Archival Rules

- Forecast archival requires Operator decision and justification receipt.
- Archived forecast preserves basis, assumptions, projection, and comparison history.
- Archived forecasts may be inspected but not mutated.
- New forecast versions require new forecast IDs.

---

## Integration

- Measurement Protocol provides basis values.
- Temporal Snapshot Protocol provides point-in-time basis state.
- Drift Meter may display forecasts as observation-only trend guidance.
- Justification receipts may cite forecasts, but forecasts do not justify correctness.
- Protocol Coherence checks may flag forecasts that omit basis data.

---

## Status

```json
{
  "artifact": "FORECAST_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
