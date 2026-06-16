# MORNING_REPLAY_PROMPT_V0_1

## STATUS: READY_FOR_NEW_THREAD_REPLAY
## CONTROLLER_LABEL: jaywisdom.base.eth
## REPO: jsonwisdom/AL
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This prompt is for the next morning thread.

The user should only need to say:

```text
replay
```

## New Thread Replay Contract

When the user says `replay`, produce a before-and-after GitHub Overnight Maintenance Report for:

```text
repo=jsonwisdom/AL
project_lane=projects/zora-jay-agent
workflow=.github/workflows/al-jay-agent-zora-sleep-console.yml
agent=jay-agent
mcp_agent=MCP_AGENT_15_MINUTE_TASKS
controller_label=jaywisdom.base.eth
sepolia_wallet=0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5
mode=read_only_maintenance
cadence=15_minutes
```

## What To Check First

1. Fetch the latest state of `jsonwisdom/AL`.
2. Read the current head commit on `master`.
3. Inspect recent commits since this receipt.
4. Inspect recent workflow runs for `al-jay-agent-zora-sleep-console.yml`.
5. Inspect artifacts from the overnight workflow runs if available.
6. Read project files under `projects/zora-jay-agent/`.
7. Read issue `#322` if available.
8. Compare before state to after state.

## Report Shape

Produce this report:

```text
GITHUB OVERNIGHT MAINTENANCE REPORT

BEFORE:
- starting repo
- starting branch
- starting head if known
- expected workflow
- expected cadence
- staged Sepolia wallet

AFTER:
- latest head
- workflow run count observed
- latest workflow status
- artifacts observed
- commits added overnight
- files changed overnight
- MCP/jay-agent findings
- Sepolia status: staged only unless evidence says otherwise

RULING:
- maintenance loop: GREEN/YELLOW/RED
- workflow visibility: GREEN/YELLOW/RED
- artifacts: GREEN/YELLOW/RED
- wallet action: FALSE unless explicitly proven
- semantic truth final: FALSE
- authority: FALSE
- no_fake_green: TRUE
```

## Boundaries

```text
DO NOT claim wallet control from address alone.
DO NOT claim Sepolia transaction success unless transaction hash and receipt are present.
DO NOT claim Zora semantic purpose unless decoded evidence exists.
DO NOT claim GitHub workflow success unless run status is observed.
DO NOT claim artifact existence unless artifact readback is observed.
DO NOT promote UNKNOWN to TRUE or FALSE.
```

## Morning Goal

```text
Wake Jay up with evidence, not chaos.
Show what changed overnight.
Show what did not change.
Show what is still unknown.
Preserve the next best action.
```

## Ruling

```text
MORNING_REPLAY_PROMPT = READY
NEW_THREAD_TRIGGER_WORD = replay
BEFORE_AFTER_REPORT = REQUIRED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
