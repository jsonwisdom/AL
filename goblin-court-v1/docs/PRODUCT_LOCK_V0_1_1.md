# PRODUCT_LOCK_V0_1_1

**Status:** SIGNED  
**Builder Code:** `bc_j1200j64`  
**Demo Case:** `MN-STEARNS-003`  
**Canonical Thread State:** signed in ChatGPT thread before repo promotion  
**Repo Path:** `/goblin-court-v1/docs/`

---

## 1. Product Definition

Goblin Court v1 is:

```text
Docket -> Receipt -> Replay -> Nutrition Score -> x402 Payment -> Prompt Pack Unit
```

The product does not sell legal conclusions, truth claims, or generated images.

The product sells seven lineage-bound transformations of a receipt.

---

## 2. Free Tier

Free users receive:

1. Receipt
2. Replay
3. One-line Goblin Verdict
4. Nutrition Score

Free tier stops before the Prompt Pack Unit.

---

## 3. Paid Tier

Paid users receive exactly one SKU:

```text
PROMPT_PACK_UNIT_V0_1
```

No subscriptions, no marketplace, no image rendering, no agent swarm, no PDF Empire, no Alabama, no federal expansion in v1.

---

## 4. Payment Boundary

**PAYMENT_BOUNDARY_V0_1:** SIGNED

```text
Trigger:
Valid x402 payment received

Builder Code:
bc_j1200j64

Input:
docket_id
receipt_id
nutrition_score
replay_url

Output:
PROMPT_PACK_UNIT_V0_1

Artifact Count:
Exactly 7

Delivery:
Single immutable bundle

Re-generation:
Allowed. Same inputs may regenerate outputs. Lineage must remain identical.

Refund Rule:
Prompt quality disputes do not automatically trigger refund. Receipt mismatch triggers refund.

Authority:
FALSE

Truth Claims:
PROHIBITED
```

---

## 5. Nutrition Score

**NUTRITION_SCORE_V0_1:** SIGNED

Deterministic. No LLM scoring.

Inputs:

- `filing_count`
- `continuance_count`
- `days_open`
- `fee_multiplier = final_amount / original_amount`
- `outcome_type`

Score is stored on the replay, computed at replay publish time, and treated as immutable for that replay.

Score bands:

```text
0-24     PERFECT_DOCKET
25-49    MILDLY_SILLY
50-74    BUREAUCRATICALLY_WEIRD
75-100   GOBLIN_FEAST
```

---

## 6. Canonical Demo

```text
Docket ID: MN-STEARNS-003
Title: The Parking Ticket That Lived for 3 Years
Score: 78
Band: GOBLIN_FEAST
Verdict: The original ticket was $35. The paperwork disagreed.
Receipt ID: r_mn_stearns_003_v1
Replay URL: https://goblin.court/replay/mn-stearns-003
```

This is the only seed built end-to-end in v1.

The other Tier 1 seeds remain frozen backlog:

- `MN-STEARNS-008` — Security Deposit Wars
- `MN-STEARNS-015` — The $600 Snowblower
- `MN-STEARNS-018` — HOA Paint Color Tribunal
- `MN-STEARNS-020` — The Perfect Docket

---

## 7. Forbidden in v1

The following are explicitly out of scope:

- Repo sprawl
- Generated images
- Legal conclusions
- Truth claims
- Subscriptions
- Marketplace
- Agent swarm
- Federal expansion
- Alabama expansion
- Bulk PDF Empire processing
- Additional seed cases before MN-STEARNS-003 works end-to-end

---

## 8. Core Principle

```text
Lineage is the product.
Prompts are the delivery mechanism.
Receipts outrank narrative.
```
