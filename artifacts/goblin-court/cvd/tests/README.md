# CVD Test Gate

Expected harness coverage:

- each input path lands in the correct `failure_state`;
- every failure state has an explicit `recovery_condition`;
- non-F005 debounce behavior is tested;
- minimum transition interval is tested;
- F005 immediate path is tested without claiming real HSM revocation;
- stale, unreachable, mismatch, rollback, and equivocation remain distinct;
- state oscillation becomes first-class in v1.1.

`TESTS_OBSERVED` remains false until output from the bound commit is available.
