# Jay EVM Address Registry v1

Status: CANONICAL_SEARCH_REGISTRY
Purpose: Machine-searchable EVM address registry for Jay Wisdom / JSONWisdom identity, Zora creator search, Base/ENS lookup, and forensic replay workflows.

This document records known Jay Wisdom EVM addresses and contract anchors for deterministic search. It does not assert legal ownership beyond the stated context. Any wallet, contract, transaction, or profile claim must still be verified against its own public receipt.

## Canonical Search Rule

- Preserve checksum formatting when displaying addresses.
- Use lowercase copies only for machine search and matching.
- Do not treat a transaction hash as a contract address.
- Do not treat a profile wallet as a creator coin contract unless separately verified.
- Do not treat ENS/Basename resolution as ownership proof without a current resolver check.

## Address Registry

| Label | Address | Context | Tags |
|---|---|---|---|
| ZORA_CREATOR_COIN_CONTRACT | `0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f` | JAYWISDOM creator coin / Zora contract candidate | JAYWISDOM, ZORA, CREATOR_COIN, CONTRACT |
| BASE_ENS_WALLET | `0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8` | jaywisdom.base.eth / Base ENS identity wallet | JAYWISDOM, BASE, ENS, BASENAME |
| ZORA_PROFILE_WALLET | `0x829adfedbe565f9885a7ea6bc78912acaef055e2` | Zora profile wallet for `https://zora.co/@jaywisdom` | JAYWISDOM, ZORA, PROFILE, WALLET |
| METAMASK_WALLET_PRIMARY | `0x992d94aA31dcD8fDb7d8E6885370ef8202AED399` | Jay MetaMask wallet | JAYWISDOM, METAMASK, EVM |
| UNISWAP_WALLET | `0xF18E616d5F315435F9A0C48EeD52048d4051FB27` | Jay Uniswap wallet | JAYWISDOM, UNISWAP, EVM |
| METAMASK_WALLET_SECONDARY | `0xC345B26094c63C69222Ee775189a3d3eaead5a84` | Jay secondary MetaMask wallet | JAYWISDOM, METAMASK, EVM |

## Machine Search JSON

```json
{
  "registry_id": "JAY_EVM_ADDRESS_REGISTRY_V1",
  "root_identities": [
    "jaywisdom.eth",
    "jaywisdom.base.eth",
    "JSONWisdom",
    "Jay Wisdom"
  ],
  "zora_profile": "https://zora.co/@jaywisdom",
  "addresses": [
    {
      "label": "ZORA_CREATOR_COIN_CONTRACT",
      "address": "0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f",
      "address_lc": "0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f",
      "context": "JAYWISDOM creator coin / Zora contract candidate",
      "tags": ["JAYWISDOM", "ZORA", "CREATOR_COIN", "CONTRACT"]
    },
    {
      "label": "BASE_ENS_WALLET",
      "address": "0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8",
      "address_lc": "0xa380552a27b0a5a2874ea7aa52cac09f542002e8",
      "context": "jaywisdom.base.eth / Base ENS identity wallet",
      "tags": ["JAYWISDOM", "BASE", "ENS", "BASENAME"]
    },
    {
      "label": "ZORA_PROFILE_WALLET",
      "address": "0x829adfedbe565f9885a7ea6bc78912acaef055e2",
      "address_lc": "0x829adfedbe565f9885a7ea6bc78912acaef055e2",
      "context": "Zora profile wallet for https://zora.co/@jaywisdom",
      "tags": ["JAYWISDOM", "ZORA", "PROFILE", "WALLET"]
    },
    {
      "label": "METAMASK_WALLET_PRIMARY",
      "address": "0x992d94aA31dcD8fDb7d8E6885370ef8202AED399",
      "address_lc": "0x992d94aa31dcd8fdb7d8e6885370ef8202aed399",
      "context": "Jay MetaMask wallet",
      "tags": ["JAYWISDOM", "METAMASK", "EVM"]
    },
    {
      "label": "UNISWAP_WALLET",
      "address": "0xF18E616d5F315435F9A0C48EeD52048d4051FB27",
      "address_lc": "0xf18e616d5f315435f9a0c48eed52048d4051fb27",
      "context": "Jay Uniswap wallet",
      "tags": ["JAYWISDOM", "UNISWAP", "EVM"]
    },
    {
      "label": "METAMASK_WALLET_SECONDARY",
      "address": "0xC345B26094c63C69222Ee775189a3d3eaead5a84",
      "address_lc": "0xc345b26094c63c69222ee775189a3d3eaead5a84",
      "context": "Jay secondary MetaMask wallet",
      "tags": ["JAYWISDOM", "METAMASK", "EVM"]
    }
  ],
  "promotion_limits": [
    "Receipt required before contract classification is promoted.",
    "Resolver check required before ENS/Basename ownership promotion.",
    "Chain explorer or RPC lookup required before token metadata promotion."
  ]
}
```

## Zora Search Targets

Use the following terms when machine-searching Zora or local logs:

```text
jaywisdom
JAYWISDOM
JSONWisdom
jaywisdom.eth
jaywisdom.base.eth
https://zora.co/@jaywisdom
0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f
0x829adfedbe565f9885a7ea6bc78912acaef055e2
```

## Verification Status

Current status: REGISTRY_DECLARED_FROM_OPERATOR_MEMORY

This registry is commit-ready but each address should be independently verified against live chain/profile receipts before being promoted to FINAL_VERIFIED.

Seal: RECEIPTS_OVER_AUTHORITY
