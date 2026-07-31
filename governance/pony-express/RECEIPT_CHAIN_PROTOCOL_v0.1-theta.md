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

## 2. Receipt Anatomy

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

## 3. Hash Construction

1. Canonicalize the receipt object **excluding** the `receipt_hash` field itself (and any signature fields) using a deterministic JSON serialization (sorted keys, no insignificant whitespace).
2. Compute `SHA-256` over the UTF-8 bytes of the canonical form.
3. Store the lowercase hex digest in `receipt_hash`.
4. The next receipt in the same chain MUST set `previous_receipt_hash` to this value.

```text
receipt_hash = SHA256( canonical_json( receipt without receipt_hash ) )
```

A chain is valid only when every link satisfies:

```text
receipt[n].previous_receipt_hash == receipt[n-1].receipt_hash
```

(for n ≥ 1; the genesis receipt has `previous_receipt_hash: null`).

## 4. Namespaces

| Prefix | Use |
|--------|-----|
| `RECEIPT-PX-` | Pony Express transport events |
| `RECEIPT-CW-` | Civic War board-game events |
| `RECEIPT-MC-` | Moot-court session events |
| `RECEIPT-GV-` | Gate-validation / transition events |
| `RECEIPT-RC-` | Meta receipt-chain maintenance events |

## 5. Chain Rules

1. **Append-only** — Prior receipts are never rewritten. Corrections are new receipts that reference the earlier receipt_id.
2. **No silent reordering** — Sequence is determined solely by the hash links.
3. **Fail-closed on break** — A missing, mismatched, or cyclic hash link renders the entire downstream chain `INVALID` for advancement purposes.
4. **Genesis** — The first receipt of a new session or stage may have `previous_receipt_hash: null`. Subsequent receipts must link.
5. **Cross-namespace linking** — A receipt may reference a prior receipt from another namespace via `previous_receipt_hash` when a logical custody transfer occurs (e.g., gate validation following a moot session).
6. **Malicious fixture resistance** — Gate Stage-5 explicitly requires test receipts generated under injected malformed fixtures; the chain protocol itself must reject any receipt whose `authority` or `historical_truth_established` fields are not the constant `false`.

## 6. Minimum Chain Lengths (from Transition Matrix)

| Stage | Minimum receipts | Notes |
|-------|------------------|-------|
| STAGE-1 | 1 | Replication / fixture receipt |
| STAGE-2 | 3 | Claim-layer separation |
| STAGE-3 | 5 | Ingestion digests |
| STAGE-4 | 2 | Hash-chained precedent |
| STAGE-5 | 3 | Malicious-fixture test passes |
| STAGE-6 | Full chain 1–5 + self-exam log | Completeness required |

## 7. Verification Algorithm (Pseudocode)

```text
function verify_chain(receipts: ordered list) -> PASS | FAIL:
    if receipts is empty: return FAIL
    prev_hash = null
    for r in receipts:
        if r.authority != false: return FAIL
        if r.historical_truth_established != false: return FAIL
        if r.gate_1_status != "BLOCKED": return FAIL
        if r.previous_receipt_hash != prev_hash: return FAIL
        expected = SHA256(canonical_json_without_hash(r))
        if r.receipt_hash != expected: return FAIL
        prev_hash = r.receipt_hash
    return PASS
```

## 8. Integration

- Pony Express carries receipt packets; it does not validate their semantic content.
- Gate Validation Spec consumes receipt chains to decide PASS/FAIL for role transitions.
- Moot Court Framework emits `RECEIPT-MC-*` receipts for every session phase.
- No receipt type satisfies Gate 1 or populates the core historical docket.

## 9. Prohibited Behaviors

```text
REWRITE_PRIOR_RECEIPT              = PROHIBITED
BREAK_HASH_LINK_SILENTLY           = PROHIBITED
SET_AUTHORITY_TRUE                 = PROHIBITED
SET_HISTORICAL_TRUTH_TRUE          = PROHIBITED
BYPASS_GATE_1_VIA_RECEIPT          = PROHIBITED
SYNTHETIC_BYTE_CLAIM_IN_PAYLOAD    = PROHIBITED
```

## 10. Current State

```text
ARTIFACT                = RECEIPT_CHAIN_PROTOCOL_v0.1-theta
PARENT                  = TRANSITION_CONTROL_MATRIX_v0.1-theta
GATE_1                  = BLOCKED
AUTHORITY               = FALSE
CORE_DOCKET             = EMPTY
EXECUTION               = SIMULATION_ONLY
PROMOTION               = BLOCKED
```
