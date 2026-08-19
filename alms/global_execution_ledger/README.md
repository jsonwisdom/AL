# JSONWisdom Global Execution Ledger — v0.1

Status: `SKELETON / REVIEW_ONLY / NO_SYNTHETIC_RUNS`

```text
authority = false
no_fake_green = true
```

## Purpose

Provide one append-only arithmetic surface for machine-speed replay across JSONWisdom repositories and ALMS workflows.

The ledger is intended to answer, per real execution:

- repository / ref / commit
- workflow run ID and attempt
- started / completed timestamps
- replay runner exit code
- hard-gate disposition
- items requested / observed / validated / passed / held / conflicted / rejected / indeterminate
- receipt IDs and source hashes
- replay hash
- optional ReceiptOS frame and ENS discovery pointer

It does **not** convert workflow execution into factual truth, legal authority, or whole-lane GREEN.

## Files

- Schema: `schemas/JSONWISDOM_GLOBAL_EXECUTION_LEDGER_V0_1.schema.json`
- Writer: `scripts/alms_append_global_execution_ledger.py`
- Future runtime ledger: `alms/global_execution_ledger/ledger.jsonl`

`ledger.jsonl` is intentionally absent until a real workflow run is bound. Do not seed it with a fabricated first execution.

## Append contract

Each row is one JSON object. The writer:

1. requires explicit workflow identity, commit, start/completion timestamps, and runner exit code;
2. hashes the exact replay report when present;
3. derives counters from `ci/corpus_report.json`;
4. rejects duplicate `workflow_run_id + workflow_attempt` bindings;
5. links the new row to the previous row with `previous_entry_sha256`;
6. computes `entry_sha256` over the canonical JSON payload before the hash field is added;
7. validates the completed record against the v0.1 schema;
8. appends one line only after validation.

## Replay parameter 125

The user-requested replay parameter `125` remains **unit-unbound**.

Do not write it into the execution ledger as cases, scans, repos, workers, or any other unit until an explicit contract binds the unit. When bound, use:

```json
{
  "requested_replay_parameter": {
    "value": 125,
    "unit": "<EXPLICIT_UNIT>"
  }
}
```

## Current integration boundary

The writer is **not yet wired into** `alms-auto-replay-and-bump.yml` in v0.1. This avoids creating partial or fabricated execution receipts before the workflow has an exact timestamp/exit-code binding strategy for both successful and failed runs.

The first integration patch should preserve these invariants:

```text
RUNNER_FAIL          -> WORKFLOW_FAIL
FAILED_RUN           -> STILL_ELIGIBLE_FOR_EXECUTION_RECEIPT
LEDGER_APPEND_FAIL   -> NO_GREEN
REPLAY_SUCCESS       != FACT_TRUE
RECEIPT              != VERDICT
AUTHORITY_CREATED    = FALSE
```
