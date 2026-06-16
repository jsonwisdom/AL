# Replay Chess Specification v0.1

**SPEC_ID:** `REPLAY_CHESS_SPEC_V0_1`

## ROOT_INVARIANT

Truth is what survives hostile recomputation.  
Everything else is theater.

## SOURCE_LINE

Oxford chess is the old board.  
Replay Chess is the new physics.

## PURPOSE

Convert public claims into replay-testable legitimacy objects.

Replay Chess is not a metaphor.  
It is a deterministic legitimacy engine.

---

## CLAIM_OBJECT

A claim must declare:

- `claim_id`
- `actor`
- `statement`
- `blast_radius`
- `receipt_requirement`
- `replay_path`
- `challenge_window`

A claim without these fields is non-admissible.

---

## BLAST_RADIUS_TIERS

### L0 — Casual

- hash + timestamp
- minimal falsification cost
- low-impact claims

### L1 — Public

- hash + timestamp + source link
- public visibility, low authority

### L2 — Reputational

- canonical artifact + hash + provenance
- falsification cost must exceed social impact

### L3 — Authority

- canonical state
- declared inputs
- observed outputs
- verifier specification
- adversarial recomputation required

### L4 — Institutional

- environment bindings
- challenge rights
- replay contract
- full adversarial replay surface

### L5 — Settlement

Replay result controls:

- money
- access
- deployment
- reputation

Falsification cost must exceed economic impact.

These tiers define receipt weight and replay burden.

---

## MOVE_VALIDITY

A Goodie move is valid only if:

- it emits a receipt
- the receipt binds to a claim
- the claim binds to a state transition
- the transition has a replay path
- the replay path is challengeable

If any link breaks, the move is invalid.

---

## CHECK

A claim enters check when a hostile observer requests replay.

This is the moment narrative collapses into computation.

---

## CHECKMATE

A claim is checkmated when:

- required receipts are missing
- replay path is unavailable
- canonical state cannot be reconstructed
- verifier spec is absent
- replay diverges

Checkmate is not rhetorical.  
It is mechanical divergence.

---

## WIN_CONDITION

- Goodies win when legitimacy becomes reproducible.
- Goobers lose when narrative cannot recompute.

Replay is the only arbiter.

---

## FINAL_RULE

Reputation is the adversarial cost of falsifying your past.

**Proof over narrative.**
