# Witness Key Rotation Policy v0.1

## Status

DRAFT_FOR_REVIEW

## Purpose

Establish the production witness trust root for Treasury live capture and real-genesis promotion.

This policy separates simulated/staging signatures from production witness authority.

## Doctrine

- NO_FAKE_GREEN remains active.
- Simulated keys may document staging history.
- Simulated keys must not authorize real genesis.
- Production witness keys must be fresh Ed25519 keys.
- Real promotion requires quorum.
- Revoked keys fail strict verification.
- Revoked simulated keys remain visible for audit history only.

## Witness Set

Production witness set must use Ed25519 public keys only.

Required witness fields:

- key_id
- algorithm
- public_key
- role
- active_from
- active_until
- status
- custody
- allowed_actions

## Quorum

Default quorum:

```text
2-of-N
```

Real Treasury genesis promotion requires at least two active production witness signatures.

Single-witness promotion is invalid.

## Revocation

All sim-era keys must be listed under `revoked`.

Revocation reason for simulated genesis keys:

```text
simulated_genesis
```

Revoked keys:

- fail strict verification
- fail audit verification for production promotion
- may remain visible as historical staging evidence

## Private Key Custody

Private witness material must not be committed to git.

Allowed storage patterns:

- hardware-backed signer
- offline signer
- age-encrypted local secret-store
- future HSM/KMS signer interface

The repository may contain signer interface stubs, public keys, revocation records, and signed receipts only.

## Promotion Boundary

A receipt may not promote from simulated genesis to real genesis unless:

1. receipt mode is REAL
2. source data is live-captured
3. witness bundle is loaded
4. all signing keys are active production keys
5. quorum is satisfied
6. no revoked/sim key appears in the signature set
7. verifier strict mode passes

## NO_FAKE_GREEN

If any required witness check fails, emit a failure receipt.

Do not fake success.
Do not silently downgrade to audit mode.
Do not treat simulated witness material as production authority.
