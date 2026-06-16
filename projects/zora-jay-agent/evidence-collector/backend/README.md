# Read-Only Evidence Backend

## STATUS: GITHUB_API_AND_SEPOLIA_RPC_SCAFFOLD
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This backend serves the AL Evidence Collector and fetches read-only GitHub plus Sepolia evidence server-side.

It does not run workflows, dispatch workflows, write commits, control wallets, sign messages, broadcast transactions, or call an AI provider.

## GitHub evidence reads

```text
repo=jsonwisdom/AL
base=44da17d559f7df8f6a0d5049375a9a823a63c2b9
head=master
workflow=.github/workflows/al-jay-agent-zora-sleep-console.yml
```

## Sepolia evidence reads

```text
wallet=0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5
rpc_default=https://rpc.sepolia.org
rpc_override_env=SEPOLIA_RPC_URL
mode=read_only
```

The Sepolia endpoint observes balance and scans a limited recent block window for matching transactions. Public RPC may be rate-limited and may not be suitable for deep transaction history.

## Required environment

```bash
export GITHUB_TOKEN="github_pat_or_fine_grained_token_here"
export SEPOLIA_RPC_URL="https://rpc.sepolia.org"
export PORT=8787
npm install
npm start
```

`SEPOLIA_RPC_URL` may be replaced with an Alchemy, Infura, or other read-only Sepolia endpoint.

## Token scope

Use the smallest read-only GitHub scope available.

Recommended fine-grained GitHub token permissions:

```text
Repository: jsonwisdom/AL only
Contents: read
Actions: read
Metadata: read
```

Do not grant write permission for this backend.

## API

```text
GET /api/health
GET /api/github-evidence?repo=jsonwisdom/AL&base=44da17d559f7df8f6a0d5049375a9a823a63c2b9&head=master
GET /api/sepolia-evidence?wallet=0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5&limit=8
```

## Returned GitHub evidence

```text
repo metadata
compare base...head
workflow file existence
recent workflow runs
latest-run artifacts
NO_FAKE_GREEN ruling fields
```

## Returned Sepolia evidence

```text
chain id
latest block
wallet balance wei/eth
recent matching tx hashes when observable
receipt status for matching tx hashes
NO_FAKE_GREEN ruling fields
```

## Boundaries

```text
GITHUB_TOKEN_IN_BROWSER = FORBIDDEN
WORKFLOW_DISPATCH = FALSE
WORKFLOW_WRITE = FALSE
CHAIN_WRITE = FALSE
SEPOLIA_RPC = READ_ONLY
WALLET_CONTROL = FALSE
SIGNING = FALSE
BROADCAST = FALSE
AI_BACKEND = NOT_INCLUDED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```

## Next best action

Run locally or deploy behind a server that can hold server-side environment variables. Then open:

```text
http://localhost:8787
```

Type:

```text
replay
```

Then use the GitHub fetch button from the main collector. For Sepolia frontend integration, review:

```text
projects/zora-jay-agent/evidence-collector/sepolia-adapter.js
```
