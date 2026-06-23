# PROMPT_PACK_SCHEMA_V0_1

**Status:** SIGNED  
**Product Lock:** `PRODUCT_LOCK_V0_1_1`  
**Payment Boundary:** `PAYMENT_BOUNDARY_V0_1`  
**Builder Code:** `bc_j1200j64`

---

## 1. Purpose

`PROMPT_PACK_UNIT_V0_1` defines the only paid SKU in Goblin Court v1.

It is not an image.  
It is not a legal conclusion.  
It is not a truth claim.  
It is a lineage-bound creative bundle generated from a receipt-backed replay.

---

## 2. Required Input

Every Prompt Pack Unit requires validated input:

```text
docket_id
receipt_id
nutrition_score
replay_url
```

Optional contextual inputs may include:

```text
title
one_line_verdict
jurisdiction
record_type
receipt_angle
risk_level
source_summary
```

---

## 3. Required Output

Every paid Prompt Pack Unit returns exactly seven artifacts:

1. Poster Prompt
2. Meme Prompt
3. Storyboard Prompt
4. Trading Card Prompt
5. Court Sketch Prompt
6. Tweet Thread
7. Headline Pack

No more, no less in v1.

---

## 4. Lineage Requirement

Every output must embed:

```text
docket_id
receipt_id
nutrition_score
replay_url
```

Lineage format:

- Artifacts 1-5: machine-readable footer preferred
- Artifacts 6-7: human-readable lineage acceptable

Example footer:

```text
LINEAGE: docket=MN-STEARNS-003 | receipt=r_mn_stearns_003_v1 | score=78 | replay=https://goblin.court/replay/mn-stearns-003
```

---

## 5. Payment Rule

The Prompt Pack Unit is released only after a valid x402 payment.

```text
builder_code = bc_j1200j64
```

Payment unlocks one immutable bundle.

Regeneration is allowed only when the same lineage values are preserved.

---

## 6. Prohibited Output

Prompt Packs must not contain:

- Statements that a person committed a crime unless an adjudicated public record supports it
- Legal advice
- Claims of official court authority
- Truth claims beyond receipt/source matching
- Instructions to harass, dox, threaten, or target private parties
- Sensitive personal information
- Image generation as a service in v1

---

## 7. Prompt Pack Object

Canonical object shape:

```json
{
  "schema": "PROMPT_PACK_UNIT_V0_1",
  "docket_id": "MN-STEARNS-003",
  "receipt_id": "r_mn_stearns_003_v1",
  "nutrition_score": 78,
  "nutrition_band": "GOBLIN_FEAST",
  "replay_url": "https://goblin.court/replay/mn-stearns-003",
  "builder_code": "bc_j1200j64",
  "authority": false,
  "truth_claims": "prohibited",
  "artifacts": {
    "poster_prompt": "...",
    "meme_prompt": "...",
    "storyboard_prompt": "...",
    "trading_card_prompt": "...",
    "court_sketch_prompt": "...",
    "tweet_thread": "...",
    "headline_pack": ["..."]
  }
}
```

---

## 8. Core Invariant

```text
If an artifact cannot trace back to docket_id, receipt_id, nutrition_score, and replay_url, it is not a valid paid artifact.
```
