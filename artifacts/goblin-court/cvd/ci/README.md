# CVD CI Gate

A future workflow must:

1. check out the exact PR commit;
2. install the pinned Rust toolchain;
3. run formatting and lint checks;
4. run `cargo test --test harness`;
5. publish machine-readable test receipts;
6. expose the workflow run ID, job IDs, commit SHA, and final conclusion.

A workflow file alone does not establish green status.

```text
CI_CONFIG_PRESENT = FALSE
CI_RUN_OBSERVED   = FALSE
PROVISIONAL       = LOCKED
T                 = 0
```
