# REPLAY_TRACE_CLOSURE_INVARIANT_V1

## Status

`REPLAY_TRACE_CLOSURE_INVARIANT_V1_OPENED`

---

## Statement

For every invocation of replay, the system MUST terminate only after emitting exactly one terminal `TRACE_CLOSED` event.

A verdict without `TRACE_CLOSED` is constitutionally void.

---

## Scope

This invariant applies to all exit paths, including:

- `PASS`
- `FAIL`
- `INDETERMINATE`
- `TAINTED`
- `REVIEW_REQUIRED`
- `HIGH_RISK_VARIANT`
- malformed input
- schema failure
- provenance failure
- undeclared transform
- digest mismatch
- receipt mismatch
- internal exception
- early validation return

No replay path may emit a public CVD opinion without trace closure.

---

## Mandatory Behavior

1. Replay MUST execute inside a court-session closure boundary.
2. `finalize_verdict()` MUST run for every replay invocation.
3. `finalize_verdict()` is the sole function authorized to append `TRACE_CLOSED`.
4. `TRACE_CLOSED` MUST be the final entry in the transcript.
5. After `TRACE_CLOSED`, the transcript MUST be sealed and immutable.
6. A CVD output object MAY be returned only after the session closure completes.
7. Report emission MUST abort if `TRACE_CLOSED` is absent.

---

## Terminal Event Structure

A terminal closure event MUST include:

```json
{
  "name": "TRACE_CLOSED",
  "status": "PASS|FAIL|INDETERMINATE|TAINTED|REVIEW_REQUIRED|HIGH_RISK_VARIANT|ERROR",
  "verdict": "PASS|FAIL|INDETERMINATE|TAINTED|REVIEW_REQUIRED|HIGH_RISK_VARIANT|ERROR",
  "reason_code": "deterministic enum from ALMS kernel taxonomy",
  "trace_hash": "sha256:<hex>",
  "closed_at": "ISO-8601 timestamp",
  "kernel_version": "v0.1"
}
```

The trace hash MUST be computed over the complete transcript with the terminal event's own `trace_hash` field set to `null` before hashing.

Self-referential trace hashing is forbidden.

---

## Implementation Guarantee

Reference implementations SHOULD use a single replay-session closure path:

```text
open court session
  validate schema
  validate provenance
  validate transform policy
  recompute digest
  verify receipt
  classify verdict
finally
  finalize_verdict()
  seal transcript
emit CVD output only after sealed
```

No public report emitter may accept an unsealed replay state.

---

## Regression Prevention

CI SHOULD fail if:

- any test vector emits a report without terminal `TRACE_CLOSED`,
- more than one `TRACE_CLOSED` event exists,
- `TRACE_CLOSED` is not the final trace event,
- `TRACE_CLOSED.trace_hash` is missing,
- the transcript mutates after closure,
- public report emission occurs before closure,
- PASS is emitted without digest recomputation,
- any code path bypasses the session closure boundary.

---

## Constitutional Rule

No trace, no opinion.

A replay court that exits without closing the record has not issued a valid opinion.

Verify > narrative.
