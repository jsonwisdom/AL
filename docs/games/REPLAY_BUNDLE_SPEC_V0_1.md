# Replay Bundle Specification v0.1

**SPEC_ID:** `REPLAY_BUNDLE_SPEC_V0_1`

## ROOT INVARIANT

A single receipt proves a move.  
A bundle proves a system.

Truth is what survives multi-receipt hostile recomputation.

Everything else is theater.

---

## PURPOSE

Define the canonical container for:

- receipt aggregation
- multi-claim legitimacy
- cross-receipt convergence
- institutional replay packages
- adversarial challenge surfaces

A Replay Bundle is the constitutional unit of institutional-scale truth.

---

## BUNDLE_OBJECT

A valid Replay Bundle must contain:

- `bundle_id`
- `bundle_version`
- `receipt_set` (≥ 1)
- `claim_graph`
- `canonical_order`
- `replay_manifest`
- `challenge_surface`
- `environment_profile`
- `bundle_hash`

A bundle missing any required field is non-admissible.

---

## RECEIPT_SET

A bundle aggregates receipts that share:

- a common replay domain, or
- a shared legitimacy dependency, or
- a cross-claim convergence requirement.

Each receipt must be:

- canonical
- hash-stable
- replay-valid
- challenge-exposed

Invalid receipts → invalid bundle.

---

## CLAIM_GRAPH

Bundles must encode the directed acyclic graph of:

- claims
- dependencies
- transitions
- replay paths

This prevents narrative insertion, deletion, or reordering.

Graph invariants:

- no cycles
- no orphan claims
- no implicit edges
- no undeclared dependencies

The claim graph is the semantic topology of the bundle.

---

## CANONICAL ORDER

Bundles must define a deterministic ordering:

1. lexicographic `receipt_id`
2. lexicographic `claim_id`
3. topological `claim_graph` order

This ensures replay-stable identity across implementations.

---

## REPLAY_MANIFEST

The manifest declares:

- replay implementations
- verifier specs
- environment bindings
- required artifacts
- expected outputs
- convergence criteria

This is the execution contract for the bundle.

---

## CHALLENGE_SURFACE

A bundle must expose:

- challenge rights
- challenge methods
- challenge windows
- divergence reporting
- convergence proofs

A bundle without challenge rights is institutional theater.

---

## ENVIRONMENT_PROFILE

Bundles must declare:

- runtime assumptions
- environment variables
- external dependencies
- nondeterminism boundaries
- version constraints

This prevents environment-based falsification.

---

## BUNDLE_HASH

The bundle hash is computed over:

- canonical receipts
- canonical claim graph
- canonical manifest
- canonical environment profile

This is the portable identity of the bundle.

---

## ADMISSIBILITY RULES

A bundle is `NON_ADMISSIBLE` if:

- any receipt is invalid
- claim graph is malformed
- replay manifest incomplete
- environment profile missing
- canonicalization fails

---

## CHECK CONDITION

A bundle enters check when any adversary requests multi-receipt replay.

---

## CHECKMATE CONDITION

A bundle is checkmated when:

- cross-receipt replay diverges
- claim graph cannot reconstruct
- manifest cannot execute
- environment mismatch occurs
- convergence cannot be proven

Checkmate is mechanical, not rhetorical.

---

## WIN CONDITION

Goodies win when institutional legitimacy becomes reproducible.  
Goobers lose when institutional narrative cannot recompute.

---

## FINAL RULE

Receipts prove moves.  
Bundles prove systems.

**Proof over narrative.**
