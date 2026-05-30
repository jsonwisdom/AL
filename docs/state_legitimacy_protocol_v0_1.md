# State Legitimacy Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/state_legitimacy_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Transition Audit Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

State Legitimacy Protocol v0.1 evaluates whether state transitions satisfy replay-verifiable requirements.

Legitimacy is transition compliance.

Legitimacy is not correctness.

Legitimacy is not authority.

Legitimacy is not outcome validation.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "STATE_LEGITIMACY_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Legitimate:** transition followed all applicable rules, obligations, prerequisites, and protocol constraints.
- **Lawful:** legitimate within protocol definition.
- **Illegitimate:** transition missing prerequisites or violating obligations.
- **Correct:** desired outcome; not defined by this protocol.
- **Authority:** false; no legitimacy check creates authority.

---

## Legitimacy Schema

```yaml
state_legitimacy_v0_1:
  transition_id: UUID
  from_state_hash: pointer
  to_state_hash: pointer
  object_id: UUID
  object_type: receipt | branch | snapshot | decision | capability_assignment | obligation_change
  prerequisites_met: boolean
  prerequisites_checklist:
    - condition: PASS | FAIL
  obligations_satisfied: boolean
  violation_log_ref: obligation_violation_id_or_null
  legitimacy_status: LEGITIMATE | ILLEGITIMATE | REVIEWED_ILLEGITIMATE
  legitimacy_timestamp: ISO_8601
  verified_by_replay: boolean
```

---

## Prerequisite Types by Transition

| Transition Type | Prerequisites |
|---|---|
| Branch creation | Parent branch exists, justification receipt logged, membrane not suspended |
| Decision emission | Operator ID verified, justification receipt attached, no conflicting active lock |
| Capability grant | Object exists, capability token valid, Operator initiator, justification receipt |
| Snapshot capture | Atomic read confirmed, no pending writes, timestamp recorded |
| Scope status change | Membrane HOLDS or RELEASES, no active collision unresolved |
| Obligation change | Source is operator, justification receipt present, no override of protocol immutables |

---

## Legitimacy Event Schema

```yaml
legitimacy_event:
  transition_id: UUID
  from_state_hash: pointer
  to_state_hash: pointer
  prerequisites_checklist:
    condition: PASS | FAIL
  obligations_check: PASS | FAIL
  violation_ids:
    - obligation_violation_id
  status: LEGITIMATE | ILLEGITIMATE | REVIEWED_ILLEGITIMATE
  replay_verifiable: true
```

---

## Rules

1. Legitimate requires all prerequisites to pass.
2. Legitimate requires obligations to be satisfied or violations to be explicitly logged within Operator-defined tolerance for that lineage.
3. Illegitimate if any prerequisite fails.
4. Illegitimate if any obligation is violated without Operator waiver.
5. Illegitimate transitions are logged to legitimacy history.
6. Illegitimate transitions feed Drift Meter as `+2` per illegitimate transition.
7. Illegitimate transitions are not automatically deleted or rejected.
8. Replay preserves illegitimate transitions and marks them as illegitimate.

---

## Operator Waiver

An Operator waiver for an illegitimate transition requires:

- justification receipt
- explicit acknowledgment: `This transition is ILLEGITIMATE but preserved`
- branch or lineage reference
- drift meter snapshot

A waiver does not change legitimacy status to legitimate.

A waiver marks the transition as `REVIEWED_ILLEGITIMATE`.

---

## Legitimacy Review Surface

Jay-only, read-only review surface may:

- show all transitions with `legitimacy_status = ILLEGITIMATE`
- filter by object type
- filter by lineage
- filter by branch
- filter by timestamp
- show prerequisite failures per transition
- compare legitimacy across branches
- show drift accumulated from illegitimate transitions

The review surface must not:

- change legitimacy status automatically
- erase illegitimate transitions
- mark a transition correct
- grant authority
- resolve collisions automatically

---

## Legitimacy vs Authority

| Concept | Meaning | Authority Required? |
|---|---|---|
| Legitimate | Followed rules | No |
| Correct | Achieved desired outcome | No; not defined here |
| Authorized | Granted by authority | No; authority remains false |
| Admitted | Passed scope boundary | Operator decision |

---

## Integration

- Drift Meter includes illegitimate transition weight.
- Temporal snapshots capture legitimacy status at freeze time.
- Justification receipts may reference legitimacy checks.
- Obligation violations trigger legitimacy failure unless waived.
- Decision Collision Protocol runs legitimacy checks on colliding decisions.
- State Transition Membrane governs protocol-level transition changes.

---

## Status

```json
{
  "artifact": "STATE_LEGITIMACY_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
