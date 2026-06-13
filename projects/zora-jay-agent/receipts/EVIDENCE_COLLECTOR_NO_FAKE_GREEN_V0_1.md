# EVIDENCE_COLLECTOR_NO_FAKE_GREEN_V0_1

## STATUS: FRONTEND_EVIDENCE_COLLECTOR_LANDED
## REPO: jsonwisdom/AL
## PROJECT_LANE: projects/zora-jay-agent
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This receipt records the first-pass evidence collector shell for the AL / Zora Jay Agent maintenance lane.

## Built Artifact

```text
path=projects/zora-jay-agent/evidence-collector/index.html
purpose=browser-only evidence collector
trigger=replay
mode=local_parse_only
backend=false
wallet_control=false
chain_write=false
workflow_write=false
```

## Design Ruling

The collector is not a money-making claim, not a wallet controller, not a workflow runner, and not a blockchain verifier.

It is an evidence intake surface that preserves unknowns and refuses fake green.

## Enforced Rules

```text
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
DEFAULT_STATUS = UNKNOWN
GREEN_REQUIRES_EVIDENCE_STRING = TRUE
SEPOLIA_ACTION_REQUIRES_BALANCE_AND_TX_HASH = TRUE
UNKNOWN_IS_NOT_PROMOTED = TRUE
```

## Operator Inputs

```text
commits = git log / GitHub compare evidence
workflow_runs = GitHub Actions run status or API response
artifacts = artifact list or artifact readback
sepolia = balance + tx hash + receipt evidence if present
mcp_agent = MCP_AGENT_15_MINUTE_TASKS output
unknowns = explicitly preserved unresolved fields
```

## Boundaries

```text
DO_NOT_CLAIM_WALLET_CONTROL_FROM_ADDRESS_ALONE = TRUE
DO_NOT_CLAIM_SEPOLIA_SUCCESS_WITHOUT_TX_HASH_AND_RECEIPT = TRUE
DO_NOT_CLAIM_WORKFLOW_SUCCESS_WITHOUT_OBSERVED_RUN_STATUS = TRUE
DO_NOT_CLAIM_ARTIFACT_EXISTENCE_WITHOUT_ARTIFACT_READBACK = TRUE
DO_NOT_PROMOTE_UNKNOWN_TO_TRUE_OR_FALSE = TRUE
```

## Current Highest Defensible State

```text
EVIDENCE_COLLECTOR_FRONTEND = LANDED
AI_BACKEND = NOT_INCLUDED
GITHUB_API_BACKEND = NOT_INCLUDED
SEPOLIA_RPC_BACKEND = NOT_INCLUDED
AUTONOMOUS_AGENT_CONTROL = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```

## Next Best Action

Wire the collector to a backend only after secrets and API permissions are explicitly scoped.

Recommended backend gates:

```text
GITHUB_TOKEN_SCOPE = actions:read, contents:read
SEPOLIA_RPC = read_only
WALLET_PRIVATE_KEY = NEVER_IN_BROWSER
AI_API_KEY = SERVER_SIDE_ONLY
WRITE_ACTIONS = DISABLED_BY_DEFAULT
```

## Ruling

```text
RECEIPTS_BEFORE_THEATER = TRUE
DASHBOARD_SECOND = TRUE
EVIDENCE_COLLECTOR_FIRST = TRUE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
