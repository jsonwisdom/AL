# Zora Jay-Agent Console

## STATUS: TRANSFERRED_TO_AL
## TARGET: ZORA
## CONTROLLER_LABEL: jaywisdom.base.eth
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This project lane moves the Zora jay-agent sleep console into the AL repository so GitHub workflows can be run from AL's repository-root `.github/workflows/` directory.

## Mission

The jay-agent console is a read-only maintenance and observation surface for Zora-facing work.

It watches repo state, trigger surfaces, unknown metadata surfaces, and proof/receipt drift.

## Allowed

- read repository state
- snapshot project files
- scan for UNKNOWN, YELLOW, TODO, FIXME, NO_FAKE_GREEN markers
- upload workflow artifacts
- preserve receipt boundaries

## Not Allowed

- no wallet signing
- no minting
- no token buy or sell actions
- no final semantic truth claim
- no authority claim
- no ownership claim

## Current Sleep Goal

Every 15 minutes, the AL workflow should leave the project better than it found it by producing a fresh maintenance artifact.

## Boundary

```text
AL ROOT WORKFLOW = ACCESSIBLE TRIGGER SURFACE
JAY-AGENT = OBSERVER
ZORA = TARGET SURFACE
BASE = ANCHOR SURFACE
GITHUB = PUBLIC MIRROR
MACHINE GREEN = CONSISTENCY ONLY
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
