# ALMS v0 Provenance

## Purpose

ALMS provenance is law over receipt graphs, not decorative metadata.

A receipt is admissible only when the receipt itself is locally valid and every reachable ancestor receipt is admissible under the same ALMS v0 rules.

## Core Invariant

For any receipt `R`:

```text
admissible(R) = verify_local(R).code == 0 AND all(admissible(P) for P in Parents(R))
```

Where `Parents(R)` is resolved from:

```json
{
  "provenance": {
    "parent_receipts": ["<sha256-of-parent-receipt>"],
    "parent_verification_mode": "FULL_RECURSIVE"
  }
}
```

`verify_local` means all ALMS v0 checks on `R` itself, ignoring parent receipts.

## Parent Verification Mode

Allowed values in ALMS v0:

```text
FULL_RECURSIVE
```

Any other value is rejected:

```json
{"verdict":"reject","code":5,"reason":"parent_verification_mode_unsupported"}
```

`FULL_RECURSIVE` means the verifier must be able to fetch every ancestor receipt by hash and re-run full verification over the entire reachable provenance DAG.

Cached green summaries are not sufficient.

## Missing Parent

If any parent hash cannot be resolved to a receipt, verification of the child fails:

```json
{"verdict":"reject","code":5,"reason":"parent_receipt_missing"}
```

Diagnostics on stderr SHOULD include:

```text
missing_parent_hash=<hash>
```

## Invalid Parent

If a parent receipt resolves but fails verification, verification of the child fails:

```json
{"verdict":"reject","code":5,"reason":"parent_receipt_invalid"}
```

Diagnostics on stderr MUST include:

```text
failing_parent_hash=<hash> parent_exit_code=<code> parent_reason=<reason>
```

Stdout remains the single JCS verdict line.

## Cycle Safety

No receipt is admissible if its provenance graph contains a cycle.

Verifier rule:

- Maintain a recursion stack keyed by `SHA256(JCS(receipt_full))`.
- If a parent hash already exists in the active recursion stack, reject.

Cycle verdict:

```json
{"verdict":"reject","code":5,"reason":"parent_receipt_cycle"}
```

Diagnostics on stderr SHOULD include:

```text
cycle_parent_hash=<hash>
```

## Deterministic First Failing Ancestor

When multiple parents exist, implementations must agree on the failing ancestor reported first.

Verifier rule:

- Sort `provenance.parent_receipts[]` lexicographically by hash.
- Verify parents in that order.
- The first parent whose verification does not return code `0` is the deterministic failing ancestor.

Child stdout:

```json
{"verdict":"reject","code":5,"reason":"parent_receipt_invalid"}
```

Child stderr:

```text
failing_parent_hash=<hash> parent_exit_code=<code> parent_reason=<reason>
```

## A -> B -> C Conformance Pattern

### Node A: valid root

- `provenance.parent_receipts = []`
- `parent_verification_mode = FULL_RECURSIVE`
- Direct verification exits `0`.

### Node B: invalid constitution

- `provenance.parent_receipts = [h_A]`
- All local checks pass until policy binding.
- `policy.constitution_hash` is wrong or unknown.
- Direct verification exits `3`.

Expected stdout:

```json
{"verdict":"reject","code":3,"reason":"constitution_mismatch"}
```

### Node C: locally valid leaf with invalid parent

- `provenance.parent_receipts = [h_B]`
- Local verification of C passes.
- Recursive parent verification resolves B.
- B fails with `constitution_mismatch`.

Expected stdout for C:

```json
{"verdict":"reject","code":5,"reason":"parent_receipt_invalid"}
```

Expected stderr for C:

```text
failing_parent_hash=<h_B> parent_exit_code=3 parent_reason=constitution_mismatch
```

## Exit Code 5 Provenance Reasons

ALMS v0 provenance failures use exit code `5` with one of these reasons:

```text
parent_receipt_missing
parent_receipt_invalid
parent_receipt_cycle
parent_verification_mode_unsupported
```

## Security Meaning

A clean child cannot launder a poisoned parent.

A receipt with valid schema, signature, typing, determinism, and local policy still fails if any ancestor is missing, invalid, cyclic, or not recursively verifiable.

Provenance is a hard dependency.

## Recommended Conformance Directory

```text
alms-v0-conformance/v5_provenance/
```

Recommended fixture names:

```text
A_valid_root.json
B_invalid_constitution_child.json
C_valid_leaf_invalid_parent.json
```
