# GBRS-MIG-0001: Migration, Fork, and Succession Legitimacy

**Status:** Draft  
**Version:** 0.1  
**Category:** Migration / Fork Governance / Succession  
**Applies to:** GBRS-governed truth surfaces, routing surfaces, capability surfaces, agent authority surfaces, and successor or forked deployments.

---

## 1. Purpose

This specification defines how a GBRS-governed system may migrate, fork, or transfer authority without erasing lineage.

GBRS permits evolution. It does not permit amnesia.

Core axiom:

```text
Authority may migrate, but lineage must not disappear.
```

A successor truth surface may supersede prior canon, but it MUST preserve the replayability and verifiability of the prior canonical truth surface.

---

## 2. Scope

This specification governs:

- migration from one canonical truth surface to another;
- forks that preserve visibility of the prior canon;
- succession of administrative or agent authority;
- transition windows where old and new truth surfaces co-exist;
- rejection of hostile, non-lineage-valid, or history-erasing forks.

This specification does not define a particular storage layer, blockchain, resolver, Git host, wallet, or signature scheme.

---

## 3. Terminology

### 3.1 Truth Surface

A replay-verifiable source of canonical receipts, such as `_truth/receipts/index.json` and its associated receipt graph.

### 3.2 Prior Canon

The final accepted canonical state of `TS_old` before migration, fork, or succession begins.

### 3.3 Successor Truth Surface

A new truth surface `TS_new` that claims legitimate continuity from `TS_old`.

### 3.4 Fork

A new truth surface that preserves lineage from `TS_old` while declaring a divergent future path.

### 3.5 Migration

A continuity-preserving transition from `TS_old` to `TS_new` where `TS_new` is intended to become successor canon.

### 3.6 Succession

A transfer of authority from one canonically authorized actor or set of actors to another.

---

## 4. Genesis Receipt for Forks and Successor Truth Surfaces

### 4.1 Name

`GENESIS_RECEIPT`

### 4.2 Role

A `GENESIS_RECEIPT` establishes the legitimate origin of a new truth surface, whether successor or fork.

### 4.3 Definition

A `GENESIS_RECEIPT` is a canonical receipt in the new truth surface `TS_new` that:

#### References the prior canon

- `previous_truth_surface_hash`, such as the hash of `_truth/receipts/index.json` at the final canonical commit of `TS_old`;
- `previous_canonical_commit`, such as a Git SHA or equivalent lineage identifier.

#### Declares the new root

- `new_truth_surface_hash`;
- `new_canonical_commit`.

#### Binds authority

- signature or authorization by the current canonical authority of `TS_old`; or
- N-of-M authorization under a canonically defined sovereign transfer protocol.

#### Specifies intent

- `migration_kind`: `successor` or `fork`;
- `migration_policy_hash`: hash of the migration policy document governing the transition.

### 4.4 Validity Conditions

A `GENESIS_RECEIPT` is valid if and only if:

1. `previous_truth_surface_hash` and `previous_canonical_commit` are replay-verifiable in `TS_old`.
2. The signer or signers are canonically authorized in `TS_old`, according to GBRS-AGT-0001 or the applicable authority profile.
3. `new_truth_surface_hash` and `new_canonical_commit` match the actual state of `TS_new`.

If any condition fails, the new truth surface is non-legitimate under GBRS.

---

## 5. Lineage Transfer Invariant

### 5.1 Name

`LINEAGE_TRANSFER_INVARIANT`

### 5.2 Role

The Lineage Transfer Invariant ensures that authority may migrate, but lineage must not disappear.

### 5.3 Invariant Statement

No migration, fork, or succession event may render the prior canonical truth surface unreplayable or its lineage unverifiable.

For a transition from `TS_old` to `TS_new` to be constitutionally valid, all of the following MUST hold.

#### 5.3.1 Replay Preservation

A verifier MUST be able to:

- reconstruct `TS_old` up to its final canonical commit;
- verify `previous_truth_surface_hash` and `previous_canonical_commit` referenced in the `GENESIS_RECEIPT`.

#### 5.3.2 Lineage Link

There MUST exist at least one `GENESIS_RECEIPT` in `TS_new` such that:

- it references `TS_old`;
- it is canonical in `TS_new`;
- it is signed or authorized by canonically authorized agents from `TS_old`.

