# MCP_AGENT_ASSIGNMENT_15_MINUTE_TASKS_V0_1

## STATUS: MCP_AGENT_ASSIGNED
## TARGET: ZORA
## HOST_REPO: jsonwisdom/AL
## CADENCE: 15_MINUTES
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

jay-agent assigns MCP Agent as a read-only maintenance worker for the AL-hosted Zora lane.

## Role

MCP Agent is not a wallet agent, trading agent, minting agent, or authority agent.

MCP Agent is a maintenance observer whose job is to leave the repo better by producing cleaner readbacks, task snapshots, and alarm receipts.

## 15 Minute Task Loop

Every scheduled run should answer:

```text
1. What changed since the last known head?
2. Did the jay-agent Zora lane remain readable?
3. Are UNKNOWN or YELLOW surfaces preserved instead of promoted?
4. Did the repo produce a new maintenance snapshot?
5. Are workflow artifacts present for morning replay?
6. Is Sepolia wallet work still staged instead of executed without human approval?
7. Is NO_FAKE_GREEN still true?
```

## Production Alarm Rule

The production alarm is informational only.

```text
ALARM_GREEN = workflow ran and artifacts were produced
ALARM_YELLOW = unknowns or staged tasks remain
ALARM_RED = script failure, missing artifacts, missing workflow, or fake authority claim
```

## Next Run Task Queue

```text
TASK_001: run jay-agent sleep console
TASK_002: run MCP production alarm snapshot
TASK_003: scan Zora lane markers
TASK_004: preserve Sepolia wallet task as STAGED_ONLY
TASK_005: produce artifact hashes
TASK_006: hold semantic truth YELLOW unless receipts prove otherwise
```

## Tomorrow Sepolia Learning Gate

```text
sepolia_wallet_creation = STAGED_ONLY
private_key_handling = LOCAL_ONLY
cloudshell_required = TRUE
human_approval_required = TRUE
funding_required = Sepolia faucet only
real_asset_risk = FALSE if testnet only
```

## Boundary

```text
MCP_AGENT = OBSERVER
15_MINUTE_RUN = MAINTENANCE LOOP
PRODUCTION_ALARM = READBACK SIGNAL
STAGED_SEPOLIA_WALLET != WALLET_CONTROL_PROOF
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
