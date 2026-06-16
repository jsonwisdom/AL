# State-Level ALMS Flywheel v1

## Constitutional Basis

This template defines the standard state-level ALMS workflow.
It is seeded from the NY prototype only. No pattern is included
that has not been demonstrated by at least one committed artifact
in the NY pipeline.

## Rule

NY is the prototype, not proof of cross-state maturity.
Each state must demonstrate its own artifacts before its
pipeline is considered operational.

## Standard State Flywheel

### Phase 1: Scaffold

**STATE-001: County FIPS Scaffold**
- Deterministic county enumeration
- Exact count enforced
- Duplicate rejection
- Hash-pinned CSV output
- Manifest JSON with hash
- Ledger append
- Policy: LOCAL_ONLY_NO_DYNAMIC_FETCH_NO_GHOST_PROMOTION

### Phase 2: Probe

**STATE-002: Source/Schema Probe**
- Identify available data sources for the state
- Document schema for each source
- Record accessibility (FOUND, NOT_FOUND, CRAWLER_BLOCKED)
- No data fetch yet; probe only
- Explicitly document what is NOT available

### Phase 3: Full-Density Economic Overlay

**STATE-003: Economic Overlay**
- Full county coverage expected
- Hash-pinned source data
- Deterministic join to FIPS scaffold
- Row count verification
- Content hash in ledger
- Policy: FULL_COUNTY_ECONOMIC_ONLY_NO_CLIMATE_CLAIM

### Phase 4: Sparse Climate/Public-Data Overlay

**STATE-004: Sparse Overlay**
- Partial county coverage expected
- Explicit sparsity declaration (X/N counties)
- Enumeration of covered counties
- Enumeration of uncovered counties
- No interpolation
- No statewide claim
- Hash-pinned source data
- Deterministic join
- Policy: SPARSE_ONLY_NO_STATEWIDE_VALIDATION

### Phase 5: Dependency Audit

**STATE-005: Dependency Audit**
- Map all downstream dependencies
- Verify each referenced artifact exists
- Flag missing artifacts as BLOCKED
- Document transitive dependencies
- No promotion of unverifiable claims

### Phase 6: Methodology Limitations

**STATE-006: Methodology Limitations Note**
- Document all guardrails
- Enumerate prohibited claims
- Record data gaps explicitly
- Cite relevant precedents
- Policy: NO_GHOST_PROMOTION

### Phase 7-9: Halt/Lift/Restoration (Conditional)

**STATE-007: Halt Receipt**
- Only if a referenced artifact is missing or unverifiable
- Records: what is missing, what depends on it, constitutional basis

**STATE-008: Lift Contract**
- Only if a halt is active
- Enumerates exact conditions for restoration

**STATE-009: Restoration/Rejection**
- Only after artifact is committed and replay-verified
- Restoration receipt if conditions met
- Rejection receipt if conditions not met
- Precedent update if new holding established

## Current State

### NY (Prototype)

| Phase | Artifact | Status |
|-------|----------|--------|
| 1 | NY-001 FIPS Scaffold | COMMITTED |
| 2 | NY-002 Probe | NOT FOUND |
| 3 | NY-003C ACS Income | COMMITTED (62/62) |
| 4 | NY-004 NOAA Overlay | LEDGER_VERIFIED (6/62), ARTIFACT NOT FOUND |
| 5 | NY-005 Dependency Audit | NOT FOUND |
| 6 | NY-012 Methodology | COMMITTED |
| 7 | NY_ALMS_HALT_001 | COMMITTED |
| 8 | NY_004_LIFT_CONDITIONS_V1 | COMMITTED |
| 9 | NY_004_RESTORATION_REJECTION_V1 | COMMITTED |

### Other States

No other state-level pipelines are committed.

## Rule for Expansion

A new state may be added to this document only when:
1. Its STATE-001 FIPS scaffold is committed and hash-verified
2. At least one overlay (STATE-003 or STATE-004) is committed
3. The state's methodology limitations note is committed

Until then, the state is not operational and is not listed here.

## Constitutional Invariant

```text
NO STATE EXISTS IN THIS DOCUMENT
UNTIL ITS ARTIFACTS EXIST IN THE REPO
```

This document describes what the repo contains, not what it plans to contain.