#### 5.3.3 Non-Destructive Succession

`TS_new` MUST NOT:

- delete receipts from `TS_old`;
- rewrite history of `TS_old`;
- collapse multiple historical states into an untraceable aggregate.

`TS_new` MAY supersede prior canon. It MUST NOT erase it.

If any of these conditions fail, the migration MUST be classified as `MIGRATION_REJECTED` and treated as hostile, non-legitimate, or non-canonical.

---

## 6. Dual Witness Window

### 6.1 Purpose

The Dual Witness Window is the period during which both `TS_old` and `TS_new` MUST remain replay-verifiable before `TS_new` may be accepted as `SUCCESSOR_CANON`.

This prevents rushed or coercive authority transfer.

### 6.2 Required State

During the Dual Witness Window:

- `TS_old` remains replayable;
- `TS_new` remains replayable;
- the `GENESIS_RECEIPT` is verifiable in `TS_new`;
- the final canonical state of `TS_old` is independently reconstructable;
- both surfaces expose enough state for external replay.

### 6.3 Acceptance Condition

`TS_new` may transition to `SUCCESSOR_CANON` only if:

1. the Dual Witness Window completes without unresolved divergence;
2. all migration policy checks pass;
3. no valid challenge receipt remains open;
4. `TS_old` remains preserved as `SUPERSEDED_CANON` or equivalent lineage-visible archive.

### 6.4 Failure Condition

If `TS_old` becomes unreplayable, if `TS_new` cannot prove its genesis, or if authority signatures fail lineage validation, the migration MUST enter `MIGRATION_REJECTED`.

---

## 7. Migration State Machine

GBRS-MIG-0001 defines the following states:

```text
ACTIVE_CANON
MIGRATION_PROPOSED
DUAL_WITNESS_WINDOW
SUCCESSOR_CANON
SUPERSEDED_CANON
FORK_DECLARED
RECONVERGENCE_PROVEN
DEPRECATED_WITH_MEMORY
MIGRATION_REJECTED
```

### 7.1 ACTIVE_CANON

The current accepted canonical truth surface.

### 7.2 MIGRATION_PROPOSED

A successor or fork has been proposed but has not yet completed lineage validation.

### 7.3 DUAL_WITNESS_WINDOW

Both prior and proposed truth surfaces are replay-visible.

### 7.4 SUCCESSOR_CANON

The new truth surface has passed validation and becomes canonical going forward.

### 7.5 SUPERSEDED_CANON

The prior truth surface is no longer active but remains replayable and lineage-visible.

### 7.6 FORK_DECLARED

A new truth surface declares divergence while preserving prior lineage.

### 7.7 RECONVERGENCE_PROVEN

A prior fork or migration split has been non-destructively reconciled by replay-valid receipts.

### 7.8 DEPRECATED_WITH_MEMORY

A surface is deprecated, but its receipts and authority trail remain available for replay.

### 7.9 MIGRATION_REJECTED

A migration or fork failed lineage, authority, or replay validation.

---

## 8. Succession Rules

Authority succession MUST be receipt-bound.

A successor authority is valid only if:

- the prior authority is canonical;
- the transfer receipt is canonical;
- the successor authority identity is canonical;
- the transfer is not revoked, superseded, or under unresolved challenge.

Possession of a key, repository credential, resolver permission, or deployment token does not by itself establish succession legitimacy.

---

## 9. Fork Legitimacy

A fork is legitimate only if it preserves and references prior lineage.

A fork that hides, deletes, rewrites, or refuses to reference the prior truth surface MUST be treated as hostile or non-canonical.

GBRS permits divergent futures. It denies falsified origins.

---

## 10. Compliance

A system is GBRS-MIG-0001 compliant if and only if:

1. every successor or fork begins with a valid `GENESIS_RECEIPT`;
2. prior canon remains replayable;
3. authority transfer is receipt-bound;
4. the Dual Witness Window is enforced before successor canon is accepted;
5. rejected migrations are visibly classified as `MIGRATION_REJECTED`;
6. no migration erases or silently rewrites prior lineage.

---

## 11. Core Axiom

```text
Authority may migrate, but lineage must not disappear.
```

This is the evolutionary boundary of GBRS.
