# Revenue Readback Fetcher

## STATUS: READ_ONLY_FETCHER_SCAFFOLD
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This document describes the read-only fetcher for JOY revenue gates 2-4.

It does not sign, broadcast, mint, claim rewards, withdraw funds, or control a wallet.

## Script

```text
joy-revenue/src/revenue-readback.ts
```

Run:

```bash
cd joy-revenue
npm install
RPC_URL=https://your-base-rpc.example \
JOY_CONTRACT_ADDRESS=0x0000000000000000000000000000000000000000 \
CONTRACT_VERIFICATION_STATUS=verified \
ZORA_PRODUCT_TYPE=zora_content_coin \
START_BLOCK=0 \
npm run readback
```

The zero address placeholder will halt. Replace it only after the target contract is verified.

## Gate 2: Holders / Volume / Market Surface

The fetcher reads:

```text
ERC20 name
ERC20 symbol
ERC20 decimals
ERC20 totalSupply
Transfer logs from START_BLOCK to latest block
unique senders observed
unique recipients observed
unique touched addresses observed
raw transfer volume observed
sample transfers
```

This is a transfer-log surface only. It does not equal confirmed holder count unless cross-checked against a token tracker or indexed balance reconstruction.

## Gate 3: Token Contract Readback

The fetcher requires the existing contract verification gate:

```text
CONTRACT_VERIFICATION_STATUS=verified
ZORA_PRODUCT_TYPE=<accepted product type>
```

A contract address alone is insufficient.

## Gate 4: Creator Rewards / Earnings

Creator earnings are optional and must be configured explicitly:

```text
CREATOR_ADDRESS=<creator address>
REWARDS_CONTRACT_ADDRESS=<rewards contract address>
REWARDS_EVENT_ABI='event Example(address indexed creator,uint256 amount)'
```

If those are missing, the fetcher reports:

```text
creator_earnings_confirmed=false
reason=rewards source not configured
```

Do not infer earnings from token price, market surface, or transfer activity.

## Ruling

```text
READBACK_FETCHER = LANDED
GATES_2_TO_4 = READ_ONLY_SUPPORTED
REWARDS_DETECTION = OPTIONAL_CONFIG_REQUIRED
CREATOR_EARNINGS = FALSE_UNTIL_REWARDS_LOG_MATCH
CHAIN_WRITE = FALSE
WALLET_CONTROL = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
