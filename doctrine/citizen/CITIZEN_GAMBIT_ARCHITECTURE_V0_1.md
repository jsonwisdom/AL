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
UID_STRING != ATTESTATION
SEARCH_ABSENCE != CHAIN_ABSENCE
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
- Exact head at strategy registration: `f37fc371c68bb61232e4fc6bb53d522f31632880`
- Path: `citizen/blockchain-reverse-replay/CITIZEN_BLOCKCHAIN_REVERSE_REPLAY_LEDGER_V0_1.json`
- Seed: `CITIZEN_LEDGER_ITEM_001`
- Seed disposition: `CONFLICT`
- Negative replay receipt: `citizen/blockchain-reverse-replay/receipts/CITIZEN_LEDGER_ITEM_001_NEGATIVE_RPC_REPLAY_2026_08_18.json`
- Recovery record: `citizen/blockchain-reverse-replay/EAS_UID_RECOVERY_REPLAY_V0_1.json`
- Negative replay source: `USER_SUPPLIED_RPC_OUTPUT`

ReceiptOS replay packet proposal:

- Repo: `jsonwisdom/receiptos-base`
- Draft PR: `#178`
- Branch: `agent/citizen-blockchain-replay-packet-v0-1`
- Exact head at strategy registration: `ea810688dca8ad8d82d30621a839ab29b6e254e2`
- Replay state: `CONFLICT_PRESERVED_EAS_UID_RECOVERY_OPEN`

## Strategy rule

```text
PRESERVE_CITIZEN_LEDGER_ITEM_001_CONFLICT = TRUE
OPTION_A_HASH_CORRECTION = BLOCKED_NO_CORRECTED_HASH
OPTION_B_DIRECT_EAS_UID_REPLAY = ACTIVE_RECOVERY_PATH
```

The failed transaction hash is historical evidence and must not be silently overwritten.

A replacement transaction hash is accepted only if it is returned by a bound EAS attestation object or independently replayed chain record.

The EAS UID path is a separate recovery lane. Its existence does not upgrade the parent conflict.

## Internal transition audit

Two COMPUTERWISDOM receipts expose a transition that itself requires replay:

```text
EAS_SCHEMA_AND_ATTESTATION_ENTRIES_001
= SCHEMA_AND_ENTRIES_PREPARED_NOT_REGISTERED_NOT_SUBMITTED

↓ later repository claim ↓

EAS_ATTESTATION_SUBMITTED_001
= EAS_ATTESTATION_SUBMITTED / base-sepolia
```

The later receipt asserts schema registration and attestation submission. That transition is not authority-validated merely because it is written in the repository.

```text
REPOSITORY_TRANSITION_CLAIM != CHAIN_TRANSITION_PROVEN
```

## Executive-round gate

```text
ROUND_06_EXECUTIVE = READY_NOT_ROLLED
```

Round 06 may not advance merely because the schema, ledger, packet, CI, negative replay, conflict state, or EAS recovery lane exists. Advance requires the named upstream evidence gate for the intended public-record event.

## Family boundary

No family names, relationships, private messages, family claims, custody material, or family-derived inference belong in this doctrine or its replay packets.

```text
FAMILY_LANE_IMPORTED = FALSE
AUTHORITY_CREATED = FALSE
```
