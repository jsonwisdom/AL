# Protocol Coherence Protocol v0.1

**Repo:** `jsonwisdom/AL`  
**Branch:** `feature/alabama-alms-speed-layer-v0-1`  
**Artifact:** `docs/protocol_coherence_protocol_v0_1.md`  
**Status:** Ratified as Proposed / Protocol Stack Audit Layer  
**Authority:** false  
**Membrane:** HOLDS

---

## Purpose

Protocol Coherence Protocol v0.1 defines how protocols are compared for contradictions, overlaps, gaps, and incompatible obligations or capabilities.

Coherence is observable consistency between protocols.

Coherence is not correctness.

Coherence is not authority.

Coherence is not enforcement.

---

## Operator Receipt

```json
{
  "operator": "JASON_WISDOM_ZEROCOOL",
  "artifact": "PROTOCOL_COHERENCE_PROTOCOL_V0_1",
  "decision": "RATIFIED_AS_PROPOSED",
  "edits_required": false,
  "authority": false,
  "membrane": "HOLDS"
}
```

---

## Core Definitions

- **Coherence:** protocols do not contradict, overlaps are clean, and no required coverage is missing.
- **Incoherence:** contradiction, ambiguous overlap, or missing coverage detected.
- **Replay-verifiable coherence:** coherence state captured with every protocol addition or change.
- **Observation-only check:** coherence check reports findings; Operator decides action.

---

## Coherence Schema

```yaml
protocol_coherence_v0_1:
  coherence_check_id: UUID
  timestamp: ISO_8601
  protocols_checked:
    - protocol_id
  contradictions:
    - conflict_object
  overlaps:
    - overlap_object
  gaps:
    - gap_object
  coherence_status: COHERENT | INCOHERENT | PARTIAL
  replay_verifiable: true
```

---

## Contradiction Detection Rules

Two protocols contradict when one permits, requires, defines, or preserves something that another forbids, negates, deletes, or redefines incompatibly.

| Type | Example | Severity |
|---|---|---|
| Obligation clash | A says `MUST_LOG_TIMESTAMP`, B says `MUST_NOT_LOG_TIMESTAMP` | Critical |
| Capability clash | A says `CAN_FORK`, B says `CANNOT_FORK` | Major |
| Category clash | A defines `ARCHIVED` as frozen, B defines `ARCHIVED` as deletable | Major |
| Identity clash | A says ID changes on fork, B says ID persists | Critical |

---

## Overlap Detection Rules

Overlap is coherent when:

- protocols agree on identical rule
- protocols define compatible but different aspects of the same object
- overlap is tagged as `OVERLAP_COHERENT`

Overlap is ambiguous when:

- protocols both address the same domain but precedence or compatibility is unclear
- overlap is tagged as `OVERLAP_AMBIGUOUS`

Example ambiguous overlap:

```text
Protocol A: Snapshots preserve state.
Protocol B: Snapshots may omit witness clusters if size exceeds threshold.
No explicit precedence is defined.
```

---

## Gap Detection Rules

Missing coverage is detected when an expected behavior or object class lacks governing rules.

| Gap Type | Example |
|---|---|
| Undefined transition | No protocol addresses snapshot capture during collision |
| Missing obligation | Object type exists but no mandatory or prohibited behavior is defined |
| Orphaned capability | Capability granted but no protocol defines bounds |

---

## Coherence Event Schema

```yaml
coherence_event:
  coherence_check_id: UUID
  protocols_checked:
    - protocol_id
  contradictions_found:
    - contradiction_id
  overlaps_found:
    - overlap_id
  gaps_found:
    - gap_id
  status: COHERENT | INCOHERENT | PARTIAL
  operator_review_required: boolean
```

---

## Severity and Drift Contribution

| Severity | Drift Units | Operator Action Required? |
|---|---:|---|
| Critical contradiction | +5 | Yes; resolution receipt required |
| Major contradiction | +3 | Recommended |
| Minor contradiction | +1 | Optional |
| Ambiguous overlap | +0 | Review recommended |
| Critical gap | +4 | Yes; resolution receipt required |

---

## Resolution Actions

Operator-only resolution actions:

1. **Amend protocol:** modify one or both conflicting protocols and log justification receipt.
2. **Declare precedence:** specify which protocol governs in case of contradiction and log justification.
3. **Accept incoherence:** acknowledge and preserve both; drift recorded; no merge.
4. **Version split:** create protocol v0.2 for one branch while preserving v0.1 on another.

---

## Coherence Review Surface

Jay-only, read-only surface may:

- run full coherence check on active protocols
- run subset check, such as capability-related protocols only
- show historical coherence status from snapshots
- compare coherence across branches
- export contradiction and gap report

The review surface must not:

- enforce changes
- alter protocols
- resolve contradictions automatically
- claim authority
- erase prior protocol versions

---

## Rules

1. Protocol changes trigger coherence check.
2. Critical contradictions prevent protocol activation until resolved.
3. Coherence check observes and reports; it does not enforce changes by itself.
4. Witnesses cannot propose coherence changes.
5. Temporal snapshots capture coherence status at freeze time.
6. Operator actions that resolve coherence require justification receipts.

---

## Integration

- Drift Meter includes coherence-derived drift units.
- Justification receipts may cite coherence check IDs.
- State Legitimacy Protocol references coherence for prerequisite checks.
- Obligation and capability changes trigger coherence re-checks.
- Decision Collision Protocol includes coherence as an inspection dimension.

---

## Status

```json
{
  "artifact": "PROTOCOL_COHERENCE_PROTOCOL_V0_1",
  "status": "RATIFIED_AS_PROPOSED",
  "authority": false,
  "membrane": "HOLDS"
}
```
