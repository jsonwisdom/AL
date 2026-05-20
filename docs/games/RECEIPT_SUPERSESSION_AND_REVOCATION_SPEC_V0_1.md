# Replay Supersession & Revocation Specification v0.1

**SPEC_ID:** `RECEIPT_SUPERSESSION_AND_REVOCATION_SPEC_V0_1`

## ROOT INVARIANT

History cannot be rewritten.  
History can only be superseded.

Replay does not erase the past — it extends it.

## SOURCE_LINE

Once settlement exists, continuity correction becomes constitutional:

- lawful correction
- revocation semantics
- supersession lineage
- historical preservation
- replay-safe amendments

This is the memory layer of Replay Chess.

---

## PURPOSE

Define the constitutional mechanics for:

- receipt supersession
- receipt revocation
- lineage preservation
- historical continuity
- replay-safe amendments

This spec ensures that correction is lawful and history is immutable.

---

## 1. RECEIPT_SUPERSESSION_OBJECT

A supersession declaration must include:

- `supersession_id`
- `prior_receipt_id`
- `superseding_receipt_id`
- `supersession_basis`
- `challenge_window`
- `lineage_proof`
- `supersession_hash`

Missing any → `NON_ADMISSIBLE`.

---

## 2. LAWFUL SUPERSESSION

A receipt may be superseded only if:

- the prior receipt is valid
- the superseding receipt is valid
- the supersession basis is declared
- the lineage is preserved
- the challenge window is open
- replay converges

Supersession is additive, not destructive.

---

## 3. SUPERSESSION BASIS

Valid bases include:

- error correction
- environment mismatch correction
- canonicalization correction
- state reconstruction correction
- verifier spec update
- receipt field amendment

Invalid bases:

- narrative preference
- platform declaration
- authority fiat
- reputational pressure

Replay, not narrative, determines correction.

---

## 4. RECEIPT REVOCATION

A receipt may be revoked only if:

- replay diverges
- canonicalization fails
- environment invalid
- challenge upheld
- fraud proven
- malicious divergence detected

Revocation is rare, hostile-tested, and forensically proven.

---

## 5. LINEAGE PRESERVATION

Supersession must preserve:

- full historical chain
- prior receipt identity
- prior canonical bytes
- prior replay results
- prior challenge history

History is append-only, never rewritten.

---

## 6. AMENDMENT RULES

Amendments must:

- be replay-safe
- be challenge-exposed
- preserve lineage
- not alter prior canonical bytes
- not erase prior receipts

Amendments are extensions, not edits.

---

## 7. SUPERSESSION GRAPH

Supersession forms a directed acyclic graph:

- nodes = receipts
- edges = supersession events
- no cycles
- no deletion
- no orphan receipts

This is the memory topology of Replay Chess.

---

## 8. INVALID SUPERSESSION CONDITIONS

Supersession is invalid if:

- lineage breaks
- canonical bytes altered
- environment drift introduced
- challenge window bypassed
- replay diverges
- supersession basis missing

Invalid supersession → ignored.

---

## 9. CHECK CONDITION

A receipt enters check when:

- a supersession is proposed
- a revocation is proposed
- a lineage challenge is filed

---

## 10. CHECKMATE CONDITION

Checkmate occurs when:

- supersession fails replay
- revocation fails replay
- lineage cannot reconstruct
- canonical bytes mismatch
- challenge upheld

Checkmate is mechanical, not rhetorical.

---

## WIN CONDITION

Goodies win when history becomes immutable but correctable.  
Goobers lose when narrative cannot rewrite the past.

---

## FINAL RULE

History is append-only.  
Correction is lawful.  
Supersession is constitutional.

**Proof over narrative.**
