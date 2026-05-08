# State Jurisdiction Enum v1

## Purpose

Define the closed jurisdiction status enum for state-level ALMS intake.

This enum converts state posture labels into CI-targetable constitutional language.
It prevents scaffold evidence from being promoted into full operational jurisdiction.

---

## Constitutional Basis

A state is operational only for the specific tier it has earned through committed, hash-verifiable artifacts.

```text
ACTIVE != FULL_OPERATIONAL
ACTIVE MUST BE TIER-SCOPED
```

---

## Allowed Jurisdiction Values

```text
NOT_ESTABLISHED
SUSPENDED
ACTIVE_SCAFFOLD_ONLY
ACTIVE_ECONOMIC_ONLY
ACTIVE_SPARSE_OVERLAY_ONLY
ACTIVE_FULL_STATE_WORKFLOW
```

No other jurisdiction values are permitted.

---

## Enum Semantics

### NOT_ESTABLISHED

No committed state artifacts exist.

A state in this status may not appear in the active state map except as explicitly excluded or not indexed.

### SUSPENDED

The state has at least one claim/reference/shape tier present, but evidence or jurisdiction is blocked by an active halt.

Downstream claims may not proceed.

### ACTIVE_SCAFFOLD_ONLY

The state has a committed and hash-verified STATE-001 county FIPS scaffold.

This status proves only:

- county enumeration exists
- committed scaffold bytes exist
- real artifact hash exists
- manifest exists

This status does not prove:

- economic coverage
- climate coverage
- multi-signal coverage
- interstate comparison
- policy recommendation

### ACTIVE_ECONOMIC_ONLY

The state has a committed and hash-verified economic overlay tied to its scaffold.

This status does not prove climate or sparse public-data coverage.

### ACTIVE_SPARSE_OVERLAY_ONLY

The state has a committed and hash-verified sparse overlay with explicit coverage and absence enumeration.

This status does not prove full statewide coverage unless all counties are covered and declared as such by committed evidence.

### ACTIVE_FULL_STATE_WORKFLOW

The state has passed all required tiers for the declared workflow:

- scaffold
- source/schema probe
- economic overlay where applicable
- sparse overlay where applicable
- dependency audit
- methodology limitations note
- no active halt

This status may not be assigned by declaration.
It must be derived from committed artifacts.

---

## Prohibited Values

The following values are forbidden because they collapse tier boundaries:

```text
ACTIVE
OPERATIONAL
VERIFIED
COMPLETE
FULLY_VERIFIED
READY
GREEN
```

These values are ambiguous and must fail future CI once enforcement exists.

---

## Current Assignments

| State | Jurisdiction Enum | Basis |
|-------|-------------------|-------|
| NY | SUSPENDED | NY-004 evidence incomplete; halt active |
| MN | ACTIVE_SCAFFOLD_ONLY | MN-001 scaffold CSV + manifest committed and hash-verified |

No other state jurisdiction is established.

---

## Invariant

```text
NO STATE MAY CLAIM A BROADER JURISDICTION ENUM
THAN ITS COMMITTED ARTIFACTS SUPPORT.
```

Any unclassified or ambiguous state posture defaults to:

```text
NOT_ESTABLISHED
```

Fail closed, never open.
