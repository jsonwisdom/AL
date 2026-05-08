# CIPHER_COURT_SCAM_SUSCEPTIBILITY_PREREGISTRATION_V1

Status: `PREREGISTRATION_SCAFFOLD`
Instrument:
- `schemas/cipher_court/telemetry_v1.schema.json`
- `docs/research/CIPHER_COURT_AGGREGATION_AND_PRIVACY_V1.md`
- `docs/research/CIPHER_COURT_PREREGISTRATION_V1.md`

## Proposed Title

Cipher Court as a Calibration Intervention for Scam and Phishing Susceptibility

## Core Research Question

```text
Does adaptive adversarial calibration training in Cipher Court reduce susceptibility to scam and phishing attempts?
```

## Rationale

Historical backtests validate the instrument against past intelligence failures.

Scam and phishing studies test prospective intervention: whether the instrument improves future decisions under adversarial evidence.

The study asks whether calibration training transfers from cryptographic gameplay to real-world social engineering resistance.

## Primary Hypothesis

Participants receiving adaptive Noise Agent training will show greater reduction in scam / phishing susceptibility from pre-test to post-test than participants receiving fixed-difficulty training.

## Secondary Hypotheses

- Adaptive training reduces overconfidence_gap faster than static training.
- Adaptive training increases second-message verification behavior.
- High crib_dependency predicts susceptibility to urgent-action phishing frames.
- High frequency_bias predicts susceptibility to familiar-brand spoofing.
- High collision_blindness predicts susceptibility to one-factor legitimacy cues.
- Improvement in Cipher Court calibration predicts improvement on scam susceptibility batteries.

## Study Design

```text
N = 200 participants
PRE_TEST = standardized scam / phishing susceptibility battery
INTERVENTION = 10 hours Cipher Court training
POST_TEST = standardized scam / phishing susceptibility battery
GROUPS = adaptive Noise Agent vs fixed-difficulty Noise Agent
```

## Conditions

### Control Condition

Fixed-difficulty Cipher Court missions with scripted Noise attacks.

### Treatment Condition

Adaptive Noise Agent missions selected from participant vulnerability profile.

## Primary Outcome

```text
Change in scam / phishing susceptibility score from pre-test to post-test.
```

## Secondary Outcomes

```text
Change in overconfidence_gap.
Change in second-message verification behavior.
Change in vulnerability_profile scores.
Change in calibration curve alignment.
Transfer correlation between Cipher Court calibration and scam battery performance.
```

## Exploratory Outcomes

```text
Which vulnerability profiles predict scam susceptibility?
Which Noise Agent attacks produce fastest recalibration?
Does one catastrophic high-confidence replay failure produce faster real-world caution than multiple moderate failures?
```

## Open Telemetry Standard

All Cipher Court gameplay telemetry should conform to:

```text
schemas/cipher_court/telemetry_v1.schema.json
```

Minimum telemetry fields required:

- session_id
- mission_id
- engine
- player_actions
- noise_attacks
- replay_events
- vulnerability_profile
- receipt_hash

## Scam Battery Boundary

The protocol should use standardized or independently reviewable scam / phishing susceptibility batteries where available.

Candidate categories:

- phishing email recognition
- SMS urgent-action scams
- tech support scam scripts
- romance / trust-building scams
- familiar-brand spoofing
- authority impersonation lures

Outcome measures should separate:

```text
DETECTION_ACCURACY
FALSE_POSITIVE_RATE
RESPONSE_LATENCY
CONFIDENCE_IN_DECISION
CALIBRATION_ERROR
```

## Transfer Mapping

| Cipher Court Vulnerability | Real-World Scam Risk |
|---|---|
| crib_dependency | trusting a single familiar cue |
| frequency_bias | trusting familiar style or brand resemblance |
| collision_blindness | accepting one legitimacy signal without cross-checking |
| entropy_insensitivity | missing disorder hidden inside plausible language |
| replay_impatience | acting before verification |
| confidence_inflation | over-trusting one's own detection ability |

## Analysis Plan

### Primary Analysis

Compare pre/post scam susceptibility score change between treatment and control.

```text
adaptive_noise_delta vs fixed_noise_delta
```

### Secondary Analysis

Compare overconfidence_gap reduction between groups.

```text
mean_overconfidence_gap_pre - mean_overconfidence_gap_post
```

### Transfer Analysis

Test whether Cipher Court telemetry predicts scam battery improvement.

```text
vulnerability_profile_delta -> scam_susceptibility_delta
```

## Privacy and Ethics Boundary

Do not collect unnecessary personal identity.

Required:

```text
MINIMIZE_PERSONAL_DATA
ALLOW_OPT_OUT
PUBLISH_AGGREGATE_RESULTS
SEPARATE_GAME_TELEMETRY_FROM IDENTITY
```

Any real-world scam simulations must include debriefing and avoid financial harm.

## Replication Plan

The study should be runnable by independent labs using the open telemetry schema.

Target replication model:

```text
Lab A: general adult participants
Lab B: older adults / high-risk scam population
Lab C: professional analysts
Lab D: students or trainees
```

Pooled analysis should use the open aggregation format defined in:

```text
docs/research/CIPHER_COURT_AGGREGATION_AND_PRIVACY_V1.md
```

## Decision Rule

If adaptive Noise Agent training reduces scam susceptibility more than fixed training, Cipher Court qualifies as a prospective calibration intervention, not merely a historical reasoning game.

## Core Claim Under Test

```text
Personalized adversarial evidence can reduce real-world overconfidence under deception.
```

## Product Boundary

This preregistration does not claim clinical efficacy, intelligence-training efficacy, or fraud-prevention efficacy before empirical testing.

The protocol measures whether such transfer exists.
