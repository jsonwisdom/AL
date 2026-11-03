# PONY EXPRESS v0.1

**Repository:** `jsonwisdom/AL`  
**Classification:** Governance transport protocol candidate  
**Status:** DRAFT / FAIL-CLOSED  
**Execution authority:** `false`  
**Promotion authority:** `false`

## 1. Purpose

Pony Express is a bounded transport layer for moving evidence packets, hashes, receipts, and verification requests between approved governance surfaces.

It transports claims and artifacts. It does not validate them merely by carrying them.

```text
TRANSPORT ≠ VERIFICATION
DELIVERY ≠ AUTHENTICATION
RECEIPT_OF_DELIVERY ≠ TRUTH
ROUTE_ACCESS ≠ GOVERNANCE_AUTHORITY
```

## 2. Constitutional Boundary

Pony Express may:

- package an artifact with declared metadata;
- record origin and destination surfaces;
- preserve byte hashes supplied by an operator or verifier;
- record custody transitions after ingestion;
- issue delivery and rejection receipts;
- replay the transport history.

Pony Express may not:

- invent missing bytes, timestamps, identities, or signatures;
- assert authorship from a hash;
- assert authority from repository access;
- treat transport custody as pre-acquisition custody;
- satisfy Gate 1 without the required byte-capture pair;
- promote a governance object;
- unlock interpretation layers.

## 3. Packet Model

Every packet MUST declare:

```json
{
  "packet_id": "PX-<date>-<sequence>",
  "protocol_version": "0.1",
  "source_surface": null,
  "destination_surface": null,
  "artifact_name": null,
  "artifact_sha256": null,
  "artifact_byte_size": null,
  "observed_at_utc": null,
  "custody_status": "UNPROVEN_BEFORE_INGESTION",
  "gate_1_status": "BYTE_CAPTURE_PAIR_REQUIRED",
  "authority": false,
  "promotion_eligible": false
}
```

Null fields are admissible only when the packet is explicitly classified `INCOMPLETE` and rejected from promotion.

## 4. Route Ledger

Each hop appends a route event:

```json
{
  "hop_index": 0,
  "from": "surface-a",
  "to": "surface-b",
  "event": "ACCEPTED | FORWARDED | REJECTED | DELIVERED",
  "observed_at_utc": null,
  "packet_sha256": null,
  "operator_or_agent": null,
  "authority": false
}
```

The route ledger is append-only. Corrections are new events; prior events are never silently rewritten.

## 5. Gate Behavior

### Gate PX-0 — Route Resolution

Confirms that source and destination surfaces exist and are addressable.

`PASS` does not create authority.

### Gate PX-1 — Packet Completeness

Requires all mandatory packet fields and a reproducible packet encoding.

### Gate PX-2 — Byte Material

For evidence workflows requiring Gate 1, requires the complete byte-capture pair and associated timestamps.

Current default:

```text
PX-2 = FAIL
REASON = BYTE_CAPTURE_PAIR_REQUIRED
```

### Gate PX-3 — Integrity Verification

Recomputes packet and artifact hashes.

A pass establishes byte equality only.

### Gate PX-4 — Destination Acceptance

The destination independently decides whether to accept, quarantine, or reject the packet.

Delivery cannot force acceptance.

### Gate PX-5 — Promotion Eligibility

Pony Express never grants promotion. It may only carry an independently issued promotion decision.

```text
PROMOTION_AUTHORITY = EXTERNAL_AND_EXPLICIT
```

## 6. Receipt Types

- `DISPATCH_RECEIPT` — packet entered the route.
- `HOP_RECEIPT` — packet crossed one declared boundary.
- `DELIVERY_RECEIPT` — destination received the packet bytes.
- `REJECTION_RECEIPT` — destination rejected the packet with reason codes.
- `REPLAY_RECEIPT` — route history was deterministically replayed.

No receipt type establishes semantic truth, authorship, or legal authority by itself.

## 7. Minnesota Gate-1 Route

Initial candidate route:

```text
JOY / public-record target
        ↓ dispatch
COMPUTERWISDOM / byte capture and forensic comparison
        ↓ verified evidence packet
ReceiptOS or receipts-engine-v1 / receipt construction
        ↓ independently authorized governance route
AL / governance review
```

The Goblin Court interpretation layer remains locked until all required evidence and receipt gates pass.

## 8. Failure Modes

Pony Express MUST halt on:

- missing artifact bytes;
- hash mismatch;
- ambiguous destination;
- duplicate packet ID with different bytes;
- route event reordering;
- unsupported protocol version;
- attempted authority escalation;
- attempted promotion without an external authorization receipt.

## 9. Current State

```text
PROTOCOL              = PONY_EXPRESS_v0.1
STATE                 = DRAFT_FAIL_CLOSED
ROUTE_VERIFIED        = jsonwisdom/AL
GATE_1                = BYTE_CAPTURE_PAIR_REQUIRED
EXECUTION_AUTHORITY   = FALSE
AUTHORITY_EXPANSION   = FALSE
PROMOTION             = BLOCKED
INTERPRETATION        = LOCKED
```

## 10. Promotion Boundary

This document is a protocol candidate only. Its presence in a branch or pull request does not make it normative.

Normative activation requires an explicit review and promotion action separate from transport, hashing, delivery, or merge status.
