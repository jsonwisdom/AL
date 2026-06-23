# BUILD_003 — MN-STEARNS-003 Vertical Slice

**Status:** BUILD SCAFFOLD  
**Branch:** `goblin-court-v1-build-003`  
**Canonical Demo:** `MN-STEARNS-003`  
**Builder Code:** `bc_j1200j64`

---

## Purpose

This build creates the first end-to-end Goblin Court v1 vertical slice for the canonical demo case:

```text
Receipt -> Replay -> Nutrition Score -> x402 Payment Boundary -> Prompt Pack Unit
```

This build does not add DDL, migrations, database code, subscriptions, image rendering, marketplace behavior, agents, bulk PDF processing, or additional seed cases.

---

## Files

```text
goblin-court-v1/
  README_BUILD_003.md
  demo/
    mn-stearns-003.html
  fixtures/
    mn-stearns-003/
      receipt.json
      replay.json
      payment_boundary.json
      prompt_pack_unit.json
```

---

## Build Boundary

This is a static, fixture-backed vertical slice. It proves product shape and lineage before database work.

The payment boundary is represented as a signed contract fixture. Live x402 middleware is intentionally not added in this build.

---

## Valid Flow

1. Load `receipt.json`
2. Load `replay.json`
3. Confirm replay score: `78 / GOBLIN_FEAST`
4. Confirm `payment_boundary.json` requires valid x402 payment using builder code `bc_j1200j64`
5. Unlock `prompt_pack_unit.json` only after payment boundary satisfaction

---

## Non-Goals

- No DDL
- No migration
- No generated images
- No LLM score computation
- No new products
- No additional seeds
- No repo sprawl

---

## Core Invariant

```text
Lineage is the product.
Prompts are the delivery mechanism.
Receipts outrank narrative.
```
