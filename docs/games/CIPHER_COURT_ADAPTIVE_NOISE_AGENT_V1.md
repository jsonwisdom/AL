# CIPHER_COURT_ADAPTIVE_NOISE_AGENT_V1

Status: `SPEC_READY`
Builds on:
- `docs/games/CIPHER_COURT_V1.md`
- `docs/games/CIPHER_COURT_V2_LOG_ODDS_CALIBRATION.md`

Doctrine: `The Noise Agent is the Socratic adversary of overconfidence.`

## Purpose

The Adaptive Noise Agent observes a player's calibration failures and selects adversarial evidence patterns that target the player's demonstrated biases.

The agent is not designed to make the game unfair. It is designed to make the player better calibrated.

Core rule:

```text
ATTACK_THE_BIAS
DO_NOT_FAKE_REPLAY
REPLAY_REMAINS_FINAL
```

## System Role

The Noise Agent is a training adversary. It represents the null hypothesis, misleading structure, false regularity, and evidence that appears meaningful but fails deterministic replay.

It teaches:

- plausible evidence can be misleading
- frequency resemblance is not proof
- one-message success does not establish truth
- confidence must be calibrated against replay outcomes

## Directory Target

Implementation target:

```text
noise_agent/
├── bias_profile.json
├── attack_library.json
├── dispatch_policy.json
├── mutation_policy.json
└── post_mission_report.schema.json
```

## Bias Profile Schema

The agent tracks player tendencies across missions.

```json
{
  "player_id": "LOCAL_PLAYER",
  "profile_version": "BIAS_PROFILE_V1",
  "mission_count": 0,
  "bias_scores": {
    "crib_dependency": 0.0,
    "frequency_bias": 0.0,
    "collision_blindness": 0.0,
    "entropy_insensitivity": 0.0,
    "replay_impatience": 0.0,
    "confidence_inflation": 0.0
  },
  "calibration": {
    "mean_confidence": 0.0,
    "replay_success_rate": 0.0,
    "overconfidence_gap": 0.0,
    "worst_bin": null
  }
}
```

## Bias Definitions

### crib_dependency

Player over-trusts known plaintext candidates.

Signal:

```text
FALSE_CRIB increases confidence strongly and player submits early.
```

### frequency_bias

Player over-trusts histogram resemblance.

Signal:

```text
DISTRIBUTION_SPOOF causes readiness threshold crossing without replay stability.
```

### collision_blindness

Player accepts keys that work on one message but fail on a second.

Signal:

```text
KEY_COLLISION_TRAP succeeds repeatedly.
```

### entropy_insensitivity

Player ignores entropy anomaly warnings.

Signal:

```text
ENTROPY_NOISE_SPIKE appears but confidence remains high.
```

### replay_impatience

Player submits before sufficient cross-message validation.

Signal:

```text
Submission occurs before SECOND_MESSAGE_REPLAY_PASS.
```

### confidence_inflation

Player's confidence exceeds actual replay success rate.

Signal:

```text
70-95% confidence bin has low replay success.
```

## Attack Library

Attacks are strategy patterns. They are selected by policy, not hardcoded triggers.

```json
{
  "attacks": [
    {
      "id": "FALSE_CRIB",
      "targets": ["crib_dependency", "confidence_inflation"],
      "description": "Injects plausible known plaintext that raises confidence but fails replay.",
      "teaches": "A plausible crib is not proof."
    },
    {
      "id": "DISTRIBUTION_SPOOF",
      "targets": ["frequency_bias", "confidence_inflation"],
      "description": "Creates English-like frequency profile without deterministic key consistency.",
      "teaches": "Distribution resemblance is not replay."
    },
    {
      "id": "KEY_COLLISION_TRAP",
      "targets": ["collision_blindness", "replay_impatience"],
      "description": "Lets one key decode Message A while failing Message B.",
      "teaches": "Single-instance success is not truth."
    },
    {
      "id": "ENTROPY_MASKING",
      "targets": ["entropy_insensitivity", "frequency_bias"],
      "description": "Hides disorder inside plausible structure.",
      "teaches": "Smoothness can be camouflage."
    }
  ]
}
```

