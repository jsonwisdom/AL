# AL_TRANSFER_ZORA_JAY_AGENT_RECEIPT_V0_1

## STATUS: TRANSFERRED_TO_AL_ROOT_WORKFLOW_SURFACE
## SOURCE_TARGET: ZORA
## AGENT: jay-agent
## CONTROLLER_LABEL: jaywisdom.base.eth
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

The Zora jay-agent console has been transferred into the AL repository as a first-class project lane.

## Reason

The immediate operational requirement is workflow accessibility. The workflow now lives under the AL repository workflow directory:

```text
.github/workflows/al-jay-agent-zora-sleep-console.yml
```

Project content lives under:

```text
projects/zora-jay-agent/
```

## Preserved Files

```text
projects/zora-jay-agent/README.md
projects/zora-jay-agent/scripts/jay_agent_sleep_console.sh
.github/workflows/al-jay-agent-zora-sleep-console.yml
projects/zora-jay-agent/receipts/AL_TRANSFER_ZORA_JAY_AGENT_RECEIPT_V0_1.md
```

## Sleep Goal

Run the jay-agent Zora maintenance console every 15 minutes and preserve artifacts for morning replay.

## Boundaries

```text
JAY-AGENT = OBSERVER
ZORA = TARGET SURFACE
AL = ROOT WORKFLOW HOST
GITHUB ACTIONS = TRIGGER SURFACE
SEMANTIC TRUTH FINAL = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```

## Ruling

```text
TRANSFER TO AL = GREEN
WORKFLOW ACCESS SURFACE = GREEN
READ_ONLY MAINTENANCE = GREEN
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
