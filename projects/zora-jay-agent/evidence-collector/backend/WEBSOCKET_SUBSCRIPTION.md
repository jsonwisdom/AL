# Sepolia WebSocket Live Witness Subsystem

## STATUS: WEBSOCKET_SUBSCRIPTION_SCAFFOLD
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This subsystem is a read-only live witness layer for Sepolia.

It observes chain events over WebSocket and emits local JSON lines. It does not sign, broadcast, mutate workflow state, control a wallet, or prove ownership of any address.

## Why WebSocket

REST/RPC polling answers: what is true now?

WebSocket subscription answers: what changed live while the observer was connected?

This is useful for:

```text
new block witness stream
live tx/log monitoring
latency-sensitive evidence capture
agent maintenance heartbeat
```

## File

```text
projects/zora-jay-agent/evidence-collector/backend/ws-subscription.js
```

## Dependency

The package update was blocked by tooling safety checks, so install dependency manually before running:

```bash
npm install ws
```

## Run

```bash
export SEPOLIA_WS_URL="wss://YOUR_SEPOLIA_WEBSOCKET_ENDPOINT"
export SEPOLIA_WATCH_WALLET="0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5"
node ws-subscription.js
```

## Current Subscription

```text
eth_subscribe: newHeads
```

This proves the live chain head stream is observable. It does not prove wallet activity by itself.

## Wallet Monitoring Boundary

Ethereum WebSocket nodes do not reliably provide address-specific wallet transaction subscriptions by address alone.

For wallet-specific live monitoring, the next safe layer is:

```text
subscribe newHeads
on each new head fetch block transactions
filter tx.from or tx.to against WATCH_WALLET
fetch receipt for matched tx
emit evidence JSON
```

That should be added only after the base newHeads witness stream is tested.

## Log Monitoring Boundary

`eth_subscribe logs` is useful only when a target contract address and/or topic filter is known.

Do not use logs subscription to claim wallet activity without decoded contract evidence.

## Non-Capabilities

```text
chain_write=false
wallet_control=false
signing=false
broadcast=false
private_key_required=false
workflow_dispatch=false
money_making_claim=false
authority=false
no_fake_green=true
```

## Ruling

```text
WEBSOCKET_SUBSCRIPTION = SCAFFOLD_LANDED
LIVE_HEAD_WITNESS = READY_FOR_TEST
WALLET_SPECIFIC_WS_FILTER = NOT_INCLUDED
CHAIN_WRITE = FALSE
WALLET_CONTROL = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
