# Replay Identity Graph Specification v0.1

**SPEC_ID:** `REPLAY_IDENTITY_GRAPH_SPEC_V0_1`

## ROOT INVARIANT

Identity is not a name.  
Identity is a replay-verifiable lineage.

Everything else is theater.

## SOURCE_LINE

Once memory exists, identity must be:

- replay-bound
- lineage-preserving
- challenge-exposed
- supersession-aware
- falsification-cost-indexed

This is the identity layer of Replay Chess.

---

## PURPOSE

Define the constitutional mechanics for:

- identity continuity
- cross-receipt actor lineage
- verifier reputation topology
- trustless identity linkage
- replay-bound reputation graphs

Identity becomes a graph, not a string.

---

## IDENTITY_OBJECT

A valid identity object must declare:

- `identity_id`
- `public_keys` (≥1)
- `key_history`
- `receipt_history`
- `supersession_history`
- `challenge_history`
- `reputation_vector`
- `identity_hash`

Missing any → `NON_ADMISSIBLE`.

---

## IDENTITY GRAPH

The identity graph is a directed acyclic graph where:

- nodes = identity states
- edges = supersession events
- receipts = evidence
- challenges = adversarial tests
- reputation = falsification cost

Identity is append-only, never rewritten.

---

## KEY CONTINUITY

Identity continuity requires:

- key rotation lineage
- key supersession proofs
- key revocation receipts
- key-to-actor binding receipts

A key without lineage → orphaned identity.

---

## REPUTATION VECTOR

Reputation is computed as:

- cumulative falsification cost
- challenge survival rate
- settlement impact
- bundle participation
- supersession correctness
- divergence avoidance

Reputation is mathematical, not social.

---

## ACTOR LINEAGE

Actor lineage must include:

- all receipts issued
- all bundles participated in
- all challenges filed
- all challenges survived
- all supersessions performed
- all revocations applied

This forms the identity trajectory.

---

## TRUSTLESS IDENTITY LINKAGE

Identity linkage must be:

- receipt-based
- replay-verifiable
- challenge-exposed
- environment-sealed
- canonicalizable

No platform identity.  
No narrative identity.  
No unverifiable identity.

---

## IDENTITY CONVERGENCE

Identity is legitimate only if:

- canonical bytes converge
- lineage reconstructs
- key history converges
- reputation vector converges
- cross-implementation replay converges

If any diverge → `IDENTITY_DIVERGENT`.

---

## INVALID IDENTITY CONDITIONS

Identity is invalid if:

- lineage breaks
- keys drift
- receipts missing
- supersession invalid
- revocation invalid
- replay diverges
- canonicalization fails

Invalid identity → no authority.

---

## CHECK CONDITION

Identity enters check when:

- lineage is challenged
- key continuity is challenged
- reputation vector is challenged
- supersession is challenged

---

## CHECKMATE CONDITION

Identity is checkmated when:

- lineage cannot reconstruct
- key continuity fails
- receipts diverge
- canonical bytes mismatch
- challenge upheld

Checkmate is mechanical, not rhetorical.

---

## WIN CONDITION

Goodies win when identity becomes replay-verifiable.  
Goobers lose when identity collapses under lineage replay.

---

## FINAL RULE

Identity is not who you say you are.  
Identity is what survives replay.

**Proof over narrative.**
