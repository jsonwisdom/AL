# Settlement Replay Protocol v0.1

**SPEC_ID:** `SETTLEMENT_REPLAY_PROTOCOL_V0_1`

## ROOT INVARIANT

Replay without consequence is theater.  
Replay with consequence is settlement.

Economic finality is the moment replay becomes binding.

## SOURCE_LINE

Once determinism is demonstrated, replay must control:

- value
- access
- deployment
- slashing
- reputation

This is the economic physics of Replay Chess.

---

## PURPOSE

Define the constitutional mechanics for:

- replay-triggered settlement
- state transitions with economic consequence
- slashing semantics
- machine-speed enforcement
- convergence-backed value movement

This protocol turns replay into economic truth.

---

## SETTLEMENT_OBJECT

A valid settlement declaration must include:

- `settlement_id`
- `bundle_id`
- `claim_set`
- `economic_effects`
- `replay_manifest`
- `challenge_window`
- `settlement_ruleset`
- `settlement_hash`

Missing any → `NON_ADMISSIBLE`.

---

## ECONOMIC_EFFECTS

A settlement may control:

- value transfer
- access rights
- deployment authorization
- revocation or slashing
- reputation adjustment
- contract activation
- contract termination

All effects must be:

- deterministic
- replay-derivable
- challenge-exposed
- environment-sealed

---

## SETTLEMENT TIERS

### S0 — Informational

Replay produces no economic effect.

### S1 — Soft Reputation

Replay adjusts reputational weight only.

### S2 — Access Control

Replay grants or revokes access.

### S3 — Deployment Control

Replay authorizes or blocks deployment.

### S4 — Economic Transfer

Replay moves value.

### S5 — Slashing / Finality

Replay destroys value, reputation, or authority.

S5 is the constitutional maximum.

---

## REPLAY REQUIREMENTS

Settlement replay must:

- reconstruct canonical state
- execute verifier spec
- validate environment
- run cross-implementation replay
- classify divergence
- produce convergence proof

If any step fails → `SETTLEMENT_INVALID`.

---

## CHALLENGE MODEL

A settlement enters check when:

- any adversary challenges
- any verifier diverges
- any environment mismatch occurs

A settlement is checkmated when:

- replay diverges
- canonical state fails
- verifier spec missing
- environment invalid
- challenge upheld

Checkmate voids the settlement.

---

## SLASHING SEMANTICS

Slashing must be:

- deterministic
- replay-provable
- challenge-exposed
- irreversible after convergence

Slashing cannot be:

- discretionary
- narrative-based
- platform-declared

Slashing is mathematical punishment, not social punishment.

---

## MACHINE-SPEED ENFORCEMENT

Once:

- challenge window closes
- replay converges
- settlement is admissible

Then enforcement must be:

- automatic
- irreversible
- environment-sealed
- implementation-consistent

This is economic finality.

---

## SETTLEMENT HASH

Compute:

```text
settlement_hash = SHA256(canonical_settlement_bytes)
```

This is the portable identity of the settlement.

---

## INVALID SETTLEMENT CONDITIONS

Settlement is invalid if:

- receipts invalid
- bundle invalid
- replay diverges
- environment drift
- canonicalization drift
- challenge upheld
- slashing rules violated

Invalid settlement → no economic effect.

---

## WIN CONDITION

Goodies win when replay controls consequence.  
Goobers lose when narrative cannot move value.

---

## FINAL RULE

Replay is not legitimate until it controls settlement.  
Settlement is not legitimate unless it survives replay.

**Proof over narrative.**
