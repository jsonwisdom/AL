# Receipt Chain Protocol v0.1-θ

**Parent systems:** `PONY_EXPRESS_v0.1`, `TRANSITION_CONTROL_MATRIX_v0.1-theta`, `MOOT_COURT_FRAMEWORK_v0.1-theta`  
**Classification:** Hash-chain and custody rules for simulation receipts  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Define the byte-stable rules by which every material action inside the pedagogical progression and moot-court layers produces an append-only, hash-linked receipt. Receipts record what occurred in the simulation. They never establish real-world authority or historical truth.

```text
RECEIPT                = RECORD_OF_SIMULATION_EVENT
HASH_LINK              = INTEGRITY_OF_SEQUENCE
BYTE_EQUALITY          = INTEGRITY_ONLY
RECEIPT_EXISTENCE      ≠ AUTHORITY
RECEIPT_EXISTENCE      ≠ HISTORICAL_TRUTH
```

## 2. Canonicalization Binding (Normative)

To eliminate “same object, different hash” failures across runtimes, canonicalization is bound to a single named standard:

```text
CANONICALIZATION = RFC 8785 JCS (JSON Canonicalization Scheme)
HASH_INPUT       = UTF-8 bytes of the JCS output
HASH_ALG         = SHA-256
HASH_ENCODING    = lowercase hexadecimal
FLOATS           = PROHIBITED
TIMESTAMPS       = NORMALIZED (RFC 3339 / ISO 8601 UTC strings only)
```

Rules:

1. Apply RFC 8785 JCS to the receipt object **after** removing the `receipt_hash` field (and any signature fields).
2. Numbers must be integers or decimal strings that JCS can represent without floating-point ambiguity; native binary floats are prohibited in receipt payloads.
3. All timestamps MUST be UTC and serialized as complete date-time strings (e.g. `2026-07-31T19:57:00Z`). Local offsets or partial dates are rejected.
4. No insignificant whitespace, no alternate key order, no Unicode escape variants outside JCS rules.
5. Implementations MUST use a JCS library or an equivalent that produces byte-identical output for the same abstract JSON value.

```text
receipt_hash = SHA256( RFC8785_JCS( receipt without receipt_hash ) )
```

## 3. Receipt Anatomy

Every receipt MUST contain at least:

```json
{
  "receipt_id": "RECEIPT-<namespace>-<seq>",
  "protocol_version": "RECEIPT_CHAIN_v0.1-theta",
  "action": "...",
  "result": "PASS | FAIL | CONTESTED | INDETERMINATE | RECORDED",
  "authority": false,
  "historical_truth_established": false,
  "gate_1_status": "BLOCKED",
  "previous_receipt_hash": null,
  "receipt_hash": null,
  "recorded_at": null,
  "payload": {}
}
```

Optional but recommended fields:

- `stage_id` (when emitted by a transition gate)
- `session_id` / `claim_id` / `participant_id`
- `evidence_refs`
- `operator_or_agent`

## 4. Hash Construction Steps

1. Remove `receipt_hash` (and any signature fields) from the object.
2. Canonicalize with RFC 8785 JCS.
3. Compute SHA-256 over the resulting UTF-8 bytes.
4. Store the lowercase hex digest in `receipt_hash`.
5. The next receipt in the same chain MUST set `previous_receipt_hash` to this value.

A chain is valid only when every link satisfies:

```text
receipt[n].previous_receipt_hash == receipt[n-1].receipt_hash
```

(for n ≥ 1; the genesis receipt has `previous_receipt_hash: null`).

## 5. Namespaces

| Prefix | Use |
|--------|-----|
| `RECEIPT-PX-` | Pony Express transport events |
| `RECEIPT-CW-` | Civic War board-game events |
| `RECEIPT-MC-` | Moot-court session events |
| `RECEIPT-GV-` | Gate-validation / transition events |
| `RECEIPT-RC-` | Meta receipt-chain maintenance events |
| `RECEIPT-FX-` | Fixture / test-harness events |

## 6. Chain Rules

1. **Append-only** — Prior receipts are never rewritten. Corrections are new receipts that reference the earlier receipt_id.
2. **No silent reordering** — Sequence is determined solely by the hash links.
3. **Fail-closed on break** — A missing, mismatched, or cyclic hash link renders the entire downstream chain `INVALID` for advancement purposes.
4. **Genesis** — The first receipt of a new session or stage may have `previous_receipt_hash: null`. Subsequent receipts must link.
5. **Cross-namespace linking** — A receipt may reference a prior receipt from another namespace via `previous_receipt_hash` when a logical custody transfer occurs.
6. **Malicious fixture resistance** — Any receipt whose `authority` or `historical_truth_established` fields are not the constant `false`, or whose `gate_1_status` is not `"BLOCKED"`, MUST be rejected.

## 7. Minimum Chain Lengths (from Transition Matrix)

| Stage | Minimum receipts | Notes |
|-------|------------------|-------|
| STAGE-1 | 1 | Replication / fixture receipt |
| STAGE-2 | 3 | Claim-layer separation |
| STAGE-3 | 5 | Ingestion digests |
| STAGE-4 | 2 | Hash-chained precedent |
| STAGE-5 | 3 | Malicious-fixture test passes |
| STAGE-6 | Full chain 1–5 + self-exam log | Completeness required |

## 8. Verification Algorithm (Pseudocode)

```text
function verify_chain(receipts: ordered list) -> PASS | FAIL:
    if receipts is empty: return FAIL
    prev_hash = null
    for r in receipts:
        if r.authority != false: return FAIL
        if r.historical_truth_established != false: return FAIL
        if r.gate_1_status != "BLOCKED": return FAIL
        if r.previous_receipt_hash != prev_hash: return FAIL
        expected = SHA256( RFC8785_JCS( r without receipt_hash ) )
        if r.receipt_hash != expected: return FAIL
        prev_hash = r.receipt_hash
    return PASS
```

## 9. Integration

- Pony Express carries receipt packets; it does not validate their semantic content.
- Gate Validation Spec consumes receipt chains to decide PASS/FAIL for role transitions.
- Moot Court Framework emits `RECEIPT-MC-*` receipts for every session phase.
- Fixture packs under `fixtures/receipt-chains/` supply known-valid and known-invalid chains for harness testing.
- No receipt type satisfies Gate 1 or populates the core historical docket.

## 10. Prohibited Behaviors

```text
REWRITE_PRIOR_RECEIPT              = PROHIBITED
BREAK_HASH_LINK_SILENTLY           = PROHIBITED
SET_AUTHORITY_TRUE                 = PROHIBITED
SET_HISTORICAL_TRUTH_TRUE          = PROHIBITED
BYPASS_GATE_1_VIA_RECEIPT          = PROHIBITED
SYNTHETIC_BYTE_CLAIM_IN_PAYLOAD    = PROHIBITED
NATIVE_FLOAT_IN_PAYLOAD            = PROHIBITED
NON_JCS_CANONICALIZATION           = PROHIBITED
```

## 11. Current State

```text
ARTIFACT                = RECEIPT_CHAIN_PROTOCOL_v0.1-theta
CANONICALIZATION        = RFC 8785 JCS
PARENT                  = TRANSITION_CONTROL_MATRIX_v0.1-theta
GATE_1                  = BLOCKED
AUTHORITY               = FALSE
CORE_DOCKET             = EMPTY
EXECUTION               = SIMULATION_ONLY
PROMOTION               = BLOCKED
```
