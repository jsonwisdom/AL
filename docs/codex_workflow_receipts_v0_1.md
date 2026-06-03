# Codex Workflow Receipts v0.1

## Purpose

Define a minimal AL receipt pattern for AI-generated role workflows.

Codex can create role-specific workflows, hosted Sites, and annotation-driven artifact edits. AL records what happened, what evidence was used, what changed, and whether the result can be replayed.

Core thesis:

> Codex builds the workflow. Receipts prove what happened.

## Scope

This v0.1 spec covers:

- workflow creation receipts,
- artifact hash binding,
- evidence reference requirements,
- annotation mutation events,
- successor receipt linkage,
- refusal when evidence or replay steps are missing.

This spec does not claim OpenAI endorsement, Codex runtime access, or universal truth. Authority remains false.

## Required files

```text
schemas/codex_workflow_receipt.v0_1.schema.json
examples/codex-workflow/receipt-001.json
examples/codex-workflow/README.md
scripts/validate_codex_workflow_receipt.py
```

## Receipt lifecycle

```text
DRAFT
  -> VERIFIED
  -> SUPERSEDED

DRAFT
  -> REFUSED

VERIFIED
  -> STALE
```

## Core invariants

1. No workflow artifact is verified without an artifact hash.
2. No workflow artifact is verified without evidence references.
3. No annotation silently mutates the original artifact.
4. Every annotation mutation emits a successor receipt or remains DRAFT.
5. Missing evidence produces REFUSED, not a partial truth claim.
6. Authority remains false.

## Minimum validation rules

A validator must confirm:

- `receipt_type` equals `CODEX_WORKFLOW_RECEIPT_V0_1`.
- `authority` is false.
- `workflow.id` exists.
- `workflow.role` is known or `other`.
- `artifact.hash` uses `sha256:<64 hex>`.
- `evidence_refs` is non-empty for `VERIFIED` receipts.
- `replay_steps` is non-empty for `VERIFIED` receipts.
- annotation events, when present, include a target, instruction, predecessor artifact hash, and successor artifact hash.
- `SUPERSEDED` receipts include `successor_receipt_id`.
- `REFUSED` receipts include refusal reasons.

## Win condition

A local demo must produce:

```text
✅ Workflow receipt emitted.
✅ Annotation mutation produced successor receipt.
✅ Missing evidence workflow refused.
Authority: false.
```

## Status

```json
{
  "status": "SPEC_DRAFT_V0_1",
  "issue": 284,
  "implementation_verified": false,
  "authority": false
}
```
