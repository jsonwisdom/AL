# CIPHER_COURT_PREREGISTRATION_V1

Status: `PREREGISTRATION_SCAFFOLD`

## Proposed Title

Cipher Court: An Instrument for Measuring Human Calibration Under Adversarial Evidence

## Core Research Question

```text
Does personalized adversarial evidence produce faster recalibration than fixed-difficulty levels?
```

## Hypothesis

Players exposed to adaptive adversarial evidence will reduce overconfidence gaps faster than players exposed to static scripted adversarial evidence.

## Primary Outcome

```text
Reduction in mean_overconfidence_gap across N missions.
```

## Secondary Outcomes

- Increased second-message verification behavior.
- Reduced crib_dependency.
- Reduced frequency_bias.
- Improved calibration curve alignment.
- Faster replay patience acquisition.

## Study Groups

### Control

Static Noise Agent.

### Treatment

Adaptive Noise Agent.

## Instrument

Open telemetry schema:

`schemas/cipher_court/telemetry_v1.schema.json`

## Replay Boundary

Replay remains the final authority for mission outcomes.

```text
CONFIDENCE != VERDICT
REPLAY_PASS = VERDICT
```

## Ethics Boundary

The instrument is designed to measure calibration behavior while minimizing personal identity collection.

Required principles:

```text
MINIMIZE_PERSONAL_DATA
ALLOW_OPT_OUT
PUBLISH_AGGREGATE_RESULTS
```

## Intended Domains

- cryptography education
- intelligence analysis training
- medical calibration research
- judicial reasoning studies
- financial overconfidence studies
- adversarial decision training

## Open Standard Goal

The telemetry schema and aggregation process are intended to be openly inspectable and reproducible.

Goal:

```text
REPLICATION_OVER_PROPRIETARY_ORACLE
```
