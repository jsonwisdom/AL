# ALMS Post-Merge Replay

Directories-first scaffold for constitutional replay against an exact merged commit.

## Replay root

`59448d850d355854956cb5834ebef17f7f14c7dc`

## Required evidence surfaces

- `source/` — exact checked-out source and provenance notes
- `harness/` — executable replay and injected-failure tests
- `matrix/` — constitutional failure-state expectations
- `schemas/` — CRO and attestation receipt schemas
- `ci/` — workflow and dispatch design
- `receipts/` — observed run receipts and final verdicts

## Current state

```text
DIRECTORY_SCAFFOLD_PRESENT = TRUE
REPLAY_WORKFLOW_PRESENT    = FALSE
REPLAY_HARNESS_PRESENT     = FALSE
CRO_SCHEMA_PRESENT         = FALSE
POST_MERGE_RUN_OBSERVED    = FALSE
ALMS_GREEN                 = FALSE
SOVEREIGN_SPHERE_SPIN      = LOCKED
T                          = 1
```

No runtime replay, deterministic-build result, attestation lineage, oracle recovery, injected-failure result, monotonic-counter result, commit status, or CRO verdict is claimed by this scaffold.
