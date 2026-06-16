# EPOCH 02 — Epoch Boundary Rules v1

## Purpose

Define the constitutional rules governing epoch boundaries in Epoch 02.

Core separation:

- `EPOCH_BOUNDARY != CONTINUITY_BY_DEFAULT`
- `EPOCH_BOUNDARY = EXPLICIT_STATE_TRANSITION`

Nothing crosses epochs unless explicitly declared admissible.
No authority, quorum, or runtime state carries forward by implication.

Epochs open from commitments, not from live state.

---

## 1. Epoch Boundary Definition

An epoch boundary is the constitutional cut between:

- `epoch_n`: closed, replay-sealed
- `epoch_n+1`: new, explicitly declared

At the boundary:

- hard commitments may carry forward
- soft / executable state must die
- no implicit continuity is allowed

---

## 2. State That May Carry Forward

Only the following hard commitments may cross an epoch boundary:

```text
prior_epoch_number
prior_epoch_closure_hash
prior_kernel_hash
prior_schema_hash
prior_operator_set_hash
prior_evidence_root
prior_anchor_hashes
```

### 2.1 `prior_epoch_number`

Monotonic reference to the immediately preceding epoch.

### 2.2 `prior_epoch_closure_hash`

Hash committing to the final, replay-validated closure state of the prior epoch.

### 2.3 `prior_kernel_hash` / `prior_schema_hash` / `prior_operator_set_hash`

Historical commitments only; no executable authority.

### 2.4 `prior_evidence_root`

Final `evidence_root` of the prior epoch.

### 2.5 `prior_anchor_hashes`

Set of `anchor_hash` values for final attestations in the prior epoch.

No other state is admissible across the boundary.

---

## 3. State That Must Die at Boundary

The following must not cross epochs:

- operator authority: must be redeclared via new operator set
- observer participation
- quorum membership
- temporary exclusions
- runtime cache
- partial replay state
- unfinalized attestations
- interpretive notes
- environment assumptions

Any attempt to carry these forward is constitutionally void.

---

## 4. Required Predicates for Opening a New Epoch

A new epoch `epoch_n+1` may open only if all predicates hold:

```text
previous_epoch.finality == TRUE
previous_epoch_closure_hash == REPLAY_MATCH
new_epoch.kernel_hash == DECLARED
new_epoch.schema_hash == DECLARED
new_epoch.operator_set_hash == DECLARED
new_epoch.surface_version == DECLARED
```

### 4.1 `previous_epoch.finality`

The prior epoch must be replay-closed.

### 4.2 `previous_epoch_closure_hash`

Replay must recompute and match the declared closure hash.

### 4.3 New Epoch Declarations

Kernel, schema, operator set, and surface version must be explicitly declared and hash-anchored.

No epoch may open from an unresolved or replay-divergent predecessor.

---

## 5. Epoch Closure Hash

The `epoch_closure_hash` is defined as:

```text
epoch_closure_hash = sha256(canonical_epoch_closure_bytes)
```

Where `canonical_epoch_closure_bytes` commit to:

- epoch number
- final `evidence_root`
- final `operator_set_hash`
- final `kernel_hash`
- final `schema_hash`
- final `anchor_hash` set

Canonicalization MUST use JCS / RFC 8785.
Replay MUST be able to reconstruct `epoch_closure_hash` exactly.

If mismatch:

```text
EPOCH_CLOSURE_MISMATCH -> HALT
```

---

## 6. No Implicit Continuity

Explicit invariant:

```text
No authority, quorum, or runtime state carries forward by implication.
```

Consequences:

- operators must be re-authorized via new operator set
- observers must be re-admitted under new epoch rules
- quorum must be recomputed from scratch
- exclusions do not auto-propagate
- caches and partial computations are irrelevant

Epochs are discrete constitutional intervals, not a continuous runtime.

---

## 7. Epoch Opening From Commitments

Most important clause:

```text
An epoch opens from commitments, not from live state.
```

New epoch initialization uses only:

- `prior_epoch_closure_hash`
- `prior_kernel_hash`
- `prior_schema_hash`
- `prior_operator_set_hash`
- `prior_evidence_root`
- `prior_anchor_hashes`

No live process, in-memory state, or operator decision may define the new epoch.

---

## 8. Invalid Boundary Classifications

Replay MUST classify boundary violations as:

- `EPOCH_PREVIOUS_NOT_FINAL`
- `EPOCH_CLOSURE_MISMATCH`
- `EPOCH_KERNEL_UNDECLARED`
- `EPOCH_SCHEMA_UNDECLARED`
- `EPOCH_OPERATOR_SET_UNDECLARED`
- `EPOCH_SURFACE_VERSION_UNDECLARED`
- `EPOCH_IMPLICIT_STATE_LEAK`

Any such violation prevents the new epoch from being constitutionally recognized.

---

## 9. Closure Property

This file defines the complete epoch boundary rules for Epoch 02.

No additional:

- cross-epoch state
- implicit continuity
- boundary semantics

may be introduced at runtime.

Any unclassified cross-epoch behavior defaults to:

```text
EPOCH_BOUNDARY_VIOLATION -> HALT
```

Fail closed, never open.
