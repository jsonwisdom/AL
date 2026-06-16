# Adversarial Challenge Protocol v0.1

**SPEC_ID:** `ADVERSARIAL_CHALLENGE_PROTOCOL_V0_1`

## ROOT INVARIANT

Truth is what survives hostile recomputation.  
Authority is what survives hostile challenge.

Everything else is theater.

## SOURCE_LINE

Receipts prove moves.  
Bundles prove systems.  
Challenges prove legitimacy.

---

## PURPOSE

Define the constitutional mechanics for:

- challenge execution
- verifier assignment
- convergence adjudication
- divergence classification
- replay escalation
- institutional dispute resolution

This protocol is the warfare layer of Replay Chess.

---

## CHALLENGE_OBJECT

A valid challenge must declare:

- `challenge_id`
- `challenger`
- `target_receipt_or_bundle`
- `challenge_basis`
- `expected_failure_mode`
- `challenge_window`
- `verifier_assignment`
- `replay_parameters`

A malformed challenge is non-admissible.

---

## CHALLENGE BASIS

A challenge may assert:

- receipt invalidity
- canonicalization mismatch
- state reconstruction failure
- verifier spec absence
- environment mismatch
- replay divergence
- bundle graph inconsistency
- provenance corruption

These are the legitimate grounds for adversarial action.

---

## VERIFIER ASSIGNMENT

A challenge must be evaluated by:

- ≥ 2 independent replay implementations
- ≥ 1 adversarial verifier
- ≥ 1 neutral verifier

Assignment rules:

1. Challenger cannot be sole verifier.
2. Actor cannot self-verify.
3. Platform cannot be trust root.
4. Verifier spec must be canonical and public.

This prevents authority laundering.

---

## REPLAY EXECUTION

Replay must be executed under:

- canonical state
- declared inputs
- declared outputs
- declared environment
- declared bindings
- declared manifest

Replay must be deterministic, hostile-ready, and implementation-diverse.

---

## CONVERGENCE ADJUDICATION

Let:

- `R_i` = replay result from implementation `i`
- `H(R_i)` = canonical hash of result

### Convergence

If all `H(R_i)` match → `CONVERGENT`.

### Divergence

If any mismatch → `DIVERGENT`.

### Non-Admissible

If replay cannot execute → `NON_ADMISSIBLE`.

---

## DIVERGENCE CLASSIFICATION

If divergent, classify:

- `E1` — Canonicalization Divergence
- `E2` — State Reconstruction Divergence
- `E3` — Verifier Spec Divergence
- `E4` — Environment Divergence
- `E5` — Implementation Divergence
- `E6` — Malicious Divergence

This creates forensic replay trails.

---

## ESCALATION PATHS

If divergence persists:

1. Re-canonicalization
2. Verifier expansion
3. Environment sealing
4. Cross-bundle replay
5. Institutional arbitration
6. Settlement replay (L5 only)

Escalation is constitutional, not discretionary.

---

## OUTCOMES

A challenge returns:

- `UPHELD` — challenge correct → target illegitimate
- `REJECTED` — challenge incorrect → target legitimate
- `INCONCLUSIVE` — environment or spec incomplete

---

## CHECK CONDITION

A receipt or bundle enters check when a valid challenge is filed.

## CHECKMATE CONDITION

Checkmate occurs when:

- replay diverges
- canonical state fails
- verifier spec missing
- environment mismatch
- bundle graph invalid
- challenge upheld

Checkmate is mechanical, not rhetorical.

---

## WIN CONDITION

Goodies win when challenges strengthen legitimacy.  
Goobers lose when challenges collapse narrative.

---

## FINAL RULE

A system without adversarial challenge is theater.  
A system with adversarial challenge is truth-bearing.

**Proof over narrative.**
