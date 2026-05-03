# Meme Court x Zora Game

Status: DRAFT_CANON
Operator: Jay Wisdom
Primary identity: jaywisdom.base
Layers: Meme Court / Zora Factory / ALMS 5.0 / Wisdom Family Gaming

## Core thesis

Meme Court x Zora turns funny reviewed artifacts into collectible public proof cards.

Meme Court decides whether the joke is safe, sourced, and label-correct.
ALMS decides whether the receipt is real.
Zora distributes the artifact.

Funny is allowed. Fake verified is not.

---

## Game loop

```text
Case -> Verdict -> Receipt -> Zora Card -> Public Vote -> Legacy XP
```

Machine form:

```json
{
  "loop": [
    "meme_court_case",
    "privacy_screen",
    "receipt_screen",
    "court_verdict",
    "zora_drop_card",
    "public_reaction",
    "legacy_xp"
  ]
}
```

---

## Zora court card schema

```json
{
  "zora_card_id": "ZMC-0001",
  "case_id": "MC-0001",
  "artifact_id": "WFG-0001",
  "title": "Meme Court: How to Create Artifacts",
  "creator": "Jay Wisdom / Wisdom Family",
  "identity": "jaywisdom.base",
  "court_verdict": "NEEDS_RECEIPT | APPROVED_FOR_FUN | READY_FOR_ZORA | BLOCKED_FAKE_VERIFICATION",
  "alms_status": "UNSET | PASS | FAIL | INDETERMINATE | TAINTED",
  "receipt_path": "UNSET",
  "merkle_root": "UNSET",
  "chain_status": "UNMINTED | MINTED | CONFIRMED",
  "contract_address": "UNVERIFIED_IDENTIFIER",
  "caption": "Funny is allowed. Fake verified is not.",
  "next_action": "string"
}
```

---

## XP rules

```json
{
  "xp_rules": {
    "case_created": 10,
    "privacy_screen_passed": 10,
    "missing_receipt_caught": 25,
    "caption_fixed": 20,
    "receipt_attached": 50,
    "zora_ready": 100,
    "mint_confirmed": 150,
    "legacy_indexed": 200
  }
}
```

---

## Badges

```json
{
  "badges": {
    "Zora_Court_Clerk": "created first Zora Meme Court card",
    "Goblin_Gatekeeper": "blocked fake verification before mint",
    "Caption_Counsel": "made caption match receipt",
    "Mint_Ready_Judge": "approved artifact for Zora after receipt check",
    "Courtroom_Collector": "confirmed first Meme Court Zora mint",
    "Legacy_Minter": "indexed confirmed mint into Wisdom Family Legacy"
  }
}
```

---

## Mint rules

1. No card may say VERIFIED unless ALMS status is PASS.
2. No contract address may be claimed until chain confirms it.
3. Transaction hash is not a contract.
4. Receipt hash is not a deed.
5. UNVERIFIED_IDENTIFIER is required until chain proof exists.
6. INDETERMINATE cards may publish only as research-in-progress or needs-receipt.
7. Family 702 safety labels override Zora readiness.

---

## First playable card

```json
{
  "zora_card_id": "ZMC-0001",
  "case_id": "MC-0001",
  "artifact_id": "WFG-0001",
  "title": "Meme Court: How to Create Artifacts",
  "court_verdict": "NEEDS_RECEIPT",
  "alms_status": "UNSET",
  "chain_status": "UNMINTED",
  "contract_address": "UNVERIFIED_IDENTIFIER",
  "next_action": "create ZMC-0001 card JSON"
}
```

---

## Public caption

```text
Meme Court x Zora

Funny is allowed.
Fake verified is not.
Bring receipts or meet the goblin. 🧌⚖️🧾

jaywisdom.base
```

---

## Next build step

```json
{
  "next": "create alms/meme_court/zora/ZMC-0001.json",
  "then": "link ZMC-0001 to MC-0001",
  "then_after": "prepare first Zora-ready caption once receipt exists"
}
```
