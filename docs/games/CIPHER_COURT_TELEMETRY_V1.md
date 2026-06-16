# CIPHER_COURT_TELEMETRY_V1

Status: `SPEC_READY`
Builds on:
- `docs/games/CIPHER_COURT_V1.md`
- `docs/games/CIPHER_COURT_V2_LOG_ODDS_CALIBRATION.md`
- `docs/games/CIPHER_COURT_ADAPTIVE_NOISE_AGENT_V1.md`

Doctrine: `Telemetry turns gameplay into calibration science.`

## Purpose

Cipher Court telemetry captures structured calibration events so the game can measure whether personalized adversarial evidence improves epistemic accuracy.

Historical campaigns are content. Telemetry is the instrument.

Without telemetry, each player's calibration graph remains local. With telemetry, Cipher Court can study population-level overconfidence, evidence weighting, and recalibration velocity.

## Core Research Question

```text
Does personalized adversarial evidence produce faster recalibration than fixed-difficulty levels?
```

## Design Boundary

Telemetry must measure calibration without collecting unnecessary personal data.

Required principles:

```text
MINIMIZE_PERSONAL_DATA
HASH_OR_RANDOMIZE_SESSION_IDS
MEASURE_BEHAVIOR_NOT_IDENTITY
ALLOW_OPT_OUT
REPLAY_RECEIPTS_REMAIN_VERIFYABLE
```

## Telemetry Event Schema

```json
{
  "schema": "CIPHER_COURT_TELEMETRY_V1",
  "session_id": "random_or_hashed_session_id",
  "mission_id": "MISSION_001",
  "engine": "LOG_ODDS_V1",
  "timestamp_utc": "2026-05-08T00:00:00Z",
  "player_actions": [
    {
      "t": 0,
      "evidence_type": "CRIB",
      "event": "KNOWN_CRIB_MATCH",
      "confidence_pre": 0.42,
      "confidence_post": 0.67,
      "actual_evidence_strength": 0.11,
      "visible_confidence_delta": 0.25
    }
  ],
  "noise_attacks": [
    {
      "t": 0,
      "attack_type": "FALSE_CRIB",
      "target_bias": "crib_dependency",
      "player_response_confidence_delta": 0.25
    }
  ],
  "replay_events": [
    {
      "t": 7,
      "confidence_before": 0.92,
      "outcome": "REJECT",
      "calibration_error": 0.38,
      "reason": "KEY_COLLISION_TRAP_DETECTED"
    }
  ],
  "vulnerability_profile": {
    "crib_dependency": 0.73,
    "frequency_bias": 0.41,
    "collision_blindness": 0.28,
    "entropy_insensitivity": 0.19,
    "replay_impatience": 0.62,
    "confidence_inflation": 0.35
  },
  "receipt_hash": null
}
```

Receipt hashing must remove or null self-reference before hashing.

## Evidence Types

```json
{
  "evidence_types": [
    "CRIB",
    "DIST",
    "COLLISION",
    "ENTROPY",
    "SECOND_MESSAGE",
    "REPLAY"
  ]
}
```

## Replay Outcomes

```json
{
  "replay_outcomes": [
    "ADMIT",
    "REJECT",
    "HOLD_FOR_MORE_EVIDENCE",
    "ESCALATE_TO_REPLAY"
  ]
}
```

## Population Calibration Curves

Telemetry enables aggregation across players.

Core metric:

```text
confidence_bin -> replay_success_rate
```

Example bins:

```json
{
  "population_calibration_bins": [
    { "range": "0-10", "attempts": 0, "replay_success_rate": null },
    { "range": "10-30", "attempts": 0, "replay_success_rate": null },
    { "range": "30-50", "attempts": 0, "replay_success_rate": null },
    { "range": "50-70", "attempts": 0, "replay_success_rate": null },
    { "range": "70-90", "attempts": 0, "replay_success_rate": null },
    { "range": "90-100", "attempts": 0, "replay_success_rate": null }
  ]
}
```

