# Convergence Report Template

A deterministic replay transcript for heterogeneous interpreter verification.

<!-- replay-matrix trigger: 2026-05-17T01:24:00Z -->

## 1. Execution Context

- Workflow: `replay-matrix.yaml`
- Test Harness: `eval-receipt-adapter/test_matrix.py`
- Canonicalizer: pure-Python JCS-aligned canonicalizer with NFC normalization
- Registry: `eval-receipt-adapter/examples/expected_root.json`
- Runners: GitHub Actions `ubuntu-latest`
- Python Versions: `3.10`, `3.11`, `3.12`
- Commit SHA: `<commit-sha>`
- GitHub Actions Run ID: `<run-id>`
- Timestamp: `<utc-timestamp>`

## 2. Fixture Set Under Test

| Fixture ID | Path | Expected Root | Canonicalization Regime | Classification |
|---|---|---|---|---|
| `AFP_MINIMAL_001` | `eval-receipt-adapter/examples/fixtures/fixture_001.json` | `<sha256>` | `JCS_V1` | `CONVERGED` |
| `AFP_NESTED_002` | `eval-receipt-adapter/examples/fixtures/fixture_002.json` | `<sha256>` | `JCS_V1` | `CONVERGED` |

## 3. Interpreter Convergence Matrix

| Python Version | AFP_MINIMAL_001 | AFP_NESTED_002 | Verdict |
|---|---|---|---|
| 3.10 | `<MATCHED/DRIFT>` | `<MATCHED/DRIFT>` | `<PASS/FAIL>` |
| 3.11 | `<MATCHED/DRIFT>` | `<MATCHED/DRIFT>` | `<PASS/FAIL>` |
| 3.12 | `<MATCHED/DRIFT>` | `<MATCHED/DRIFT>` | `<PASS/FAIL>` |

Matrix Verdict: `<REPLAY_CONFIRMED / REPLAY_DIVERGED / REPLAY_INDETERMINATE>`

## 4. Canonicalization Stability Evidence

Record for each interpreter and fixture:

- canonical string length
- SHA-256 root
- Unicode normalization mode
- ordering behavior

Example:

```text
Interpreter: Python 3.12.x
Fixture: AFP_NESTED_002
Canonical Length: <bytes>
SHA-256 Root: <sha256>
Normalization: NFC
Ordering: Lexicographic object-key ordering; array order preserved
```

## 5. Drift Analysis

If a failure occurs, classify it:

- Normalization Drift
- Serialization Drift
- Ordering Drift
- Numeric Encoding Drift
- Interpreter-Specific Behavior
- Fixture Registry Mismatch
- Environment Failure

Each drift entry should include:

- observed hash
- expected hash
- interpreter version
- fixture ID
- reproduction command
- canonical diff, where practical

## 6. Replay Court Verdict

One of:

- `REPLAY_CONFIRMED` — all interpreters converged
- `REPLAY_DIVERGED` — at least one interpreter drifted
- `REPLAY_INDETERMINATE` — environment or runner failure prevented a valid verdict

## 7. Immutable Log Reference

Include:

- GitHub Actions run URL
- run ID
- commit SHA
- timestamp
- artifact links, if any

## Scope Note

This template records observed replay convergence for the adapter fixture suite. It does not claim universal replay safety across all production data, all numeric domains, or all model execution surfaces.
