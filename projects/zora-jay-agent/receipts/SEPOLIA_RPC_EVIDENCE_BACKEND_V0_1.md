# SEPOLIA_RPC_EVIDENCE_BACKEND_V0_1

## STATUS: SEPOLIA_RPC_BACKEND_SCAFFOLD_LANDED
## REPO: jsonwisdom/AL
## PROJECT_LANE: projects/zora-jay-agent
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This receipt records the first read-only Sepolia RPC evidence backend for the AL / Zora Jay Agent evidence collector.

## Files Changed

```text
projects/zora-jay-agent/evidence-collector/backend/server.js
projects/zora-jay-agent/evidence-collector/backend/README.md
projects/zora-jay-agent/evidence-collector/sepolia-adapter.js
```

## Endpoint Landed

```text
GET /api/sepolia-evidence?wallet=0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5&limit=8
```

## RPC Configuration

```text
DEFAULT_RPC=https://rpc.sepolia.org
OVERRIDE_ENV=SEPOLIA_RPC_URL
MODE=read_only
```

## Evidence Fetched

```text
chain_id=true
latest_block=true
wallet_balance=true
recent_matching_transactions=true
transaction_receipt_status=true
```

## Public RPC Limitation

```text
PUBLIC_RPC_RATE_LIMITS_POSSIBLE=true
DEEP_HISTORY_INDEXING=false
SCAN_WINDOW_LIMITED=true
ALCHEMY_OR_INFURA_RECOMMENDED_FOR_DEEP_HISTORY=true
```

## Explicit Non-Capabilities

```text
chain_write=false
wallet_control=false
signing=false
broadcast=false
private_key_required=false
workflow_dispatch=false
money_making_claim=false
```

## Frontend State

```text
MAIN_INDEX_HTML_PATCH_ATTEMPTED=true
MAIN_INDEX_HTML_PATCH_LANDED=false
REASON=tool_safety_blocked_full_html_replacement
SEPARATE_ADAPTER_LANDED=true
ADAPTER_PATH=projects/zora-jay-agent/evidence-collector/sepolia-adapter.js
```

## Highest Defensible State

```text
SEPOLIA_RPC_BACKEND = SCAFFOLD_LANDED
SEPOLIA_EVIDENCE_ENDPOINT = LANDED
SEPOLIA_FRONTEND_ADAPTER = LANDED
MAIN_COLLECTOR_BUTTON = NOT_PATCHED
CHAIN_WRITE = FALSE
WALLET_CONTROL = FALSE
SIGNING = FALSE
BROADCAST = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```

## Next Best Action

Run the backend and verify:

```text
GET /api/health
GET /api/sepolia-evidence?wallet=0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5&limit=8
```

If public RPC is slow or rate-limited, set:

```text
SEPOLIA_RPC_URL=<alchemy_or_infura_sepolia_endpoint>
```

Do not add workflow dispatch until a separate workflow-write authority receipt exists.

## Ruling

```text
BACKEND_SEPOLIA = LANDED_AS_READ_ONLY_SCAFFOLD
FRONTEND_ADAPTER = LANDED
MAIN_UI_PATCH = NOT_LANDED
RECEIPTS_BEFORE_THEATER = TRUE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
