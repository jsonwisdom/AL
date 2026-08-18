# Citizen Gambit Architecture v0.1

**Registry:** `jsonwisdom/AL` doctrine pointer only  
**Authority created:** `FALSE`

## Placement

```text
PRIMARY_CITIZEN_AUDIT_HOME = jsonwisdom/COMPUTERWISDOM
RECEIPT_REPLAY_RAIL = jsonwisdom/receiptos-base
DOCTRINE_REGISTRY = jsonwisdom/AL
JOY_HEIDEE_FAMILY = SEALED_PRIVACY_SURFACE
```

```text
CITIZEN_INVESTIGATION != FAMILY_INVESTIGATION
AMERICAN_CITIZEN != AMERICAN_FAMILY
CITIZEN_RESEARCH = PUBLIC_RECORD_ONLY
JOY_FAMILY_PRIVACY = SEALED
```

This file is a routing/doctrine record. It does not duplicate the primary ledger and does not import family material.

## Blockchain reverse-replay doctrine

```text
CURRENT CLAIM
→ WALLET / CONTRACT STATE
→ TX HASH
→ RECEIPT + EVENT LOG
→ CONTRACT / FUNCTION
→ ASSET / COUNTERPARTY
→ AGREEMENT / INVOICE / ORDER IF CLAIMED
→ PAYMENT SOURCE IF CLAIMED
→ APPROPRIATION ONLY IF GOVERNMENT MONEY
→ STATUTE / AUTHORITY
→ ORIGINAL CLAIM
```

Missing required edge = `HOLD`.

## Permanent membranes

```text
TX_HASH != FACT
HASH != SEMANTIC_TRUTH
TOKEN_TRANSFER != INVOICE
ONCHAIN_EVENT != LEGAL_AUTHORITY
WALLET_ADDRESS != NATURAL_PERSON_IDENTITY
TRACEABLE_SEQUENCE != PROVEN_CAUSATION
DICE_SELECT_QUESTION = TRUE
DICE_DECIDE_TRUTH = FALSE
AUTHORITY_CREATED = FALSE
```

## Current pinned implementation

Primary ledger proposal:

- Repo: `jsonwisdom/COMPUTERWISDOM`
- PR: `#493`
- Branch: `stack/dual-onion-azure-blockchain-audit-v0-1`
- Exact head at doctrine registration: `389a148dbe7e86f97572fa1c2ddc2198c7acc59f`
- Path: `citizen/blockchain-reverse-replay/CITIZEN_BLOCKCHAIN_REVERSE_REPLAY_LEDGER_V0_1.json`
- Seed: `CITIZEN_LEDGER_ITEM_001`
- Seed disposition: `HOLD_INDEPENDENT_CHAIN_REPLAY`

ReceiptOS replay packet proposal:

- Repo: `jsonwisdom/receiptos-base`
- Draft PR: `#178`
- Branch: `agent/citizen-blockchain-replay-packet-v0-1`
- Exact head at doctrine registration: `6392539f8572e279d8465f54b5c00305e7866aec`
- Replay state: `HOLD_EXTERNAL_CHAIN_REPLAY_NOT_PERFORMED`

## Executive-round gate

```text
ROUND_06_EXECUTIVE = READY_NOT_ROLLED
```

Round 06 may not advance merely because the schema, ledger, packet, or CI exists. Advance requires the named upstream evidence gate for the intended public-record event.

## Family boundary

No family names, relationships, private messages, family claims, custody material, or family-derived inference belong in this doctrine or its replay packets.

```text
FAMILY_LANE_IMPORTED = FALSE
AUTHORITY_CREATED = FALSE
```
