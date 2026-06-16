# FAF Epoch 03 Operational Runbook

Status: `ARCHITECTURE_COMPLETE_ANCHOR_LOCKED`

This runbook preserves the boundary between replay truth and chain permanence.

## Doctrine

- Architecture is complete and bounded.
- Authority is replay, not chain.
- Chain is pointer, not oracle.
- Gates remain locked until real-world digests, receipts, replay convergence, and dossier pinning exist.

## Current Posture

```text
CAPSULE=DECLARED
RUNTIME_IDENTITY=DECLARED
FIXTURE_IDENTITY=DECLARED
ALPHA_VERIFICATION=PENDING
REPLAY_REQUIREMENTS=DECLARED
CONVERGENCE_DOSSIER=PENDING
ANCHOR_PAYLOAD=TEMPLATE_READY
ANCHOR_GATE=LOCKED
```

## Required Sequence

1. Fill real `runtime.container_digest` in the Epoch 03 capsule.
2. Compute and fill fixture tree hashes:
   - `fixtures/faf/epoch_03`
   - `receipts/faf/epoch_02`
3. Recompute capsule canonical hash:

```bash
jq -cS '.receipt_hash=null' receipts/faf/epoch_03/parody_paradox_jay_faf_epoch_03_capsule.v1.json | sha256sum
```

4. Emit Alpha Verification Receipts until `ALPHA_VERIFIED`.
5. Run replay only through the lawful entrypoint:

```bash
npm run replay
```

6. Capture two human replay receipts with matching:
   - Merkle root
   - leaf count
   - tree layout hash
   - proof bundle hash
   - alpha verification reference
7. Finalize `epoch_03_convergence_summary.v1.json` from the pending dossier.
8. Hash and pin the finalized dossier:

```bash
sha256sum epoch_03_convergence_summary.v1.json
ipfs add --cid-version=1 --hash=sha2-256 epoch_03_convergence_summary.v1.json
```

9. Instantiate the bounded anchor payload with:
   - `dossier_sha256`
   - `dossier_ipfs_cid`
10. Only then may the anchor gate transition:

```text
ANCHOR_GATE=LOCKED -> ELIGIBLE_TO_OPEN
```

## Refusal Rules

- Missing runtime digest: no Alpha verification.
- Missing fixture hashes: no Alpha verification.
- Alpha drift: `ALMS-03 STATE_DRIFT`.
- Refusal receipt present: no Merkle root.
- Human receipt count below 2: no convergence.
- CI alone: witness only, never authority.
- Chain anchor before convergence: `ALMS-04 UNAUTHORIZED_ANCHOR`.

## Final Boundary

The chain records only a cryptographic pointer to the convergence dossier.

Replay verifies.

Chain remembers.

No ghost anchors.
