# BUILD_MATRIX.md — constitutional-replay-v1

Receipt-first mapping. Local replay sovereign.

```text
No witness, no claim.
No receipt, no ratification.
No replay, no settlement.
```

AL doctrine preserved. Module contained. v0.1 local-first only.

## Module Law

Inherited from AL and `alms-core`:

- Bytes in. Verdicts out.
- No network, no live clock, no entropy.
- No anchor until tests are green and golden vectors are independently reproduced.
- Canonicalize with Unicode NFC, recursive normalization, sorted keys, compact JSON, UTF-8, and floats forbidden.
- Hash with `sha256:` over canonical bytes.
- Policy uses a decision-table pattern: `required_inputs`, `allowed_actions`, `blocked_actions`, `limits`, and monotonicity.
- Interpreter produces a deterministic outcome: approval or refusal.
- Replay must reproduce the original verdict exactly.

## Root Files

### `README.md`

Purpose: Module declaration and execution contract.

Invariant:

- Local-first.
- CLI sovereign.
- Static dashboard only.

Failure states:

- Any Base RPC requirement in v0.1.
- Missing refusal enum.
- README claims hosted authority.

Base path:

- v0.2 may add a Base witness pointer only.
- Base does not ratify meaning.

### `DESIGN.md`

Purpose: Formal constitutional replay spec.

Invariant:

- Receipt binding is exact.
- Local replay proves meaning.
- Summary supports filtering; full receipt supports replay.

Failure states:

- Non-deterministic paths.
- Keccak used as canonical replay hash.
- Free-text refusal reasons.

### `CONTRIBUTING.md`

Purpose: Receipt-gated contribution rules.

Invariant:

- Every PR that changes executable logic must update golden vectors and provide replay proof.

Failure states:

- Untested logic changes.
- Broken historical replay.
- Missing migration receipt for semantic changes.

## `src/`

### `src/canonicalize.ts`

Rule:

- Unicode NFC normalization.
- Recursive normalization.
- Forbid floats.
- Sort keys lexicographically.
- Compact JSON serialization.
- UTF-8 bytes.

Failure states:

- `CANONICALIZATION_ERROR`
- `DIVERGENT_REPLAY`

### `src/hash.ts`

Rule:

```text
sha256:<hex(canonical_bytes)>
```

Failure states:

- `HASH_MISMATCH`

Canonical replay hashes must use the `sha256:` prefix.

### `src/policy.ts`

Rule:

- Policies must declare `required_inputs`, `allowed_actions`, `blocked_actions`, `limits`, and `refusal_codes`.

Failure states:

- `POLICY_UNAVAILABLE`
- `POLICY_HASH_MISMATCH`
- `POLICY_SCHEMA_VIOLATION`

### `src/interpreter.ts`

Rule:

- Deterministic verdict.
- Monotonic decision logic.
- No free-text refusal reasons.

Failure states:

- `INTERPRETER_HASH_MISMATCH`
- `UNHANDLED_REFUSAL`
- `UNKNOWN_ACTION`

### `src/receipt.ts`

Rule:

Every full receipt must bind:

```json
{
  "receipt_version": "receipt.v1",
  "policy_hash": "sha256:...",
  "policy_version": "policy.v1",
  "interpreter_hash": "sha256:...",
  "replay_engine_version": "replay.v1",
  "refusal_code": "SPEND_LIMIT_EXCEEDED | null",
  "action": "...",
  "context_hash": "sha256:..."
}
```

Failure states:

- `MISSING_BINDING`
- `INVALID_SIGNATURE`
- `INVALID_RECEIPT_SCHEMA`

### `src/replay.ts`

Rule:

- Sequential replay of receipts must reproduce exact original outcome.
- Replay performs no network calls.
- Replay uses no live clock.
- Replay uses no entropy.

Failure states:

- `REPLAY_DIVERGENCE`
- `RECEIPT_REJECTED`
- `POLICY_UNAVAILABLE`
- `INTERPRETER_HASH_MISMATCH`

### `src/batch.ts`

Rule:

- Batch root must cover exact receipt hashes.
- Summary is not replay authority.

Failure states:

- `BATCH_ROOT_MISMATCH`
- `RECEIPT_HASH_MISSING`

## v0.1 Hard Constraints

- No Base RPC.
- No live clock in replay.
- No floats.
- No random IDs.
- No free-text refusals.
- `sha256:` prefix only for canonical replay hashes.
- Golden vectors before any anchor.
- Static dashboard only.
- No hosted explorer.
- No reputation score.

## No-Drift Rules

1. Change requires a new policy or interpreter hash when semantics change.
2. `replayReceipt()` must succeed on all historical valid receipts.
3. Canonicalization must be byte-identical on every run.
4. `demo.sh` must pass end-to-end.
5. Dashboard must render only local data.
6. Base may witness commitment later, but Base does not decide meaning.

## Five-Level Game of Building with Jay

### Level 1 — Module Anchor

PASS:

- `README.md`, `DESIGN.md`, `CONTRIBUTING.md`, and `BUILD_MATRIX.md` exist under `constitutional-replay-v1/`.

FAIL:

- Files placed at AL root.
- Files placed in `COMPUTERWISDOM`.
- Files duplicated across repos.

### Level 2 — Canonical Bytes

PASS:

- `canonicalize.ts` and `hash.ts` mirror ALMS Core behavior.

FAIL:

- Floats accepted.
- Keys unsorted.
- No `sha256:` prefix.

### Level 3 — Refusal Interpreter

PASS:

- All refusal enum vectors pass.

FAIL:

- Unhandled refusal.
- Free-text reason.
- Non-deterministic policy outcome.

### Level 4 — Sovereign Replay

PASS:

- `refusal-001.json` replays with no network, no live clock, and no entropy.

FAIL:

- Replay requires Base RPC.
- Replay requires hosted service.

### Level 5 — Base Witness Readiness

PASS DOCS-ONLY:

- Base witness plan exists after local vectors pass.

FAIL:

- Base claimed as ratifier.
- Anchor attempted before green vectors.

## Final Status

This `BUILD_MATRIX.md` is the receipt map for `constitutional-replay-v1` v0.1.

All future changes must reference it.
