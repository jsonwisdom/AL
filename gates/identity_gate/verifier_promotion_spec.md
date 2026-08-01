# Verifier Promotion: PROPOSED → ACTIVE

## Version 1.0

## Purpose

Define evidence required to classify a verifier as mechanically reliable. `ACTIVE` does not confer authority.

## Required Criteria

All criteria must pass with non-placeholder evidence:

1. **Replayable** — canonical receipts replay successfully from pinned inputs.
2. **Deterministic** — repeated executions over identical bytes produce identical outputs.
3. **Auditable** — inputs, tool versions, outputs, and failures are recorded.
4. **Non-authoritative** — `authority_status` is explicitly `false`.
5. **Open gates documented** — unresolved gates remain visible.
6. **Dependency closure** — required dependencies are pinned, public or reproducibly obtainable, and license-compatible.
7. **Independent verification** — at least one replay is performed outside the proposing execution context.

## Process

1. Submit a proposed promotion record with evidence references.
2. CI validates structure and runs available tests.
3. Missing or skipped tests produce `PROPOSED`, not `ACTIVE`.
4. Passing CI produces `MECHANICAL_CHECKS_PASSED`.
5. Independent replay produces `ACTIVE_ELIGIBLE`.
6. A separately authorized, non-model transition may record `ACTIVE`.

## States

| State | Meaning |
|---|---|
| `PROPOSED` | Evidence incomplete or unevaluated |
| `MECHANICAL_CHECKS_PASSED` | Local automated checks passed |
| `ACTIVE_ELIGIBLE` | Independent replay also passed |
| `ACTIVE` | Separately authorized state transition recorded |
| `DISPUTED` | Evidence conflict or failed verification |

## Prohibition

CI output, a model statement, or a Git commit alone cannot create `ACTIVE`.
