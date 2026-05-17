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

## Verification Command
```bash
./verify.sh
```

## Receipt Path
- `docs/forensic/`

## Failure Condition
Block anchoring if replay evidence is incomplete or contradictory.

## Constitutional Rule
Anchor only what independent witnesses can reproduce.
