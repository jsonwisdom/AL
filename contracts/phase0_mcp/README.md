# Phase 0 MCP Contract — Directory-First Architecture

This directory is the isolated contract-test scaffold for `jsonwisdom/AL#415`.

## Directory contract

```text
contracts/phase0_mcp/
├── README.md
├── manifest.json
├── fixtures/
│   ├── signed_mcp_receipt.valid.json
│   ├── signed_mcp_receipt.hash_mismatch.json
│   └── signed_mcp_receipt.unknown_field.json
├── schemas/
│   ├── signed_mcp_receipt_v0.1.schema.json
│   └── contract_test_receipt_v0.1.schema.json
├── src/
│   ├── canonicalize.py
│   ├── contract.py
│   └── receipt.py
└── tests/
    └── test_contract.py
```

The canonical Phase 0 execution-receipt schema remains repository-level at `schemas/phase0_execution_receipt_v0.1.schema.json`.

## Boundaries

- This scaffold does not execute tests as part of its creation.
- It does not depend on merging PR #414.
- The adapter revision is pinned as data and supplied to the harness explicitly.
- JSON Schema validates structure; Python validates cross-field semantics.
- Standard JSON Schema cannot compare arbitrary sibling values; requested/executed hash equality is therefore enforced by the semantic validator.
- `authority` is always `false`.
- A passing contract test proves compatibility only for pinned inputs and revisions.
- It creates no merge, deployment, or execution authority.

## Anomalies designed for

1. Requested and executed hashes differ without `mutation_source`.
2. Unknown fields appear and would otherwise be silently dropped.
3. Signature metadata is missing or malformed.
4. Completed executions lack an output hash.
5. Failed executions lack an error object.
6. Denied executions claim `authorization=ALLOWED`.
7. Contract receipt omits one of the six mandatory evidence fields.

## Intended command

```bash
python -m pytest contracts/phase0_mcp/tests -q
```

That command is declared only. It was not executed during consolidation.
