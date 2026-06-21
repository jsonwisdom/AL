# Witness Rotation Ceremony v0.1

## Goal

Create fresh production witness trust root for Treasury real-genesis capture.

## Steps

1. Confirm Treasury Verifier v0.2 sealed.
2. Confirm simulated genesis remains labeled.
3. Generate fresh Ed25519 witness keys.
4. Publish public keys only.
5. Store secret signing material outside git.
6. Populate `policy/witnesses/witnesses.yaml`.
7. Add all sim-era/staging keys to `revoked`.
8. Run witness policy verifier.
9. Commit policy, schema, and ceremony receipt.
10. Tag witness policy release.
11. Block live capture until witness policy passes.

## Acceptance

```text
TREASURY_VERIFIER_V0_2 = SEALED
WITNESS_POLICY_V0_1 = PASS
SIM_KEYS_REVOKED = TRUE
PROD_WITNESS_QUORUM = 2-of-N
NO_SECRET_SIGNING_MATERIAL_IN_GIT = TRUE
NO_FAKE_GREEN = ACTIVE
```
