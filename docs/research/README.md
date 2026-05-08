# Cipher Court Research Protocols

Cipher Court is not only a game.

It is an open measurement protocol for studying human calibration under adversarial evidence.

## Core Doctrine

```text
CONFIDENCE != VERDICT
REPLAY_PASS = VERDICT
REPLAY_REMAINS_SOVEREIGN
```

## Research Surfaces

### Open Telemetry Schema

```text
schemas/cipher_court/telemetry_v1.schema.json
```

Structured telemetry for:

- confidence updates
- replay outcomes
- adaptive adversarial attacks
- calibration error measurement
- vulnerability profiles

### Aggregation + Privacy Boundary

```text
docs/research/CIPHER_COURT_AGGREGATION_AND_PRIVACY_V1.md
```

Defines:

- population calibration curves
- replay-safe aggregation
- personal data minimization
- append-only telemetry handling

### Core Preregistration Scaffold

```text
docs/research/CIPHER_COURT_PREREGISTRATION_V1.md
```

Defines the base calibration intervention question.

### Scam Susceptibility Transfer Study

```text
docs/research/CIPHER_COURT_SCAM_SUSCEPTIBILITY_PREREGISTRATION_V1.md
```

Tests whether adaptive adversarial calibration training transfers to phishing and scam resistance.

### Research Partnership Prospectus

```text
docs/research/CIPHER_COURT_RESEARCH_PARTNERSHIP_PROSPECTUS_V1.md
```

Outreach-ready summary for labs, IRBs, and replication partners.

## Instrument Boundary

Cipher Court measures calibration behavior.

Replay determines truth.

```text
TELEMETRY_MUST_NOT_OVERRIDE_REPLAY
```

## Citation

If you use Cipher Court telemetry, schemas, or protocols in research, cite:

```text
CITATION.cff
```

Version anchor:

```text
d14ba36dd720c837e07f16c5d4460d5547109d3b
```

## Open Science Position

```text
REPLICATION_OVER_PROPRIETARY_ORACLE
```

The telemetry schema and aggregation rules are intentionally open so independent labs can replicate, challenge, extend, or pool results.

## Long-Term Goal

Create a replay-governed open standard for measuring how humans become confidently wrong under adversarial evidence — and whether adaptive calibration training can reduce that failure mode.
