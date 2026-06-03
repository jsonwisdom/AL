# Codex Workflow Receipts - Demo Artifacts (Issue #284)

**Purpose**: Demonstrate replayable workflow receipts for AI-generated workflows.

**Authority**: false.

## Demo Files

| File | Status | Description |
|------|--------|-------------|
| `receipt-001.json` | VERIFIED | Complete workflow with annotation event and successor receipt |
| `receipt-refused-001.json` | REFUSED | Workflow rejected due to missing evidence |

## Validator Commands

```bash
python3 scripts/validate_codex_workflow_receipt.py examples/codex-workflow/receipt-001.json

python3 scripts/validate_codex_workflow_receipt.py examples/codex-workflow/receipt-refused-001.json

python3 scripts/validate_codex_workflow_receipt.py examples/codex-workflow/*.json
```

## Expected Output

```text
✅ examples/codex-workflow/receipt-001.json valid
✅ examples/codex-workflow/receipt-refused-001.json valid
```

## Win Condition

- ✅ Workflow receipt emitted.
- ✅ Annotation mutation produced successor receipt.
- ✅ Missing evidence workflow refused.
- Authority: false.

## Validation Summary

The validator enforces:

1. `receipt_type` exactly `CODEX_WORKFLOW_RECEIPT_V0_1`
2. `authority` must be `false`
3. `status` one of: `DRAFT`, `VERIFIED`, `REFUSED`, `STALE`, `SUPERSEDED`
4. `artifact.hash` format: `sha256:<64 lowercase hex>`
5. `workflow` requires `id`, `role`, `description`
6. `artifact` requires `type`, `title`, `hash`, non-empty `locations`
7. `evidence_refs` entries require `type`, `description`, `ref`
8. `VERIFIED` requires non-empty `evidence_refs` + `replay_steps`
9. `REFUSED` requires non-empty `refusal_reasons`
10. `SUPERSEDED` requires `successor_receipt_id`
11. `annotation_events` require `target`, `instruction`, predecessor/successor hashes with sha256 format

No OpenAI endorsement is claimed. No runtime Codex integration is claimed.
