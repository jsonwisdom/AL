# CVD Failure-State Matrix Gate

The authoritative matrix must define, at minimum:

```text
NORMAL
ALARM
DEGRADED
CRITICAL
F001_ORACLE_UNREACHABLE
F002_ATTESTATION_STALE
F003_DIGEST_MISMATCH
F004_ROLLBACK_DETECTED
F005_REPLAY_OR_FORGERY
F006_STATE_OSCILLATION (v1.1)
```

Each row must bind trigger, severity, enforcement scope, recovery condition, receipt emitted, and human-authorization boundary.

`MATRIX_IMPLEMENTED` remains false until a machine-readable matrix and matching tests are committed.
