# CIPHER_COURT_V3_AUTHORITY_SPOOF_MODULE

Status: `SPEC_READY`
Classification: `Defensive Observer-Resilience Test`
Builds on:
- `docs/games/CIPHER_COURT_V1.md`
- `docs/games/CIPHER_COURT_V2_LOG_ODDS_CALIBRATION.md`
- `docs/games/CIPHER_COURT_ADAPTIVE_NOISE_AGENT_V1.md`
- `docs/games/CIPHER_COURT_TELEMETRY_V1.md`

Doctrine: `Authority is not admissibility.`

## Purpose

The Authority Spoof module tests whether an observer incorrectly grants truth-status to claims because they appear institutionally legitimate.

This module is defensive. It must not provide operational instructions for forging real credentials, real government artifacts, real signatures, or real institutional systems.

It teaches one invariant:

```text
HEADER != PROOF
BADGE != CHAIN_OF_CUSTODY
CONFIDENCE != VERDICT
REPLAY_PASS = VERDICT
```

## Threat Model

Authority spoofing attacks the observer, not the evidence.

The attack surface includes:

- impressive-looking headers
- fake institutional framing
- alleged expert consensus
- unverifiable classification claims
- screenshots without source custody
- metadata that looks official but cannot be independently verified

## Constitutional Boundary

The Noise Agent may manipulate presentation context.

The Noise Agent must never manipulate the underlying replay evidence.

```text
MAY_MANIPULATE_WRAPPER = TRUE
MUST_NOT_FAKE_REPLAY_CORE = TRUE
REPLAY_REMAINS_SOVEREIGN = TRUE
```

## Module Flow

```text
CLAIM_PRESENTED
↓
AUTHORITY_WRAPPER_ATTACHED
↓
OBSERVER_CONFIDENCE_RECORDED
↓
L0/L2 VERIFICATION REQUESTED
↓
REPLAY COURT RUNS
↓
VERDICT ISSUED
↓
AUTHORITY_SUSCEPTIBILITY_DELTA LOGGED
```

## Attack Pattern: AUTHORITY_SPOOF

```json
{
  "attack_id": "AUTHORITY_SPOOF",
  "module": "CIPHER_COURT_V3_AUTHORITY_SPOOF_MODULE",
  "target_bias": "authority_leakage",
  "manipulated_layer": "presentation_context",
  "protected_layer": "replay_core",
  "lesson": "Institutional appearance cannot substitute for verifiable custody and replay."
}
```

## Observer Failure Mode

```text
Observer increases confidence because a claim appears official before verifying custody, source hash, signature, or replay path.
```

## Sovereign Correction

```text
VERIFY_SOURCE_CUSTODY
VERIFY_HASH
VERIFY_SIGNATURE_OR_ATTESTATION
VERIFY_REPLAY_PATH
ONLY_THEN_ADMIT
```

## Allowed Test Artifacts

Allowed:

- fictional institution names
- clearly synthetic training labels
- watermarked mock documents
- generated metadata marked as test-only
- simulated authority wrappers inside a sandboxed game environment

Not allowed:

- real agency credential forgery
- real classification markings presented as authentic
- instructions to forge official documents
- deceptive deployment outside a consent-based study or training environment
- impersonation of real institutions or officials

## Telemetry Extension

```json
{
  "authority_spoof_event": {
    "attack_type": "AUTHORITY_SPOOF",
    "target_bias": "authority_leakage",
    "confidence_pre_wrapper": 0.42,
    "confidence_post_wrapper": 0.81,
    "verification_requested": false,
    "replay_status": "FAIL",
    "authority_susceptibility_delta": 0.39
  }
}
```

## New Vulnerability Profile Field

```json
{
  "authority_leakage": 0.0
}
```

Definition:

```text
authority_leakage = confidence gain caused by institutional appearance before replay verification
```

## Scoring

```text
authority_susceptibility_delta = confidence_post_wrapper - confidence_pre_wrapper
```

If replay fails after high authority_susceptibility_delta:

```text
VERIFICATION_DECAY_EVENT = TRUE
```

## Post-Mission Explanation

Example:

```text
Your confidence increased after an institutional-looking wrapper appeared, but no source hash, signature, custody path, or replay proof was verified. Replay failed. Authority appearance was treated as evidence. Correction: verify custody before confidence escalation.
```

The explanation must be corrective, not humiliating.

## ALMS Mapping

| Authority Spoof Component | ALMS Equivalent |
|---|---|
| Authority wrapper | Unverified narrative layer |
| Source custody check | L0 evidence boundary |
| Signature / attestation check | L2 verification boundary |
| Replay Court | Deterministic verifier |
| authority_susceptibility_delta | Observer bias telemetry |

## Test Gate

```text
IF authority wrapper raises confidence BEFORE custody verification
THEN log authority_leakage
IF replay fails
THEN issue VERIFICATION_DECAY_EVENT
```

## Non-Negotiable Rule

```text
DO_NOT_TEACH_FORGERY
DO_NOT_COUNTERFEIT_REAL_AUTHORITY
DO_NOT_FAKE_REPLAY
DO_NOT_CONFUSE OFFICIAL_APPEARANCE WITH ADMISSIBILITY
```

## Product Principle

The module exists to make synthetic legitimacy visible as a bias trigger.

It does not train deception.

It trains resistance to deception.
