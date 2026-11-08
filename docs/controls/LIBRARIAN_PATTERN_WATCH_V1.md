# Librarian Pattern Watch v1

STATUS = PROPOSED / PR-ONLY  
AUTHORITY = JASON

## Purpose

Mechanically distinguish routine ZTVS Librarian replay churn from a material change in the drift predicate, node outputs, receipt structure, or settlement gate.

This control does **not** infer truth from `audit_summary`, `GREEN`, a changing receipt filename, or `raw_sha256`.

## Locked boundaries

- `has_drift` is one comparison result, not an intrinsic property of a document.
- Historical results are immutable.
- New rules, validator code, input, or execution produce a new result object.
- `audit_summary.drift_detected` is runtime metadata and is not independent drift proof.
- `raw_sha256 = SHA256(target_id : github_sha : "raw")`; movement is not document-byte drift.
- Receipt generation is downstream of the production settlement guard, but the receipt's PASS/GREEN fields remain writer metadata.
- Unknown schema versions HOLD.
- Adding a supported version identifier without an explicit predicate is a material control change.

## Mechanical runners

1. **receipt-structure** — checks envelope, five-node shape, expected targets, and required per-node drift fields.
2. **validator-semantics** — checks the exact code contracts learned from `librarian-replay.yml`, `drift-schema-validator.cjs`, and `production-settlement-guard.cjs`.
3. **historical-delta** — compares consecutive Librarian receipts and the three control files against the parent commit.
4. **final-gate** — emits one classification:
   - `ROUTINE_LIBRARIAN_REPLAY`
   - `MATERIAL_PATTERN_DELTA`
   - `HOLD`

## Grok / agent bridge

Grok does not make the mechanical classification.

On `MATERIAL_PATTERN_DELTA`, the workflow emits `grok_handoff.json`. The handoff asks MASTER ROOM to route the smallest useful capability set and preserves:

`producer != verifier`  
`confidence != authority`  
`UNKNOWN != ALLOW`

Suggested existing capabilities are GitHubBot for repo facts, ProofPocket/ReceiptCheck for independent verification, LeahPrime for sequence/replay, MaryDeeBot for purpose changes, and HeiDeeBot for human flow only.

No agent may merge, publish, pay, delete, canonize, seal, or otherwise perform an irreversible/external action without Jason authorization.

## Non-goals

No default-branch write. No automatic merge. No workflow dispatch of other workflows. No chain write. No attempt to reinterpret historical `has_drift` under newer rules.
