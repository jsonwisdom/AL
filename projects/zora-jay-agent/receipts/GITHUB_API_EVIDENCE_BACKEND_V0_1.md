# GITHUB_API_EVIDENCE_BACKEND_V0_1

## STATUS: GITHUB_API_BACKEND_SCAFFOLD_LANDED
## REPO: jsonwisdom/AL
## PROJECT_LANE: projects/zora-jay-agent
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This receipt records the first read-only GitHub API backend for the AL / Zora Jay Agent evidence collector.

## Files Landed

```text
projects/zora-jay-agent/evidence-collector/backend/package.json
projects/zora-jay-agent/evidence-collector/backend/server.js
projects/zora-jay-agent/evidence-collector/backend/README.md
projects/zora-jay-agent/evidence-collector/index.html
```

## Backend Purpose

```text
purpose=auto_fill_github_evidence_on_replay
mode=read_only_github_api
repo=jsonwisdom/AL
base_receipt=44da17d559f7df8f6a0d5049375a9a823a63c2b9
head=master
workflow=.github/workflows/al-jay-agent-zora-sleep-console.yml
```

## Evidence Fetched

```text
repo_metadata=true
compare_base_to_head=true
workflow_file_read=true
workflow_runs_read=true
latest_run_artifacts_read=true
```

## Explicit Non-Capabilities

```text
workflow_dispatch=false
workflow_write=false
contents_write=false
chain_write=false
sepolia_rpc=false
wallet_control=false
ai_backend=false
money_making_claim=false
```

## Secret Boundary

```text
GITHUB_TOKEN_LOCATION=server_only
GITHUB_TOKEN_IN_BROWSER=forbidden
RECOMMENDED_SCOPE=contents:read,actions:read,metadata:read
PRIVATE_KEYS_IN_BROWSER=forbidden
AI_API_KEY_IN_BROWSER=forbidden
RPC_WRITE_KEY_IN_BROWSER=forbidden
```

## Frontend Change

The evidence collector now includes a `Fetch GitHub Evidence` button that calls:

```text
GET /api/github-evidence
```

The response auto-fills:

```text
commits
workflow_runs
artifacts
unknowns
```

Sepolia remains manual / false unless read-only RPC evidence is added in a later receipt.

## Highest Defensible State

```text
GITHUB_API_BACKEND = SCAFFOLD_LANDED
GITHUB_EVIDENCE_AUTOFILL = WIRED
SEPOLIA_RPC_BACKEND = NOT_INCLUDED
WORKFLOW_DISPATCH = FALSE
WALLET_CONTROL = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```

## Next Best Action

Run the backend with a read-only GitHub token and verify the `/api/github-evidence` JSON response against the GitHub UI/API.

Do not add workflow dispatch until a separate workflow-write authority receipt exists.

## Ruling

```text
BACKEND_GITHUB = LANDED_AS_READ_ONLY_SCAFFOLD
RECEIPTS_BEFORE_THEATER = TRUE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
