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
- Ledger writer: `scripts/alms_append_global_execution_ledger.py`
- Execution-receipt writer: `scripts/alms_write_execution_receipt.py`
- Execution receipts: `alms/execution_receipts/*.json`
- Future runtime ledger: `alms/global_execution_ledger/ledger.jsonl`

`ledger.jsonl` is intentionally absent until a real workflow run is bound. Do not seed it with a fabricated first execution.

## Append contract

Each ledger row is one JSON object. The ledger writer:

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

`alms-auto-replay-and-bump.yml` now captures the replay runner exit code instead of swallowing it. The workflow writes a terminal execution receipt on the post-run path and explicitly fails the workflow when the replay runner exited non-zero.

Promotion artifacts are only staged when replay, version bump, and Merkle publication all complete as a clean PASS. The version-bump subprocess is invoked with `check=True` so a failed bump cannot silently continue to Merkle publication.

The execution receipt writer distinguishes `PASS`, `FAIL`, `INDETERMINATE`, and `ERROR`, binds the corpus report hash when available, fixes `authority=false` and `no_fake_green=true`, and does not claim RFC 8785 JCS compatibility for its local deterministic JSON hashing method.

The global JSONL ledger writer is **not yet invoked by the workflow**. The next integration step is to index committed `alms/execution_receipts/*.json` into `alms/global_execution_ledger/ledger.jsonl` without changing the workflow disposition.

### Timeout / cancellation boundary

The terminal execution receipt is a post-run step. Normal non-zero exits and recoverable runner failures are receipted. A whole-job timeout, workflow cancellation, or runner-host loss can prevent that post-step from executing. Closing that gap requires a two-phase durable receipt (`STARTED` before replay, `TERMINAL` after replay) or an external watcher.

```text
RUNNER_FAIL          -> EXECUTION_RECEIPT_ATTEMPT + WORKFLOW_FAIL
RUNNER_PASS          -> RECEIPT + PROMOTION_ELIGIBILITY
BUMP_FAIL            -> NO_MERKLE_PROMOTION
MERKLE_FAIL          -> NO_PROMOTION_ARTIFACT_COMMIT
RECEIPT_PUSH_FAIL    -> WORKFLOW_FAILS; DURABILITY_NOT_CLAIMED
LEDGER_APPEND_FAIL   -> NO_GREEN
REPLAY_SUCCESS       != FACT_TRUE
RECEIPT              != VERDICT
AUTHORITY_CREATED    = FALSE
```
