# Replay Receipt Specification v0.1

**SPEC_ID:** `REPLAY_RECEIPT_SPEC_V0_1`

## ROOT_INVARIANT

Truth is what survives hostile recomputation.  
A receipt is the portable proof that a claim can be replayed.

## SOURCE_LINE

No receipt → no admissible move.  
No replay path → no legitimacy.  
No challenge rights → no authority.

## PURPOSE

Define the canonical receipt object required for any Goodie move in Replay Chess and ALMS-aligned systems.

A receipt is the minimum portable evidence that binds:

- a claim,
- to a state transition,
- to a replay path,
- under hostile challenge.

---

## RECEIPT_OBJECT

A valid receipt must contain:

- `receipt_id`
- `claim_id`
- `actor`
- `timestamp`
- `blast_radius`
- `artifact_hash`
- `canonical_form`
- `replay_path`
- `verifier_spec_ref`
- `challenge_rights`
- `environment_bindings`
- `signature_or_commitment`

A receipt missing any required field is non-admissible.

---

## CANONICALIZATION_RULES

To prevent narrative drift:

1. UTF-8 encoding only
2. Deterministic key ordering (lexicographic)
3. No whitespace significance
4. No implicit defaults
5. Hash computed over canonical bytes only

This ensures replay-stable identity across implementations.

---

## RECEIPT_HASHING

The receipt must include:

- `artifact_hash = SHA256(canonical_artifact_bytes)`
- `receipt_hash = SHA256(canonical_receipt_bytes)`

The receipt hash is the portable identity of the move.

---

## REPLAY_REQUIREMENTS

A receipt is replay-valid only if:

- the referenced artifact exists
- the canonical form reconstructs
- the replay path is executable
- the verifier spec is available
- environment bindings are declared
- challenge rights are enforceable

If any condition fails → receipt is invalid.

---

## CHALLENGE_MODEL

A receipt must expose:

- who may challenge
- how challenges are executed
- what constitutes divergence
- what constitutes convergence
- how results are published

A receipt without challenge rights is authority theater.

---

## BLAST_RADIUS_ALIGNMENT

Receipt requirements scale with consequence:

- L0-L1 → minimal receipts
- L2-L3 → canonical artifacts + provenance
- L4-L5 → full replay contract + environment bindings

A receipt must match or exceed the claim’s blast radius.

---

## INVALID_RECEIPT_CONDITIONS

A receipt is invalid if:

- missing required fields
- hash mismatch
- canonicalization fails
- replay path missing
- verifier spec missing
- environment undefined
- challenge rights absent
- replay diverges

Invalid receipts cannot anchor legitimacy.

---

## CHECK_CONDITION

A receipt enters check when an adversary requests replay.

## CHECKMATE_CONDITION

A receipt is checkmated when:

- canonical state cannot be reconstructed
- replay path fails
- verifier spec absent
- environment mismatch
- replay diverges

Checkmate is mechanical, not rhetorical.

---

## WIN_CONDITION

Goodies win when receipts produce replay-stable legitimacy.  
Goobers lose when receipts fail to recompute.

---

## FINAL_RULE

A move without a receipt is not a move.  
A receipt without replay is not legitimacy.

**Proof over narrative.**
