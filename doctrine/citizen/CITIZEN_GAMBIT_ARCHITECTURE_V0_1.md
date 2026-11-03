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

## Permanent membranes

```text
TX_HASH != FACT
REPOSITORY_RECORD != CHAIN_TRUTH
UID_STRING != ATTESTATION
NEGATIVE_CHAIN_REPLAY != MOTIVE_PROOF
REJECTED_BASE_SEPOLIA_EDGE != GLOBAL_ABSENCE
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

Primary ledger:

- Repo: `jsonwisdom/COMPUTERWISDOM`
- PR: `#493`
- Branch: `stack/dual-onion-azure-blockchain-audit-v0-1`
- Head: `a0d30740c4e8e8844ad5e2fa304bc668a7ae3407`
- Parent: `CITIZEN_LEDGER_ITEM_001 = CONFLICT_PRESERVED`
- Direct replay receipt: `citizen/blockchain-reverse-replay/receipts/CITIZEN_LEDGER_ITEM_001_EAS_UID_DIRECT_REPLAY_2026_08_18.json`
- Recovery record: `citizen/blockchain-reverse-replay/EAS_UID_RECOVERY_REPLAY_V0_1.json`

ReceiptOS:

- Repo: `jsonwisdom/receiptos-base`
- Draft PR: `#178`
- Branch: `agent/citizen-blockchain-replay-packet-v0-1`
- Head: `f4dee5ef75728732ce950824994ce3998f13284a`
- State: `PARENT_CONFLICT_PRESERVED_CHILD_EAS_REPLAY_REJECT`

## Direct Base Sepolia replay

Bound GitHub Actions replay:

- run: `32106944392`
- replay head: `141d4af42578d28586ddcadbf661efcc33c7c0c2`
- artifact: `9313480754`
- artifact SHA-256: `fdb0e6d5d28221ed21b2452b85803234b2e5507e8e39df30d879f4e75b96a8ff`

Observed:

```text
CHAIN_ID = 84532 / PASS
DECLARED_TX = NOT_FOUND
DECLARED_TX_RECEIPT = NOT_FOUND
EASSCAN_ATTESTATION = NOT_FOUND
EAS.getAttestation(DECLARED_UID) = ZERO ATTESTATION STRUCT
SchemaRegistry.getSchema(DECLARED_SCHEMA_UID) = ZERO SCHEMA RECORD
```

Current doctrine disposition:

```text
PARENT_HISTORICAL_STATE = CONFLICT_PRESERVED
DECLARED_TRANSACTION_EDGE = REJECT
DECLARED_TRANSACTION_RECEIPT_EDGE = REJECT
DECLARED_ONCHAIN_ATTESTATION_EDGE = REJECT
DECLARED_SCHEMA_REGISTRATION_EDGE = REJECT
OPTION_B_DIRECT_EAS_UID_REPLAY = COMPLETED_REJECT
RECOVERY_TERMINAL = REJECT_DECLARED_BASE_SEPOLIA_ANCHOR_OBJECTS
ROUND_06_EXECUTIVE = READY_NOT_ROLLED
AUTHORITY_CREATED = FALSE
```

The earlier HOLD and CONFLICT states remain part of the audit history. The child REJECT receipt does not erase them.

## Scope boundary

The replay rejects the repository-declared **Base Sepolia** anchor-object edges only. It does not establish motive, wrongdoing, who introduced the values, or absence on unrelated networks or private/offchain systems.

## Family boundary

No family names, relationships, private messages, custody material, or family-derived inference belong in this doctrine or its replay packets.

```text
FAMILY_LANE_IMPORTED = FALSE
AUTHORITY_CREATED = FALSE
```
