# JOY Revenue — Path C Read-Only Scaffold

## STATUS: PATH_C_REVENUE_REPORTING_SCAFFOLD
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This package is a zero-key, read-only revenue and ownership observation scaffold.

It does not sign, broadcast, mint, collect, transfer, or control a wallet.

## What landed

```text
joy-revenue/package.json
joy-revenue/src/config.ts
joy-revenue/src/rpc.ts
joy-revenue/src/state.ts
joy-revenue/src/indexer.ts
joy-revenue/scripts/check-no-keys.ts
.github/workflows/joy-revenue-ci-no-keys.yml
```

## Runtime

```bash
cd joy-revenue
npm install
RPC_URL=wss://your-sepolia-or-base-node.example/ws \
JOY_CONTRACT_ADDRESS=0x0000000000000000000000000000000000000000 \
START_BLOCK=0 \
npm run dev
```

The zero address placeholder refuses fake indexing. Set `JOY_CONTRACT_ADDRESS` to a real contract only when the contract target is verified.

## Zero-key gate

```bash
cd joy-revenue
npm run check:no-keys
```

The CI workflow enforces the same check for changes under `joy-revenue/**`.

## Current observed event

```text
Transfer(address indexed from, address indexed to, uint256 tokenId)
```

## Explicit non-capabilities

```text
chain_write=false
wallet_control=false
signing=false
broadcast=false
minting=false
revenue_claim=false
authority=false
no_fake_green=true
```

## Path D hook

A future calldata constructor may be added as a separate non-broadcast artifact generator.

It must produce unsigned JSON only and must not import wallet clients or broadcast methods.

## Ruling

```text
PATH_C_REVENUE_REPORTING = SCAFFOLDED_READ_ONLY
ZERO_KEY_CI = LANDED
PATH_D_CALLDATA = NOT_INCLUDED
CHAIN_WRITE = FALSE
WALLET_CONTROL = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
