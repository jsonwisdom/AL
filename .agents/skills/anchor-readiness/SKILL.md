# Anchor Readiness Skill

## Purpose
Determine whether a replay artifact is ready for external anchoring.

## Use When
- Preparing Base/EAS anchoring.
- Evaluating whether a replay surface is constitutionally converged.
- Reviewing whether a release has sufficient receipts.

## Never Do
- Never anchor unresolved drift.
- Never anchor phantom infrastructure.
- Never treat missing witnesses as settled state.

## Required Inputs
- Replay receipts.
- Registry roots.
- Witness logs.
- CI status evidence.

## Allowed Outputs
- READY_FOR_ANCHOR
- WITNESS_PENDING
- DRIFT_UNRESOLVED
- CI_UNOBSERVED
- ANCHOR_BLOCKED

## Verification Commands
```bash
./verify.sh
./scripts/root_continuity_checkpoint.sh
python3 scripts/verify_root_continuity_receipt.py <receipt.json>
python3 scripts/verify_root_continuity_receipt.py --historical <receipt.json>
```

## Readiness Definition
`READY_FOR_ANCHOR` means replay evidence is sufficient for anchoring review. It does not mean the artifact is already anchored.

CI/log witness status must be inspected when anchoring claims depend on CI.

## Receipt Path
- `docs/forensic/`

## Failure Condition
Block anchoring if replay evidence is incomplete or contradictory.

## Constitutional Rule
Anchor only what independent witnesses can reproduce.