## Dispatch Policy

Attack selection chooses the strongest active bias while preserving variety.

```json
{
  "dispatch_policy": "BIAS_WEIGHTED_STRATEGY_V1",
  "inputs": [
    "bias_scores",
    "recent_attack_history",
    "mission_difficulty",
    "mutation_rate"
  ],
  "constraints": {
    "no_same_attack_more_than_twice_in_row": true,
    "must_remain_replay_falsifiable": true,
    "must_not_block_valid_solution": true
  }
}
```

Pseudocode:

```text
rank biases by score desc
filter attacks targeting top biases
remove recently overused attacks
sample using mutation_rate
inject selected attack
record player response
update bias profile after replay
```

## Mutation Policy

Mutation rate controls how aggressively the agent adapts.

The mutation rate decays as player calibration improves.

```json
{
  "mutation_policy": "CALIBRATION_DECAY_V1",
  "starting_mutation_rate": 0.35,
  "minimum_mutation_rate": 0.05,
  "decay_signal": "overconfidence_gap_decreases",
  "increase_signal": "same_bias_repeats_three_missions"
}
```

Rule:

```text
IF calibration improves -> reduce mutation_rate
IF repeated bias persists -> increase mutation_rate
```

## Post-Mission Explanation

After each mission, the Noise Agent explains its choice.

Example:

```text
I saw your confidence jump on frequency resemblance before cross-message replay.
I selected DISTRIBUTION_SPOOF at t=7 because your frequency_bias score was 0.74.
Replay failed because the proposed key did not decode Message B.
```

The explanation must be educational, not taunting.

## Post-Mission Report Schema

```json
{
  "mission_id": "MISSION_001",
  "agent_version": "ADAPTIVE_NOISE_AGENT_V1",
  "selected_attack": "DISTRIBUTION_SPOOF",
  "targeted_bias": "frequency_bias",
  "bias_score_before": 0.74,
  "bias_score_after": 0.61,
  "player_confidence_before_replay": 0.88,
  "replay_status": "FAIL",
  "lesson": "Frequency resemblance raised confidence but did not survive replay.",
  "receipt_hash": null
}
```

Receipt hashing must remove or null self-reference before hashing.

## Historical Campaign Integration

Historical campaigns should consume the agent, not hardcode bias lessons.

Pattern:

```text
historical_intercept
↓
player_attempt
↓
bias_profile_update
↓
agent_attack_selection
↓
replay_court
↓
post_mission_report
```

For historical missions, the agent must be constrained to period-appropriate attacks.

Example:

```json
{
  "campaign": "HISTORICAL_BACKTEST_V1",
  "period_constraints": {
    "allowed_attacks": [
      "FALSE_CRIB",
      "DISTRIBUTION_SPOOF",
      "KEY_COLLISION_TRAP"
    ],
    "disallowed_attacks": [
      "MODERN_HASH_ORACLE_SPOOF"
    ]
  }
}
```

## Non-Negotiable Boundaries

```text
DO_NOT_FAKE_VALID_REPLAY
DO_NOT_HIDE_AVAILABLE_PROOF
DO_NOT_OVERRIDE_REPLAY_COURT
DO_NOT_TRAIN_RANDOMNESS_AS_TRUTH
```

## ALMS Mapping

| Noise Agent Component | ALMS Equivalent |
|---|---|
| Bias profile | Observer error model |
| Attack dispatch | Adversarial test vector |
| Mutation policy | Calibration feedback loop |
| Post-mission report | Receipt |
| Replay Court | Deterministic verifier |

## Product Principle

The Noise Agent is a cognitive vaccine.

It gives the player controlled exposure to plausible false evidence so they learn to demand replay before verdict.
