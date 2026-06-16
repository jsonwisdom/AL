# CIPHER_COURT_V2_LOG_ODDS_CALIBRATION

Status: `SPEC_READY`
Builds on: `docs/games/CIPHER_COURT_V1.md`
V1 commit: `22a0fb687d27750b91c34048901cfbee6a0989e1`
Doctrine: `Confidence is not verdict. Replay is authority.`

## Purpose

Cipher Court V2 keeps the V1 interface readable while replacing the internal additive confidence model with a log-odds evidence engine.

The player still sees a simple confidence meter. Under the hood, evidence is combined in a mathematically stricter way.

Design rule:

```text
UI_STAYS_SIMPLE
ENGINE_GETS_STRICTER
REPLAY_REMAINS_FINAL
```

## Why V2 Exists

V1 teaches the feeling of Bayesian updating.

V2 teaches calibration.

The player learns that:

- confidence can rise for valid reasons
- confidence can rise for misleading reasons
- multiple weak signals can compound
- one attractive false signal can be outweighed by replay failure
- replay is the only authority that can issue verdict

## Visible UI

The player still sees:

```text
INTERCEPT RECEIVED
Confidence: 42%

[ crib found ]
[ frequency match ]
[ second message pass ]
[ entropy anomaly ]

Verdict readiness: 80%
```

The formula is hidden during normal play.

## Internal Engine

V2 stores confidence as log-odds internally.

```text
odds = p / (1 - p)
log_odds = log(odds)
```

Evidence updates add or subtract log-likelihood weight.

```text
new_log_odds = prior_log_odds + evidence_weight
```

The UI converts back to visible confidence:

```text
p = 1 / (1 + exp(-log_odds))
```

## Event Weights

Initial V2 weights are tunable.

```json
{
  "engine": "LOG_ODDS_V1",
  "starting_confidence": 0.42,
  "verdict_readiness_threshold": 0.80,
  "events": [
    {
      "event": "KNOWN_CRIB_MATCH",
      "weight": 0.72,
      "visible_label": "crib found"
    },
    {
      "event": "FREQUENCY_PROFILE_MATCH",
      "weight": 0.44,
      "visible_label": "frequency match"
    },
    {
      "event": "SECOND_MESSAGE_REPLAY_PASS",
      "weight": 1.10,
      "visible_label": "second message pass"
    },
    {
      "event": "ENTROPY_NOISE_SPIKE",
      "weight": -0.68,
      "visible_label": "entropy anomaly"
    }
  ]
}
```

## Confidence Is Still Not Verdict

Even if the log-odds engine produces 97 percent confidence:

```text
CONFIDENCE = 97%
REPLAY_STATUS = FAIL
VERDICT = REJECT
```

No UI confidence state can override deterministic replay.

## Calibration Graph

After each mission, V2 shows a calibration graph.

Purpose:

- compare player confidence against replay outcomes
- expose overconfidence zones
- teach probabilistic humility

Example bins:

```json
{
  "calibration_bins": [
    { "range": "0-10", "attempts": 2, "replay_success_rate": 0.00 },
    { "range": "10-30", "attempts": 5, "replay_success_rate": 0.20 },
    { "range": "30-50", "attempts": 8, "replay_success_rate": 0.38 },
    { "range": "50-70", "attempts": 10, "replay_success_rate": 0.60 },
    { "range": "70-90", "attempts": 12, "replay_success_rate": 0.58 },
    { "range": "90-100", "attempts": 4, "replay_success_rate": 0.75 }
  ]
}
```

Teaching moment:

```text
Your confidence between 70-90% was overconfident.
Replay success rate: 58%.
```

## Audit Mode

Audit Mode unlocks after the player completes several missions.

Audit Mode may show:

- prior confidence
- evidence weights
- resulting log-odds
- final visible confidence
- replay outcome
- calibration bin

Audit Mode must remain optional. The main game should still teach by feel.

## Noise Agent V2

The Noise Agent adapts to player trust patterns.

It tracks which evidence types the player overweights:

```json
{
  "player_trust_profile": {
    "crib_bias": 0.82,
    "frequency_bias": 0.67,
    "replay_patience": 0.31,
    "entropy_sensitivity": 0.24
  }
}
```

Attack selection:

```text
IF crib_bias is high -> prefer FALSE_CRIB
IF frequency_bias is high -> prefer DISTRIBUTION_SPOOF
IF replay_patience is low -> prefer KEY_COLLISION_TRAP
IF entropy_sensitivity is low -> prefer ENTROPY_MASKING
```

## Additional V2 Attack: ENTROPY_MASKING

```json
{
  "attack": "ENTROPY_MASKING",
  "effect": "Hides disorder inside plausible structure",
  "teaches": "Low apparent randomness does not guarantee meaningful signal",
  "failure_mode": "Player trusts smoothness instead of replay"
}
```

## Mission Receipt

Every V2 mission produces a calibration-aware receipt.

```json
{
  "game": "CIPHER_COURT_V2",
  "engine": "LOG_ODDS_V1",
  "intercept_id": "INTERCEPT_042",
  "starting_confidence": 0.42,
  "final_confidence_before_replay": 0.97,
  "replay_status": "FAIL",
  "verdict": "REJECT",
  "reason": "KEY_COLLISION_TRAP_DETECTED",
  "calibration_bin": "90-100",
  "receipt_hash": null
}
```

Receipt hashing must remove or null self-reference before hashing.

## V2 Build Order

1. Keep V1 additive UI intact.
2. Add log-odds engine behind the same UI.
3. Add post-mission calibration graph.
4. Add Audit Mode.
5. Add adaptive Noise Agent.
6. Add calibration-aware receipts.

## Non-Negotiable Rule

```text
REPLAY_SUPREMACY = TRUE
```

No probability, confidence score, role consensus, or player intuition may override replay.

## Product Boundary

V2 must remain original and avoid protected fictional characters, trademarks, or franchise language in shipped materials.

Use original roles:

- Cipher Analyst
- Signal Auditor
- Replay Judge
- Noise Agent
