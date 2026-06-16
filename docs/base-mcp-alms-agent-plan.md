# Base MCP ALMS Agent Plan

Status: draft scaffold

## Purpose

This document defines the first planning surface for connecting Base MCP concepts to the ALMS receipt model.

The integration is documentation-only at this phase. It does not create executable agent behavior, signing behavior, spend behavior, or automated transaction flow.

## Identity Anchor

Primary human-readable anchor:

```text
jaywisdom.base.eth
```

This anchor identifies the operator context for future ALMS receipts. It is not itself a grant of operational authority.

## Architecture

```json
{
  "identity_anchor": "jaywisdom.base.eth",
  "base_mcp": "adapter_surface",
  "alms": "receipt_and_replay_layer",
  "agent": "bounded_executor"
}
```

## Phase 1 Boundary

Phase 1 is read-only and draft-only.

Allowed planning surfaces:

- document intended adapter boundary
- define schemas
- define example receipts
- define validation checks
- review permissions before any live connection

Not enabled in this phase:

- automated execution
- message signing
- fund movement
- live approvals
- credential storage
- background agents

## Required Receipt Rule

Every future proposed action must create an ALMS receipt before any external approval surface is presented to the operator.

## Review Requirements

Before any future live adapter is added, the repository must contain:

1. permission policy schema
2. action receipt schema
3. session log schema
4. example policy
5. example intent receipt
6. validation workflow

## Authority Statement

This file is a planning document only. It creates no wallet authority, no signing authority, no execution authority, and no merge authority.
