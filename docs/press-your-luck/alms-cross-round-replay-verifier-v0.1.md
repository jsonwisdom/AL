# ALMS Cross-Round Replay Verifier v0.1

**Identity Root:** jaywisdom.eth  
**Operator Alias:** jaywisdom.base.eth  
**Project:** PRESS YOUR LUCK WITH JAY  
**Status:** FROZEN — PUBLIC REPLAY BUTTON  
**Commit Anchor:** eaa83303d3002baea041d55b671f1c7862f5d19c (verifier script)

## Purpose

Deterministic, replay-safe evaluation of C1–C5 cross-round invariants using Git vectors. Observation layer only. Produces attested results for on-chain enforcement. No authority. No custody. No randomness.

## Constitutional Invariants

- NO_REPLAY = NO_EVALUATION
- SHA256_FOR_ALMS = TRUTH_LAYER (Git/JSON verifiable)
- KECCAK_BRIDGE_LABELED = ENFORCEMENT_LAYER (explicit for EAS/Solidity)
- NO_RECEIPT = NO_STRIKE
- OBSERVATION_BEFORE_AUTHORITY = DOCTRINE

## Hash Domain Rules

- `sha256_replay_hash`: primary for ALMS/Git replay.
- `keccak256_replay_hash`: bridge field for EAS/Solidity handoff.
- NO_AMBIGUOUS_HASH = NO_CANONICAL_DRIFT

## Inputs

- `vectors/cross_round_invariant_vectors_v0_1.json`
- OperatorHistory snapshot from prior EAS attestations or local replay state

## Outputs

- JSON evaluation result
- SHA-256 replay hash
- Violations array for C1–C5
- Attestable payload for EAS

## Evaluation Flow

1. Load vectors and history.
2. Run pure C1–C5 checks.
3. Compute SHA-256 of canonical replay result.
4. Emit deterministic result JSON.
5. Attest via EAS with labeled hashes.
6. CrossRoundInvariantEnforcer consumes attested data only.

## Next Integration

- Add `vectors/cross_round_invariant_vectors_v0_1.json`
- Patch verifier for `keccak256_replay_hash`
- EAS attestation of first cross-round result
- Update ReputationStateMachine / enforcer to read attested history

## Legal Guardrails

Experimental verification system. Outcomes replayable. No guarantees. Public ledger required.

```txt
NO_CROSS_ROUND_MEMORY = NO_OPERATOR_ACCOUNTABILITY
```
