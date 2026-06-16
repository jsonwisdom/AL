# SEPOLIA_WEBSOCKET_SUBSCRIPTION_V0_1

## STATUS: WEBSOCKET_SUBSCRIPTION_SCAFFOLD_LANDED
## REPO: jsonwisdom/AL
## PROJECT_LANE: projects/zora-jay-agent
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This receipt records the first read-only WebSocket live witness subsystem for the AL / Zora Jay Agent Sepolia evidence layer.

## Files Landed

```text
projects/zora-jay-agent/evidence-collector/backend/ws-subscription.js
projects/zora-jay-agent/evidence-collector/backend/WEBSOCKET_SUBSCRIPTION.md
```

## Subscription Mode

```text
mode=read_only_websocket_witness
required_env=SEPOLIA_WS_URL
optional_env=SEPOLIA_WATCH_WALLET
current_subscription=eth_subscribe:newHeads
wallet_specific_filter=false
```

## What It Proves

```text
live_websocket_connection_possible=true
new_head_events_observable=true
json_line_evidence_output=true
```

## What It Does Not Prove

```text
wallet_control=false
wallet_activity=false_until_filtered_tx_receipt
chain_write=false
signing=false
broadcast=false
money_making_claim=false
```

## Safe Next Layer

After testing `newHeads`, add wallet-specific observation by:

```text
1. subscribe newHeads
2. fetch full block for each new head
3. filter transactions where from/to == watched wallet
4. fetch receipt for matched tx
5. emit evidence JSON
```

Do not claim wallet activity from block headers alone.

## Dependency Note

Package mutation was blocked by tooling safety checks, so dependency is documented separately:

```bash
npm install ws
```

## Highest Defensible State

```text
WEBSOCKET_SUBSCRIPTION = SCAFFOLD_LANDED
LIVE_HEAD_WITNESS = READY_FOR_TEST
WALLET_SPECIFIC_WS_FILTER = NOT_INCLUDED
CHAIN_WRITE = FALSE
WALLET_CONTROL = FALSE
SIGNING = FALSE
BROADCAST = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```

## Ruling

```text
WEBSOCKET_SUBSYSTEM = LANDED_AS_READ_ONLY_SCAFFOLD
RECEIPTS_BEFORE_THEATER = TRUE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
