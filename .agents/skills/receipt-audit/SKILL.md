# Receipt Audit Skill

## Purpose
Validate that receipts, roots, and forensic entries align with executable repository state.

## Use When
- Reviewing commits, forensic ledgers, or replay transcripts.
- Checking whether documentation matches live code.
- Auditing registry anchors or replay receipts.

## Never Do
- Never accept deprecated roots through repetition.
- Never certify undocumented state.
- Never treat architectural intent as observed execution.

## Required Inputs
- Commit hashes.
- Registry roots.
- Witness logs.
- Forensic ledger entries.

## Allowed Outputs
- RECEIPT_VALID
- RECEIPT_STALE
- ROOT_SUPERSEDED
- NARRATIVE_STATE_GAP
- FORENSIC_ESCALATION_REQUIRED

## Verification Commands
```bash
git log --oneline -- docs/forensic/
cat receipts/index.json | python3 -m json.tool
python3 scripts/verify_root_continuity_receipt.py <receipt.json>
python3 scripts/verify_root_continuity_receipt.py --historical <receipt.json>
```

## Receipt Path
- `docs/forensic/`

## Failure Condition
Escalate immediately if repository state and narrative state diverge.

## Constitutional Rule
Execution outranks commentary.