Discovered pattern to test:

```text
Do players systematically overestimate replay success in the 70-95 percent confidence range?
```

## Noise Agent Efficacy Metrics

Telemetry should measure whether adversarial exposure reduces targeted bias.

Question examples:

```text
Does FALSE_CRIB reduce crib_dependency after three exposures?
Does DISTRIBUTION_SPOOF reduce frequency_bias?
Does KEY_COLLISION_TRAP increase second-message verification behavior?
```

Metric shape:

```json
{
  "attack_efficacy": {
    "attack_type": "FALSE_CRIB",
    "target_bias": "crib_dependency",
    "exposure_count": 3,
    "bias_before": 0.78,
    "bias_after": 0.52,
    "delta": -0.26
  }
}
```

## Recalibration Velocity

Measures how quickly confidence becomes better aligned with replay outcomes.

```json
{
  "recalibration_velocity": {
    "session_id": "random_or_hashed_session_id",
    "reject_events_before_improvement": 2,
    "mean_overconfidence_gap_before": 0.34,
    "mean_overconfidence_gap_after": 0.17,
    "velocity_score": 0.50
  }
}
```

Research questions:

```text
Does one catastrophic 97 percent failure recalibrate faster than three 75 percent failures?
How many REJECT events are required before a player starts waiting for second-message replay?
```

## Meta-Strategy Evolution

Track whether players develop reliable epistemic strategies.

Examples:

```json
{
  "strategy_markers": {
    "waits_for_second_message": true,
    "ignores_single_crib_without_replay": true,
    "checks_entropy_before_submit": true,
    "submits_above_threshold_without_replay": false
  }
}
```

Comparison:

```text
Do wait-for-second-message players outperform pattern-matchers?
```

## Study Design V1

### Control Group

Fixed-difficulty Noise Agent.

```text
Noise attacks are selected from static mission scripts.
```

### Treatment Group

Adaptive Noise Agent.

```text
Noise attacks are selected from player vulnerability profile.
```

### Primary Outcome

```text
Reduction in overconfidence_gap after N missions.
```

### Secondary Outcomes

```text
Increase in second-message verification behavior.
Reduction in crib_dependency.
Reduction in frequency_bias.
Improvement in calibration curve alignment.
```

### Minimum Result Shape

```json
{
  "study": "CIPHER_COURT_POPULATION_CALIBRATION_STUDY_V1",
  "groups": {
    "control_fixed_noise": {
      "players": 0,
      "mean_overconfidence_gap_delta": null
    },
    "treatment_adaptive_noise": {
      "players": 0,
      "mean_overconfidence_gap_delta": null
    }
  },
  "primary_question": "Does personalized adversarial evidence produce faster recalibration than fixed-difficulty levels?"
}
```

## Aggregation Pipeline V1

```text
client_event
↓
schema_validation
↓
personal_data_minimization
↓
receipt_hash
↓
append_only_event_log
↓
population_calibration_bins
↓
attack_efficacy_report
↓
recalibration_velocity_report
```

## Privacy Boundary

Do not collect:

- real name
- email
- wallet address unless explicitly opted into by the player
- precise location
- device identifiers that are not required for local session continuity

Allowed:

- random session id
- mission id
- action timestamps relative to mission start
- confidence values
- evidence event types
- replay outcomes
- bias scores
- attack types

## Receipt Boundary

Receipts should prove telemetry integrity without exposing unnecessary identity.

Recommended pattern:

```text
telemetry_event_json
↓
canonicalize
↓
set receipt_hash = null
↓
sha256
↓
store hash in local or optional public aggregate receipt
```

## Non-Negotiable Rule

```text
TELEMETRY_MUST_NOT_OVERRIDE_REPLAY
```

Telemetry studies player behavior. Replay decides verdict.

## Product Principle

Telemetry tells us whether the cognitive vaccine immunizes or merely leaves a scar.
