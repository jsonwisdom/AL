# Replay Node v0.1 — Membrane Test

Status: PR #260-bounded membrane verification
Authority: false
Merge permission: false

## 1. Objective

Prove that the operator layer cannot mutate runtime semantics.

Every operator-layer claim must map directly to a runtime step, runtime scope item, fail-closed condition, or receipt field.

## 2. Claim Mapping Table

| Operator Claim | Runtime Anchor | Result |
|---|---|---|
| fetches one official public PDF URL | runtime_spec.md Section 2 item 1 | PASS |
| computes PDF SHA256 | runtime_spec.md Section 2 item 2 | PASS |
| identity gate by expected date plus proceedings/minutes text | runtime_spec.md Section 2 item 3 | PASS |
| extracts text with `pdftotext -layout` | runtime_spec.md Section 2 item 4 | PASS |
| computes extracted text SHA256 | runtime_spec.md Section 2 item 5 | PASS |
| emits deterministic rows | runtime_spec.md Section 2 item 6 | PASS |
| computes output CSV SHA256 | runtime_spec.md Section 2 item 7 | PASS |
| compares output CSV SHA256 to claimed CSV SHA256 | runtime_spec.md Section 2 item 8 | PASS |
| emits receipt JSON only on MATCH | runtime_spec.md Section 2 item 9 | PASS |
| fails closed on dependency mismatch | runtime_spec.md Section 2 item 10 | PASS |
| fails closed on identity mismatch | runtime_spec.md Section 2 item 11 | PASS |
| fails closed on output hash mismatch | runtime_spec.md Section 2 item 12 | PASS |
| authority remains false | runtime_spec.md Section 2 item 13 | PASS |
| merge_permission remains false | runtime_spec.md Section 2 item 14 | PASS |

## 3. Explicit Scope Rejection

The following claims are rejected because they are not part of the PR #260-bounded runtime:

- CSV source ingestion
- crawler behavior
- daily ingestion
- timeout guarantees
- size guarantees
- debug flags
- soft failure continuation
- merge authority assignment
- institutional certification

## 4. Membrane Result

PASS.

No narrative mutation detected.

## 5. Enforcement Rule

PR body claims must match diff surface.

Any future PR that changes the operator brief must preserve runtime anchoring for every operator-layer claim.
