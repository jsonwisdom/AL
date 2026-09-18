# JSONWisdom Global Execution Ledger — v0.1

Status: `WIRED / REVIEW_ONLY / NO_SYNTHETIC_RUNS`

```text
authority = false
proof_inferred = false
no_fake_green = true
```

## Canonical flow

```text
alms/execution_receipts/*.json
        ↓
scripts/alms_consume_execution_receipts.py
        ↓
alms/JSONWISDOM_GLOBAL_EXECUTION_LEDGER.jsonl
        ↓
scripts/alms_bind_active_lanes.py
        ↓
ACTIVE_LANES.json
```

There is **one canonical global ledger path**:

`alms/JSONWISDOM_GLOBAL_EXECUTION_LEDGER.jsonl`

The older direct-append skeleton has been retired. `scripts/alms_append_global_execution_ledger.py` is now only a compatibility entrypoint to the receipt consumer. A ledger row must originate from a sealed execution receipt.

The runtime ledger remains intentionally absent until a real workflow execution receipt is consumed. Do not seed it with a fabricated first row.

## Receipt consumption contract

The consumer:

1. validates each execution receipt's fixed boundaries (`authority=false`, `proof_inferred=false`, `no_fake_green=true`);
2. recomputes and verifies the execution receipt `final_hash` before ingestion;
3. validates every ledger row against `schemas/JSONWISDOM_GLOBAL_EXECUTION_LEDGER_V0_1.schema.json`;
4. verifies the complete existing ledger chain before appending anything;
5. requires monotonically increasing `seq` values;
6. requires `prev_tip = genesis` for the first row and the prior `entry_hash` thereafter;
7. recomputes every existing `entry_hash` and fails closed on any mismatch;
8. is idempotent by both `receipt_id` and `receipt_final_hash`;
9. rejects conflicting duplicate IDs or hashes instead of silently skipping them;
10. appends only after all validation succeeds.

Hashing uses deterministic compact sorted-key UTF-8 JSON:

`JSON_SORTED_KEYS_COMPACT_UTF8_V0_1`

This implementation **does not claim RFC 8785 JCS compatibility**.

## Ledger arithmetic

For a valid ledger:

```text
execution_receipt_count = last.seq
current_tip             = last.entry_hash
PASS                     = count(verdict == PASS)
FAIL                     = count(verdict == FAIL)
INDETERMINATE            = count(verdict == INDETERMINATE)
ERROR                     = count(verdict == ERROR)
```

Every row binds workflow run/attempt, repository, ref, commit, actor/trigger, runner exit code, explicit verdict, explicit hard-gate result, case counters, source hashes, and optional ALMS / ReceiptOS / ENS bindings.

## ACTIVE_LANES pointer law

`ACTIVE_LANES.json.receipt_ptr` may only contain a `receipt_id` that resolves to a verified entry on the canonical ledger.

Known exact bindings in v0.1 are:

```text
AL              -> jsonwisdom/AL
COMPUTERWISDOM  -> jsonwisdom/COMPUTERWISDOM
JOY             -> jsonwisdom/JOY
```

The binder selects the latest verified ledger entry for an exact known repo binding. If no matching real ledger entry exists, the pointer remains `null` and `replay_verdict` remains `UNAVAILABLE`.

A stale/non-resolving pointer is cleared rather than inferred.

## Replay parameter 125

The user-requested replay parameter `125` remains **unit-unbound**.

Do not write it as cases, scans, repos, workers, or any other unit until an explicit contract binds the unit.

## Failure law

```text
RUNNER_FAIL          -> TERMINAL RECEIPT ATTEMPT
RUNNER_FAIL          -> NO VERSION BUMP
RUNNER_FAIL          -> NO MERKLE PROMOTION
RUNNER_FAIL          -> WORKFLOW FAIL
LEDGER_VERIFY_FAIL   -> NO POINTER BIND
POINTER_NOT_ON_CHAIN -> NULL / UNAVAILABLE
PUSH_FAIL            -> DURABILITY NOT CLAIMED
REPLAY_SUCCESS       != FACT_TRUE
RECEIPT              != VERDICT
AUTHORITY_CREATED    = FALSE
```

## Concurrency boundary

The workflow serializes global-ledger mutation per Git ref with `cancel-in-progress: false`. This prevents two same-ref runs from intentionally racing the append-only tip. A failed/non-fast-forward push still leaves the workflow red; no durable receipt is claimed until GitHub accepts the commit.

## Timeout boundary

The terminal execution receipt is still a post-run step. Whole-job timeout, workflow cancellation, or runner-host loss may prevent the terminal receipt from being written. The future hardening path remains a two-phase durable `STARTED -> TERMINAL` receipt or an external watcher.
