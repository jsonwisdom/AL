# BLUE BABY — CANONICAL RECEIPT

**Version:** Locked as of 2026-09-30
**Source State:** CHAT-SUPPLIED ONLY (prior to this artifact)
**Write Action (this creation):** TRUE (file creation only)

---

## 1. COINBASE CONNECTOR RECEIPT

```
ORDER_ID                 : af317ca0-99f6-4f43-b7f5-2d9c6db9aae1
TRADE_ID                 : 016809c9-abfc-49bf-9dbd-542715134f6e
PRODUCT_ID               : NVDA-USDC
SIDE                     : BUY
STATUS                   : FILLED
CREATED_TIME             : 2026-09-18T14:45:25.222900Z
TRADE_TIME               : 2026-09-18T14:45:25.555Z
AVERAGE_FILLED_PRICE     : 219.0155
FILLED_SIZE              : 0.02282
QUOTE_SIZE               : 5
TOTAL_FEES               : 0
COMPLETION_PERCENTAGE    : 100
ORDER_CONFIGURATION      : market_market_ioc
```

**Classification**
- COINBASE_RECORD            = PASS
- COINBASE_EXTERNAL_REPLAY   = HOLD
- Provenance                 = DIRECT_CONNECTOR_FIELD

**Missing for public replay**
- network / chain_id
- tx_hash
- contract_address
- block_number
- from / to addresses

---

## 2. BASE TRANSACTION (SUPPLIED)

```
TX_HASH                  : 0xcf5ce6439f37e672419f28783245e63f36ac061ef1eba7950f5567d57c9a7995
NETWORK                  : Base
CHAIN_ID                 : 8453
BLOCK_NUMBER             : 51921275
TIMESTAMP                : 2026-09-28 21:44:57 UTC
STATUS                   : Success
METHOD                   : transfer(address,uint256)
FROM                     : 0xC345B26094c63C69222Ee775189a3d3eaead5a84
TO (contract)            : 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
RECIPIENT                : 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
AMOUNT                   : 464606.558943981725590445
OBSERVED_LABEL (recipient): jaywisdom.base.eth
TOKEN_DISPLAY_NAME       : jaywisdom
```

**Classification**
- BASE_TX_OBJECT             = PASS_AS_SUPPLIED
- BASE_EXTERNAL_REPLAY       = REPORTED_PASS
- INDEPENDENT_LIVE_REPLAY    = NOT_PERFORMED

---

## 3. JOIN STATUS

```
BASE_TX ↔ COINBASE_ORDER   = UNBOUND / NO JOIN
ONCHAIN_BINDING            = NONE
IDENTITY_BINDING           = NONE
```

**Strongest invariant**
```
TWO VALID OBJECTS ≠ A VALID JOIN
```

---

## 4. ADDRESS STATUS (observed)

```
ADDRESS                  : 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
TYPE                     : Contract (Proxy)
REVERSE / BASENAME       : jaywisdom.base.eth
```

**Firewall**
```
ENS_NAME / BASENAME      ≠ WALLET_OWNERSHIP
LABEL                    ≠ AUTHORITY
OBSERVATION              ≠ CONTROL
CONTRACT ADDRESS         ≠ CONNECTED WALLET
```

---

## 5. EXTERNAL SOURCE CHECK

```
GITHUB_BLUE_BABY_RECEIPT       = NOT FOUND (prior to this file)
GOOGLE_DRIVE_BLUE_BABY_RECEIPT = NOT FOUND
SOURCE_STATE                   = CHAT-SUPPLIED ONLY → now anchored in this file
```

---

## 6. FINAL LOCKED STATE

```
COINBASE_RECORD              = PASS
COINBASE_EXTERNAL_REPLAY     = HOLD
BASE_TX_OBJECT               = PASS_AS_SUPPLIED
BASE_EXTERNAL_REPLAY         = REPORTED_PASS
INDEPENDENT_LIVE_REPLAY      = NOT_PERFORMED
BASE_TX ↔ COINBASE_ORDER     = UNBOUND / NO JOIN
ONCHAIN_BINDING              = NONE
IDENTITY_BINDING             = NONE
WRITE_ACTION (original probe)= FALSE
WRITE_ACTION (this artifact) = TRUE (file creation only)
```

---

## 7. PERMANENT FIREWALL EQUATIONS

```
TICKER                    ≠ CONTRACT
ACCOUNT / DISPLAY LABEL   ≠ LEGAL_IDENTITY
ENS_NAME / BASENAME       ≠ WALLET_OWNERSHIP
COINBASE RECORD           ≠ BLOCKCHAIN REPLAY
OBSERVATION               ≠ VERIFICATION
TWO VALID OBJECTS         ≠ A VALID JOIN
LABEL                     ≠ AUTHORITY
CONTRACT ADDRESS          ≠ CONNECTED WALLET
```

---

**End of receipt.**
This artifact exists solely to preserve the provenance state.
No identity promotion has been performed.
No control claim has been made.
