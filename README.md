# Alabama Machine Speed

## CORECHAIN

**CORECHAIN = `contracts/` + `docs/` + `studio/`**

This repository is organized as a single chain of custody from code to
culture:

| Directory | Purpose |
|-----------|---------|
| `contracts/` | Protocol code, deployment scripts, legal compact — machine trust and execution |
| `docs/` | Cross-cutting legal, technical, and operational doctrine |
| `studio/` | Monetization, learning modules, publishing, visual command — human adoption layer |

**Build the protocol. Define the doctrine. Ship the studio.**

No drift between what the machine does, what the system claims, and what the
public sees.

---

## Overview

Alabama Machine Speed is a state-level truth arbitration system that turns
policy claims into verifiable, receipt-backed proof artifacts at machine speed.

Read the full State Chess Board explainer: [studio/STATE_CHESS_BOARD.md](studio/STATE_CHESS_BOARD.md)

---

## Machine Speed ALMS V2

Machine Speed ALMS converts fast-mutating public claims into deterministic,
replayable, tamper-evident receipts.

**Rule:** No claim graduates without a receipt.

### Core Loop

```text
capture_claim
  -> normalize_text (strict_v1)
  -> extract_entities
  -> verify_sources (with archiving)
  -> test_invariants (v1)
  -> merge_results
  -> emit_verdict
  -> hash_receipt
  -> append_ledger
```

### Guarantees

- Fully deterministic outputs
- Replayable from receipt alone
- Tamper-evident: a single-byte change breaks verification
- Explicit failure states with no silent degradation
- Machine-checkable and human-readable proof records

### Verdicts and Routing

| Verdict | Action |
|---------|--------|
| `VERIFIED` | Lock and anchor |
| `FALSE` | Lock and anchor |
| `MISLEADING` | Lock with context |
| `UNVERIFIED` | Queue retry with timeout |
| `NEEDS_MORE_EVIDENCE` | Human escalation |

### Failure States

```text
SOURCE_TIMEOUT
FORMAT_DRIFT
INVARIANT_CONFLICT
AMBIGUOUS_ENTITY
NON_REPRODUCIBLE
```

### Core Files

| Path | Purpose |
|------|---------|
| `contracts/receipt_schema.json` | Canonical receipt JSON Schema |
| `contracts/invariants/v1.json` | Versioned invariant contracts |
| `scripts/alms_normalize.sh` | Deterministic text normalization |
| `scripts/alms_verify.sh` | Full replay verifier |
| `_truth/ledger/alms_ledger.jsonl` | Append-only ledger in JSON Lines format |
| `_truth/receipts/` | Individual receipts |
| `docs/ALMS_OPERATOR_GUIDE.md` | Human escalation and operating procedures |

### Replay Rule

Every receipt is executable truth:

```json
{
  "receipt_id": "ALMS-MS-001",
  "input_hash": "sha256(...).....",
  "normalized_hash": "sha256(...).....",
  "transform_version": "normalize_strict_v1",
  "invariant_version": "invariants_v1",
  "verdict": "MISLEADING",
  "replay_cmd": "bash scripts/alms_verify.sh _truth/receipts/ALMS-MS-001.json",
  "valid_as_of": "2026-04-28T17:29:00Z"
}
```

If it cannot be replayed byte-for-byte, it is not a receipt.

### Demo Standard: Mutation Resistance

The public demo must survive adversarial edits:

1. Change one whitespace character -> hash mismatch
2. Edit one number or quantifier -> invariant failure
3. Swap entity resolution -> `AMBIGUOUS_ENTITY`
4. Modify archived source -> source drift detected

### Slogan

Machine Speed ALMS by Jay Wisdom.

Claims mutate fast. Verification must move faster.

Capture. Normalize. Test. Hash. Ledger.

No vibes. No silent edits. No authority theater.

**Truth that survives mutation.**

---

## Operator Guides

- [ALMS Operator Guide](docs/ALMS_OPERATOR_GUIDE.md) — receipts, Merkle roots, preflight audit, and verification flow.
