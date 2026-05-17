# Witness Replay Skill

## Purpose
Run the public replay oath and report only observed witness evidence.

## Use When
- A user asks whether the replay membrane holds.
- A commit, branch, or pull request needs replay verification.
- A witness transcript needs to be classified as green, red, or unobserved.

## Never Do
- Never claim green without observed replay output.
- Never treat a UI badge alone as full evidentiary proof.
- Never promote a narrative claim above the registry root.
- Never invent missing workflow logs, witnesses, commits, or hashes.

## Required Inputs
- Repository state or commit reference.
- Expected registry roots.
- Replay output from host, chamber, or CI logs.

## Allowed Outputs
- REPLAY_CONFIRMED
- REPLAY_REJECTED
- WITNESS_UNOBSERVED
- REGISTRY_MISMATCH
- DRIFT_REQUIRES_FORENSIC_ENTRY

## Verification Commands
```bash
./verify.sh
./scripts/root_continuity_checkpoint.sh
python3 scripts/verify_root_continuity_receipt.py <receipt.json>
python3 scripts/verify_root_continuity_receipt.py --historical <receipt.json>
```

## Receipt Path
- `docs/forensic/`

## Failure Condition
Fail closed if witness output, root hash, or registry anchor is missing, stale, or contradictory.

## Constitutional Rule
No witness, no claim. No receipt, no ratification.
