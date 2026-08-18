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
Valid contradictory receipts = `CONFLICT`.
A repository claim that fails replay is not silently preserved as chain truth.

## Permanent membranes

```text
TX_HASH != FACT
REPOSITORY_RECORD != CHAIN_TRUTH
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
- Exact head at correction registration: `f9d738fe37d5222bdfea62661ddb263ccfda77d0`
- Path: `citizen/blockchain-reverse-replay/CITIZEN_BLOCKCHAIN_REVERSE_REPLAY_LEDGER_V0_1.json`
- Seed: `CITIZEN_LEDGER_ITEM_001`
- Seed disposition: `CONFLICT`
- Negative replay receipt: `citizen/blockchain-reverse-replay/receipts/CITIZEN_LEDGER_ITEM_001_NEGATIVE_RPC_REPLAY_2026_08_18.json`
- Negative replay source: `USER_SUPPLIED_RPC_OUTPUT`
- Assistant external verification in correction turn: `ATTEMPTED_BUT_UNAVAILABLE_503`

ReceiptOS replay packet proposal:

- Repo: `jsonwisdom/receiptos-base`
- Draft PR: `#178`
- Branch: `agent/citizen-blockchain-replay-packet-v0-1`
- Exact head at correction registration: `005588bfdda0e56fcbecff1d094f51b61a04ccb8`
- Replay state: `CONFLICT_NEGATIVE_RPC_REPLAY_BOUND_EXTERNAL_CONFIRMATION_OPEN`

## Correction rule

```text
REPO_DECLARED_TX
+ NEGATIVE_RPC_REPLAY
= CONFLICT
```

This doctrine does **not** promote the result to `REJECT` until the negative chain result itself is independently bound by the replay rail or an authoritative explorer/RPC receipt. A corrected transaction hash or direct EAS attestation replay may also resolve the conflict.

## Executive-round gate

```text
ROUND_06_EXECUTIVE = READY_NOT_ROLLED
```

Round 06 may not advance merely because the schema, ledger, packet, CI, negative replay, or conflict state exists. Advance requires the named upstream evidence gate for the intended public-record event.

## Family boundary

No family names, relationships, private messages, family claims, custody material, or family-derived inference belong in this doctrine or its replay packets.

```text
FAMILY_LANE_IMPORTED = FALSE
AUTHORITY_CREATED = FALSE
```
