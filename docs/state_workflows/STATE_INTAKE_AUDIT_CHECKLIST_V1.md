# State Intake Audit Checklist v1

## Constitutional Basis

This checklist applies the five-tier audit model to evaluate whether
a state pipeline is constitutionally admissible. No state becomes
operational until it satisfies all applicable tiers with committed,
hash-verifiable artifacts.

## Five-Tier Audit Model

| Tier | Question | Requirement |
|------|----------|-------------|
| CLAIM | Does the pipeline claim a result? | Documented in methodology, README, or ledger |
| REFERENCE | Is the claim traceable to an artifact? | Ledger row, hash, path, or issue reference exists |
| SHAPE | Is the artifact structure valid? | Matches constitutional schema for its type |
| EVIDENCE | Are hashes from committed observed bytes? | Real source hashes, committed artifact bytes |
| JURISDICTION | May downstream claims proceed? | All prior tiers satisfied + no active halt |

## State Intake Fields

### Identification

- **State Name:** [e.g., New York]
- **State FIPS:** [e.g., 36]
- **County Count:** [e.g., 62]
- **County Count Source:** [e.g., U.S. Census Bureau 2020 FIPS]

### Scaffold (STATE-001)

- **FIPS Scaffold Path:** [e.g., _truth/bigquery/ny_county_fips_62.csv]
- **FIPS Scaffold Hash:** [sha256:...]
- **FIPS Scaffold Status:** [COMMITTED / MISSING]
- **Row Count Verified:** [62 / NOT VERIFIED]

### Source Probe (STATE-002)

- **Probe Path:** [path or NOT FOUND]
- **Sources Identified:** [e.g., ACS, NOAA GSOD]
- **Sources Accessible:** [count]
- **Sources Inaccessible:** [count]
- **Inaccessible Sources Documented:** [YES / NO]

### Economic Overlay (STATE-003)

- **Overlay Path:** [path or NOT FOUND]
- **Overlay Hash:** [sha256:... or PLACEHOLDER]
- **Coverage:** [X/Y counties]
- **Coverage Status:** [FULL / PARTIAL / NOT COMMITTED]
- **Previous Receipt Hash:** [sha256:... or INCOMPLETE]

### Sparse Overlay (STATE-004)

- **Overlay Path:** [path or NOT FOUND]
- **Overlay Hash:** [sha256:... or PLACEHOLDER]
- **Coverage:** [X/Y counties]
- **Counties With Data:** [count, enumerated]
- **Counties Without Data:** [count, enumerated]
- **Sparsity Declared:** [YES / NO]
- **Interpolation:** [NONE / PRESENT — if PRESENT, state is inadmissible]
- **Statewide Claim:** [NONE / PRESENT — if PRESENT, state is inadmissible]

### Dependency Audit (STATE-005)

- **Audit Path:** [path or NOT FOUND]
- **Missing Artifacts:** [list or NONE]
- **Downstream Dependencies:** [list]
- **Transitive Blocks:** [list or NONE]

### Methodology (STATE-006)

- **Methodology Path:** [path or NOT FOUND]
- **Guardrails Documented:** [YES / NO]
- **Prohibited Claims Enumerated:** [YES / NO]
- **Data Gaps Recorded:** [YES / NO]

### Halt Status (STATE-007, if applicable)

- **Active Halt:** [YES / NO]
- **Halt Receipt Path:** [path or NONE]
- **Halted Artifact:** [name or NONE]
- **Halt Reason:** [MISSING_ARTIFACT / PLACEHOLDER_EVIDENCE / OTHER]

### Lift Contract (STATE-008, if halted)

- **Lift Contract Path:** [path or NONE]
- **Lift Conditions Count:** [number]
- **Lift Conditions Satisfied:** [count]
- **Lift Conditions Remaining:** [count]

### Restoration Status (STATE-009, if halted)

- **Restoration Attempted:** [YES / NO]
- **Restoration Result:** [NOT_ATTEMPTED / ACCEPTED / REJECTED]
- **Restoration Receipt Path:** [path or NONE]

## Five-Tier Summary

| Tier | Status | Detail |
|------|--------|--------|
| CLAIM | [PRESENT / ABSENT] | [source document] |
| REFERENCE | [PRESENT / ABSENT] | [ledger row, hash, or path] |
| SHAPE | [ACCEPTED / REJECTED / NOT EVALUATED] | [constitutional schema] |
| EVIDENCE | [COMPLETE / INCOMPLETE / NOT EVALUATED] | [real vs placeholder hashes] |
| JURISDICTION | [ACTIVE / SUSPENDED / NOT ESTABLISHED] | [halt status] |

## Admissibility Determination

```text
STATE:          [name]
ADMISSIBLE:     [YES / NO]
HALTED:         [YES / NO]
MISSING:        [enumerated list or NONE]
NEXT ACTION:    [specific evidence required or NONE]
```

## Invariant

```text
NO STATE IS ADMISSIBLE UNTIL ALL APPLICABLE TIERS
ARE SATISFIED WITH COMMITTED, HASH-VERIFIABLE ARTIFACTS.
```

A state that passes CLAIM, REFERENCE, and SHAPE but fails EVIDENCE
is PARTIALLY VERIFIED with SUSPENDED JURISDICTION.

A state that passes all five tiers is OPERATIONAL.

## Current State Map (Auto-Generated from Committed Artifacts)

| State | Claim | Reference | Shape | Evidence | Jurisdiction |
|-------|-------|-----------|-------|----------|--------------|
| NY | PRESENT | PRESENT | ACCEPTED | INCOMPLETE | SUSPENDED |

No other states have committed artifacts.
This table grows only when new state artifacts are committed.
