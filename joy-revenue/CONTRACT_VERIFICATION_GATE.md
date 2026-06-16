# Contract Verification Gate

## STATUS: ACTIVE
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This gate prevents the revenue indexer from running against an unverified contract target.

A contract address alone is not enough.

## Required inputs

```text
JOY_CONTRACT_ADDRESS=<verified contract address>
CONTRACT_VERIFICATION_STATUS=verified
ZORA_PRODUCT_TYPE=<accepted product type>
```

## Accepted product types

```text
zora_creator_coin
zora_content_coin
zora_1155_collection
verified_erc20
verified_erc1155
```

## Current correction

The previous scaffold refused only the zero address. That was not strict enough.

The indexer now halts unless the contract target is explicitly verified and the product type is known.

## Unknown contract rule

Until independent readback confirms product type and contract behavior, any candidate target remains:

```text
CONTRACT_VERIFIED = FALSE
PRODUCT_TYPE = UNKNOWN
REVENUE_SOURCE = UNCONFIRMED
INDEXER_TARGET = BLOCKED
```

## Ruling

```text
REVENUE_INDEXER_TARGET_GATE = ACTIVE
CONTRACT_ADDRESS_ALONE = INSUFFICIENT
NO_INDEXING_UNTIL_VERIFIED = TRUE
CHAIN_WRITE = FALSE
WALLET_CONTROL = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
