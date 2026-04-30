# ALMS WebSocket Agent Receipt Layer

## Status

```json
{
  "module": "ALMS_WEBSOCKET_AGENT_RECEIPT_LAYER",
  "version": "v0.1",
  "status": "DESIGN_READY",
  "classification": "STATEFUL_AGENT_EXECUTION_RECEIPT_LAYER",
  "doctrine": "Proof > Narrative"
}
```

## Purpose

OpenAI-style WebSocket agent workflows improve execution speed by keeping a persistent session open and exchanging deltas instead of repeatedly resending full context.

ALMS adds the missing audit boundary: every inbound frame, outbound frame, tool call, and tool result must become a hash-chained receipt entry before it is trusted as state.

The speed layer may be volatile. The receipt layer must be replayable.

## Architecture Split

| Layer | Role | Trust Status |
|---|---|---|
| WebSocket session | Fast execution stream | Volatile |
| Delta log | Ordered raw event capture | Evidence candidate |
| Receipt chain | Canonical hash chain | Audit surface |
| Verifier | Replay and drift detection | Deterministic gate |

## Core Rule

```json
{
  "rule": "STATEFUL_DOES_NOT_MEAN_TRUSTED",
  "enforcement": [
    "capture raw frame before local processing",
    "assign monotonic sequence number",
    "canonicalize receipt entry",
    "hash each delta",
    "chain each entry to previous hash",
    "replay session from genesis",
    "reject mutation or sequence drift"
  ]
}
```

## Session Receipt Schema

A session receipt records a single WebSocket agent run.

```json
{
  "schema": "alms.ws_session_receipt.v0.1",
  "session_id": "sha256(canonical_session_open_event)",
  "opened_at": "ISO-8601 timestamp or externally supplied deterministic timestamp",
  "initial_state_hash": "sha256(canonical_initial_state)",
  "entries": [
    {
      "seq": 1,
      "type": "inbound_frame|outbound_frame|tool_call|tool_result|system_event",
      "payload_hash": "sha256(raw_payload_bytes)",
      "prev_hash": "initial_state_hash",
      "entry_hash": "sha256(canonical_entry_without_entry_hash)"
    }
  ],
  "final_state_hash": "last_entry_hash"
}
```

## Validity Conditions

A WebSocket session receipt is valid only if:

1. `seq` starts at `1` and increments by exactly one.
2. Every entry has a `prev_hash` equal to the previous accepted state hash.
3. Every `payload_hash` matches the raw payload bytes captured for that entry.
4. Every `entry_hash` recomputes from canonical JSON with sorted keys.
5. `final_state_hash` equals the final entry hash.
6. Replaying the ordered entries produces the same final hash.

## Failure Classes

```json
{
  "VALID": "all hashes, sequence numbers, and replay checks pass",
  "DRIFT": "same payload sequence but different recomputed hash",
  "BREAK": "missing, reordered, or mutated entry boundary",
  "INVALID": "unverifiable, malformed, or incomplete receipt"
}
```

## Placement

```txt
AL/
  docs/
    alms-websocket-agent-layer.md
  scripts/
    ws_session_receipt.sh
    verify_ws_session.sh
  _truth/
    websocket_sessions/
```

## Security Boundary

This module does not require:

- private keys
- wallet signing
- RPC calls
- contract writes
- token movement

It is a local deterministic receipt layer for high-speed agent sessions.

## Final Classification

```json
{
  "OpenAI_WebSockets": "AGENT_SPEED_LAYER",
  "ALMS_Addition": "AGENT_RECEIPT_LAYER",
  "combined_value": "continuous agents with replayable state",
  "status": "GOOD_NEXT_ANCHOR"
}
```
