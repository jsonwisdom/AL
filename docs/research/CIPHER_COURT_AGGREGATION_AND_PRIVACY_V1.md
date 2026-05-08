# CIPHER_COURT_AGGREGATION_AND_PRIVACY_V1

Status: `OPEN_STANDARD_DRAFT`
Related schema:
- `schemas/cipher_court/telemetry_v1.schema.json`

## Purpose

Define how Cipher Court telemetry can be aggregated into population calibration studies without exposing unnecessary personal identity.

Core doctrine:

```text
MEASURE_BEHAVIOR
NOT_IDENTITY
```

## Aggregation Pipeline

```text
client_event
↓
schema_validation
↓
personal_data_minimization
↓
canonicalization
↓
receipt_hash_generation
↓
append_only_event_log
↓
population_calibration_bins
↓
research_exports
```

## Required Privacy Rules

Do not require:

- real names
- email addresses
- government identifiers
- precise locations
- biometric identifiers
- stable cross-platform advertising identifiers

Recommended:

- random session ids
- rotating local identifiers
- optional institutional cohort tags
- relative timestamps instead of wall-clock activity traces where possible

## Calibration Bin Computation

Population calibration curve:

```text
confidence_bin -> replay_success_rate
```

Reference bins:

```text
0-10
10-30
30-50
50-70
70-90
90-100
```

## Example Aggregate Export

```json
{
  "study": "CIPHER_COURT_POPULATION_CALIBRATION_V1",
  "sample_size": 10000,
  "confidence_bins": [
    {
      "range": "70-90",
      "attempts": 2411,
      "replay_success_rate": 0.58,
      "mean_overconfidence_gap": 0.19
    }
  ]
}
```

## Threat Model

Potential risks:

- deanonymization through timestamp correlation
- replaying telemetry to fabricate studies
- gaming calibration curves through scripted play
- poisoning aggregate datasets

Mitigations:

```text
ROTATING_SESSION_IDS
APPEND_ONLY_RECEIPTS
OPTIONAL_SIGNATURES
OUTLIER_DETECTION
REPLAYABLE_AGGREGATION_PIPELINES
```

## Research Boundary

Telemetry studies calibration behavior.

Replay still determines truth.

```text
TELEMETRY_MUST_NOT_OVERRIDE_REPLAY
```
