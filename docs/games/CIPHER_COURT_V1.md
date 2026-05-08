# CIPHER_COURT_V1

Status: `SPEC_READY`
Classification: `Playable Epistemology`
Doctrine: `Confidence is not verdict. Replay is authority.`

## Purpose

Cipher Court V1 is a cryptographic mathematics game that teaches evidential reasoning through encrypted transmissions.

The game does not teach math as worksheet solving. It teaches math as admissibility: claims must survive pattern detection, adversarial noise, deterministic replay, and independent verification.

Core doctrine:

```text
CONFIDENCE != VERDICT
REPLAY_PASS = VERDICT
```

## Design Lineage

Cipher Court draws from wartime cryptographic reasoning, early signal intelligence, statistical cryptanalysis, and replayable verification.

It is not a clone of any specific fictional franchise or classified system. It uses generic roles and original terminology.

## Core Loop

```text
INTERCEPT RECEIVED
↓
PLAYER PROPOSES HYPOTHESIS
↓
EVIDENCE UPDATES CONFIDENCE
↓
NOISE AGENT ATTACKS
↓
SUBMIT TO REPLAY COURT
↓
DETERMINISTIC VERIFICATION
↓
VERDICT RECEIPT
```

## Primary UI

The left side of the interface displays the confidence meter.

```text
INTERCEPT RECEIVED
Confidence: 42%

[ crib found ]              +18
[ frequency match ]         +11
[ second message pass ]     +24
[ entropy anomaly ]         -15

Verdict readiness: 80%
```

The right side displays the Noise Agent and active adversarial attacks.

The main action button:

```text
SUBMIT TO REPLAY COURT
```

## Bayesian Slider Engine

The player sees belief updating without needing to see formulas.

```json
{
  "confidence_start": 42,
  "events": [
    { "event": "KNOWN_CRIB_MATCH", "delta": 18 },
    { "event": "FREQUENCY_PROFILE_MATCH", "delta": 11 },
    { "event": "SECOND_MESSAGE_REPLAY_PASS", "delta": 24 },
    { "event": "ENTROPY_NOISE_SPIKE", "delta": -15 }
  ],
  "verdict_threshold": 80
}
```

### Rule

Confidence can unlock readiness, but it cannot issue verdict.

```text
CONFIDENCE >= 80 => READY_FOR_REPLAY
REPLAY_PASS => VERDICT_ACCEPTED
REPLAY_FAIL => VERDICT_REJECTED
```

## Noise Agent

The Noise Agent exists to teach failure modes. It is not merely an enemy. It represents the null hypothesis: this variation may be random, misleading, or non-generalizable.

### Attack 1: FALSE_CRIB

```json
{
  "attack": "FALSE_CRIB",
  "effect": "Injects plausible known plaintext candidate",
  "teaches": "A claim can raise confidence and still fail replay",
  "failure_mode": "Plausible phrase does not generalize across messages"
}
```

### Attack 2: DISTRIBUTION_SPOOF

```json
{
  "attack": "DISTRIBUTION_SPOOF",
  "effect": "Fakes English-like frequency distribution",
  "teaches": "Distribution resemblance is not deterministic proof",
  "failure_mode": "Histogram passes but modular consistency fails"
}
```

### Attack 3: KEY_COLLISION_TRAP

```json
{
  "attack": "KEY_COLLISION_TRAP",
  "effect": "Makes one key work for Message A but fail on Message B",
  "teaches": "Single-instance success is not replayable truth",
  "failure_mode": "Key fails multi-message verification"
}
```

## Replay Court Procedure

A decryption is not accepted until it passes deterministic verification.

```text
1. Capture proposed key or state.
2. Decode primary intercept.
3. Decode secondary challenge intercept.
4. Compare outputs against admissibility checks.
5. Generate verdict receipt.
```

## Verdict States

```json
{
  "verdict_states": [
    "ADMIT",
    "REJECT",
    "HOLD_FOR_MORE_EVIDENCE",
    "ESCALATE_TO_REPLAY"
  ]
}
```

## Receipt Shape

Every verdict produces a receipt.

```json
{
  "game": "CIPHER_COURT_V1",
  "intercept_id": "INTERCEPT_001",
  "confidence_before_replay": 97,
  "replay_status": "FAIL",
  "verdict": "REJECT",
  "reason": "KEY_COLLISION_TRAP_DETECTED",
  "receipt_hash": null
}
```

Receipt hashing must remove or null self-reference before hashing.

## Stealth Curriculum

| Game Action | Math Internalized | Doctrine Parallel |
|---|---|---|
| Drag crib into intercept | Known-plaintext attack | Admissible evidence |
| Toggle Noise and see histogram jump | Distribution vs uniform baseline | SIGNAL vs NOISE |
| Test key across two messages | Deterministic consistency | REPLAY rule |
| Watch confidence slider update | Prior / update / posterior intuition | Evidence changes belief |
| Fail at 97 percent confidence | Overconfidence calibration | Confidence is not verdict |

## Four-Player Roles

These roles are optional for multiplayer or classroom mode.

### Cipher Analyst

Finds candidate patterns, cribs, keys, and plausible decryptions.

### Signal Auditor

Challenges provenance, checks distribution claims, and flags weak assumptions.

### Replay Judge

Runs deterministic replay and issues the final verdict receipt.

### Noise Agent

Injects false cribs, distribution spoofing, and key-collision traps.

## ALMS Mapping

| Cipher Court | ALMS |
|---|---|
| Intercept | Input artifact |
| Crib | Candidate evidence |
| Confidence slider | Epistemic update |
| Noise Agent | Noise / null hypothesis |
| Replay Court | Deterministic verifier |
| Verdict receipt | ALMS receipt |

## V2 Direction: Log-Odds Engine

V1 uses discrete visible deltas to keep the player experience clean.

V2 may replace internal confidence math with log-odds while preserving the same UI.

Design rule:

```text
UI stays simple.
Bayesian engine gets stricter under the hood.
```

V2 should not expose formulas unless the player enters advanced mode.

## Product Boundary

Do not use protected fictional characters, trademarks, or franchise names in shipped game materials.

Use original role names and mechanics:

- Cipher Analyst
- Signal Auditor
- Replay Judge
- Noise Agent

The game may be inspired by investigative and cryptographic genres, but the shipped product must remain original.
