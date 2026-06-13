# Read-Only GitHub Evidence Backend

## STATUS: GITHUB_API_BACKEND_SCAFFOLD
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This backend serves the AL Evidence Collector and fetches GitHub evidence server-side.

It does not run workflows, dispatch workflows, write commits, control wallets, query Sepolia, or call an AI provider.

## What it reads

```text
repo=jsonwisdom/AL
base=44da17d559f7df8f6a0d5049375a9a823a63c2b9
head=master
workflow=.github/workflows/al-jay-agent-zora-sleep-console.yml
```

## Required environment

```bash
export GITHUB_TOKEN="github_pat_or_fine_grained_token_here"
export PORT=8787
npm install
npm start
```

## Token scope

Use the smallest read-only scope available.

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
```

## Returned evidence

```text
repo metadata
compare base...head
workflow file existence
recent workflow runs
latest-run artifacts
NO_FAKE_GREEN ruling fields
```

## Boundaries

```text
GITHUB_TOKEN_IN_BROWSER = FORBIDDEN
WORKFLOW_DISPATCH = FALSE
WORKFLOW_WRITE = FALSE
CHAIN_WRITE = FALSE
SEPOLIA_RPC = NOT_INCLUDED
WALLET_CONTROL = FALSE
AI_BACKEND = NOT_INCLUDED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```

## Next best action

Run locally or deploy behind a server that can hold secrets. Then open:

```text
http://localhost:8787
```

Type:

```text
replay
```

Then click:

```text
Fetch GitHub Evidence
```
