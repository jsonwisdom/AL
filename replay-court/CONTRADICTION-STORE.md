# Replay Court Contradiction Store

The Contradiction Store preserves contradictions as first-class constitutional evidence.

A contradiction is not shame to erase.
A contradiction is the exhibit that makes repair legitimate.

## Purpose

```text
Preserve contradiction.
Prevent narrative laundering.
Make repair legitimacy testable.
```

The Repair Ledger records repairs.
The Contradiction Store preserves the contradictions those repairs depend on.

## Core Rule

```text
A repair is invalid unless the contradiction it repairs remains preserved and addressable.
```

## Contradiction Record Schema

Each contradiction record should include:

```text
contradiction_id:
created_at:
observed_by:
observed_where:
observed_text:
observed_text_hash:
context_snapshot:
context_hash:
contradiction_class:
why_it_matters:
why_it_matters_hash:
linked_repair_id:
linked_issue_ref:
status: preserved / superseded
```

## Hash Rules

```text
observed_text_hash = sha256(canonical observed_text)
context_hash = sha256(canonical context_snapshot)
why_it_matters_hash = sha256(canonical why_it_matters)
```

Do not hash vague summaries when exact text exists.
Hash the smallest observed contradictory surface.

## Status Rules

Allowed statuses:

```text
preserved
superseded
```

Forbidden statuses:

```text
resolved
deleted
hidden
obsolete
forgotten
```

A contradiction may be superseded by a better contradiction record.
It may not be erased by a repair.

## Common Contradiction Classes

```text
verifier_contract_contradiction
status_schema_contradiction
scoring_contradiction
progression_contradiction
settlement_contradiction
authority_boundary_contradiction
artifact_access_contradiction
self_audit_contradiction
```

## Record 001 — Issue #228 verifier contract contradiction

```text
contradiction_id: contradiction_001_issue_228_verifier_status
created_at: 2026-05-17T12:21:23Z
observed_by: Route B public artifact inspection
observed_where: artifacts/public/latest/verifier-current-tip.txt
observed_text: RECEIPT_CONFIRMED + status: failure
observed_text_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
context_snapshot: Level 2 verifier emitted confirmation token while reusing receipt outcome status field.
context_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
contradiction_class: verifier_contract_contradiction
why_it_matters: Verifier verdict and historical receipt outcome were collapsed into one ambiguous output surface.
why_it_matters_hash: sha256:UNCOMPUTED_MANUAL_ENTRY
linked_repair_id: repair_001_issue_228_verifier_contract
linked_issue_ref: https://github.com/jsonwisdom/AL/issues/228
status: preserved
```

## Validation Rule

A repair ledger entry is invalid if:

```text
- contradiction_ref does not point to a contradiction record
- contradiction_hash cannot be checked
- contradiction status is missing
- contradiction status implies deletion or erasure
- observed_text is replaced by only a summary when exact text exists
```

## Doctrine

```text
Contradictions are preserved, not laundered.
Repairs clarify; they do not erase.
Historical failure may remain true after replay repair succeeds.
```

## Invariant

```text
No preserved contradiction, no legitimate repair.
```
