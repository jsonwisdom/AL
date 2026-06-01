# ALMS Base MCP send_calls Plugin Doctrine V0.1

Status: DRAFT_BINDING_NOTE
Authority: false
Mutation model: append-only
Membrane: HOLDS

## Purpose

This note binds `JOY_ALMS_BASE_MCP_PLUGIN_V0_1` to the existing AL Base MCP and ALMS memory surfaces. It is not a new doctrine island.

A Base MCP plugin is treated as an untrusted compiler from user intent to unsigned calldata. It does not own keys, does not broadcast transactions, does not adjudicate truth, and does not mutate prior receipts.

## Parent artifacts

This note must be read as a child of:

- `docs/BASE_MCP_ENGINE_AUDIT_V0_1.md`
- `docs/base-mcp-scaffold-audit-receipt.md`
- `schemas/base_mcp_witness.v0_1.schema.json`
- `schemas/mcp_engine_audit_receipt.v0_1.schema.json`
- `agents/base_mcp/schemas/action_receipt.schema.json`
- `agents/base_mcp/schemas/session_log.schema.json`
- `agents/base_mcp/schemas/permission_policy.schema.json`
- `agents/base_mcp/examples/intent_receipt.example.json`

## Role split

```json
{
  "plugin_role": "untrusted_compiler",
  "wallet_role": "approval_boundary",
  "base_mcp_role": "transport_runtime",
  "chain_role": "receipt_surface",
  "authority": false
}
```

## Allowed primitive mapping

- `read`: display receipt DAG state only
- `anchor`: prepare unsigned calldata for a claim anchor
- `dispute`: prepare unsigned calldata challenging an existing claim
- `witness`: prepare unsigned calldata attaching testimony to a claim or dispute

## Blocked transitions

The plugin must not:

- claim custody
- execute without wallet approval
- invent deployed contract addresses
- emit executable-looking placeholder calldata
- overwrite prior receipts
- declare truth, fraud, verification, falsity, or adjudication
- create a new witness taxonomy that bypasses `schemas/base_mcp_witness.v0_1.schema.json`

## Truth-status boundary

Allowed statuses for plugin-prepared records are limited to non-adjudicative states:

```json
[
  "CLAIM_ANCHORED_NOT_PROVEN",
  "DISPUTE_RECORDED_NOT_ADJUDICATED",
  "WITNESS_RECORDED_NOT_VERDICT"
]
```

No plugin response may use `VERIFIED`, `FALSE`, `FRAUD`, or `ADJUDICATED` unless a separate higher-authority resolution receipt exists and is explicitly referenced as a receipt, not as plugin authority.

## Final invariant

```json
{
  "mutation_model": "append_only",
  "plugin_role": "untrusted_compiler",
  "wallet_role": "approval_boundary",
  "base_mcp_role": "transport_runtime",
  "chain_role": "receipt_surface",
  "authority": false,
  "membrane": "HOLDS"
}
```
