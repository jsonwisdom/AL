# Decision Collision Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/decision_collision_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Branch Preservation Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Decision Collision Protocol v0.1 defines how conflicting lawful Operator decisions are preserved, branched, replayed, and inspected without overwriting prior history.

Conflicting decisions do not erase each other.

They create a replay branch.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "DECISION_COLLISION_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Definition

A collision is two lawful Operator decisions that cannot both be applied forward.

The protocol does not pick a winner.

The protocol does not deprecate either decision.

The protocol does not merge the decisions.

Both paths remain inspectable.

---

## Collision Detection

A collision is detected when:

1. Two decisions affect the same `scope_category` with incompatible state changes.
2. Both decisions carry valid justification receipts.
3. Both decisions adhered to membrane rules at the time of decision.

---

## Branch Creation

When a collision is detected:

1. The current lattice forks at the collision point.
2. Left branch applies Decision A forward.
3. Right branch applies Decision B forward.
4. Both branches preserve complete history up to the fork.

---

## Lineage Preservation

Each branch receives a unique lineage ID:

```text
[parent_lineage]_branch_A
[parent_lineage]_branch_B
```

Rules:

- No branch is marked primary.
- No branch is marked correct.
- No branch overwrites the other.
- Drift Meter runs independently per branch.

---

## Replay Comparison Surface

The review surface may display:

- side-by-side branch inspection
- delta viewer showing where outcomes diverge
- independent drift comparison per branch
- branch-specific justification receipts

The review surface must not display:

- recommendation labels
- winner labels
- majority labels
- authority labels
- automatic resolution prompts

---

## Strict Rules

- No automatic branch resolution.
- No witness voting to collapse branches.
- Branches persist unless Operator issues explicit archival receipt.
- Archival preserves the fork but stops active replay on that branch.
- Archival does not delete history.
- Archival moves the branch to `ARCHIVED_SCOPE` with justification.

---

## Drift Meter Integration

```json
{
  "collision_event": {
    "drift_delta": 1,
    "meaning": "unresolved_fork_observed"
  },
  "branch_drift": "measured_independently",
  "authority": false
}
```

Collision events feed Drift Meter as observation only.

They do not imply error, guilt, or invalidity.

---

## Integration

- Justification receipts must reference the branch they belong to.
- State Transition Membrane evaluates each branch independently.
- Operator Review Surface displays branch comparison read-only.
- Scope Boundary Membrane governs whether branch outcomes remain active, deferred, or archived.
- Replay Receipt Lifecycle tracks branch receipts separately.

---

## Status

```json
{
  "artifact": "DECISION_COLLISION_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
