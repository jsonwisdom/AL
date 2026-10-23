# Civic War — American History Board Game v0.1

**Format:** JSON-driven tabletop strategy and civic-history navigation game  
**Players:** 2–6  
**Play time:** 60–150 minutes  
**Classification:** Draft educational simulation  
**Historical verification:** not performed  
**Execution authority:** false  
**Promotion:** blocked

## Premise

Players navigate American history across three dimensions:

- **X — Time**
- **Y — Geography and directional pathing**
- **Z — Claimed constitutional authority**

The objective is not to conquer territory. The objective is to build the most defensible civic record by connecting claims to sources, provenance, jurisdiction, implementation, effects, and later review.

`CIVIL_WAR` is a historical era. `CIVIC_WAR` is a comparative gameplay layer involving legitimacy, records, representation, institutional trust, access, and competing public claims. The game does not declare them equivalent.

## Winning

The game ends when the final Era card resolves or when the Evidence deck is exhausted.

Players score:

```text
+3 VERIFIED_SOURCE
+3 PROVENANCE_CHAIN
+2 VALID_JURISDICTION
+2 SUCCESSFUL_CHALLENGE
+2 PRESERVED_FORK
+1 PUBLIC_RECORD_ACCESS
+1 COMPLETED_APPEAL_PATH
-3 UNSUPPORTED_AUTHORITY
-2 COLLAPSED_CONFLICTING_RECORDS
-2 INVENTED_HISTORY
-1 BROKEN_CUSTODY
```

The winner has the highest **Civic Integrity Score**. Ties are broken by the greatest number of preserved evidence chains, then the fewest unresolved authority claims.

## Components

```text
1 modular US history board
1 Time track: 1763 → present
1 Authority depth track: Z0 → Z8
6 player boards
120 History cards
72 Evidence cards
48 Authority cards
36 Challenge cards
24 Institution cards
18 Fork tokens
30 Gap tokens
60 Record cubes
6 Custody markers
6 Appeal markers
1 Gate status board
1 six-sided Movement die
1 eight-sided Review die
```

## Player Roles

Roles grant methods, not truth or superior authority.

```text
ARCHIVIST       preserve source bytes and custody
REPORTER        expose records and compare public claims
ADVOCATE        challenge jurisdiction and open appeals
LEGISLATOR      propose statutes and amendments
JUDGE           review disputes under bounded procedure
CITIZEN         petition, organize, vote, and demand records
```

No role may self-validate its own disputed claim.

## Board Structure

Each location is represented by a coordinate:

```text
US3D://<TIME>/<GEOGRAPHY>/<AUTHORITY>/<OBJECT_CLASS>/<OBJECT_ID>@<VERSION>
```

The board contains:

1. **Era lanes** along X.
2. **Federal, state, county, municipal, and territorial spaces** along Y.
3. **Authority depth rings** along Z.
4. **Route edges** connecting records, events, institutions, and claims.

## Turn Sequence

```text
1 OBSERVE
2 MOVE
3 DRAW
4 CLAIM_OR_CHALLENGE
5 ATTACH_EVIDENCE
6 REVIEW_GATE
7 RECORD_RECEIPT
```

### 1. Observe

Read the current History card. Separate its stated facts, attributed claims, interpretation, and unresolved questions.

### 2. Move

Spend up to three movement points:

```text
MOVE_TIME_FORWARD
MOVE_TIME_BACKWARD
MOVE_GEOGRAPHY
MOVE_AUTHORITY_UP
MOVE_AUTHORITY_DOWN
FOLLOW_EDGE
RETURN_TO_SOURCE
```

### 3. Draw

Draw one card from the deck matching the occupied space: History, Evidence, Authority, Challenge, or Institution.

### 4. Claim or Challenge

A claim must declare:

- claimant,
- source cited,
- jurisdiction,
- authority class,
- requested effect,
- challenge path.

A challenge identifies one specific missing or conflicting gate.

### 5. Attach Evidence

Evidence may support integrity, identity, authorship, authority, implementation, effect, or later review. Evidence supporting one gate does not automatically satisfy another.

### 6. Review Gate

Resolve the claim from the lowest incomplete depth layer upward:

```text
Z0 SOURCE_BYTES
Z1 DOCUMENT_IDENTITY
Z2 PROVENANCE_AND_CUSTODY
Z3 FORMAL_AUTHORITY_CLAIM
Z4 JURISDICTION
Z5 IMPLEMENTATION
Z6 EFFECT
Z7 LATER_REVIEW
Z8 INTERPRETATION
```

A player may not jump directly from Z0 to Z8.

### 7. Record Receipt

Every resolved turn produces a JSON receipt. Failed and unresolved attempts are recorded, not erased.

## Core Mechanics

### Evidence Chains

A completed chain requires at least:

```text
SOURCE → IDENTITY → PROVENANCE → AUTHORITY → JURISDICTION
```

Implementation, effect, review, and interpretation may then be added.

### Forks

When credible records conflict, place a Fork token. Keep both branches active until a later card or successful review resolves the conflict.

```text
CONFLICTING_RECORDS -> FORK_DO_NOT_COLLAPSE
```

### Gaps

When a required record is absent, place a Gap token. Players may search, petition, compare archives, or proceed with reduced confidence. They may not invent missing history.

### Civic Pressure

Petitions, protests, elections, journalism, litigation, legislation, administrative action, and public records requests create Civic Pressure. Pressure may force review but cannot itself establish truth or lawful authority.

### Appeal

A denied claim may move through an explicit appeal route. Appeals preserve the original decision, evidence, objections, and successor ruling.

## Historical Era Modules

```text
FOUNDING_CONTEST        1763..1789
FEDERAL_FORMATION       1787..1803
EXPANSION_AND_REMOVAL   1803..1854
SECTIONAL_RUPTURE       1854..1861
CIVIL_WAR               1861..1865
RECONSTRUCTION          1865..1877
POST_RECONSTRUCTION     1877..1954
CIVIL_RIGHTS_REORDERING 1954..1968
DIGITAL_STATE           1990..present
CIVIC_WAR               comparative layer only
```

Modules may be played individually or linked as a campaign.

## Card Classes

### History Card

Presents a dated event, record, institution, or dispute with verification status.

### Evidence Card

Represents a source or evidentiary method. Examples include enrolled acts, court records, newspapers, census records, correspondence, maps, photographs, testimony, datasets, hashes, and custody logs.

### Authority Card

Represents a claimed legal or civic authority:

```text
CONSTITUTIONAL_TEXT
AMENDMENT
FEDERAL_STATUTE
STATE_CONSTITUTION
STATE_STATUTE
EXECUTIVE_ACT
JUDICIAL_DECISION
ADMINISTRATIVE_RULE
MILITARY_ORDER
TREATY
ELECTION_RESULT
PUBLIC_PETITION
UNPROVEN_CLAIM
```

### Challenge Card

Tests provenance, jurisdiction, interpretation, custody, representation, due process, enforcement, or later review.

### Institution Card

Creates a temporary rule surface such as Congress, a court, state government, county office, newspaper, archive, election board, military command, civic organization, or digital platform.

## Example Turn

```text
ERA: RECONSTRUCTION
SPACE: US-SOUTH-CAROLINA
CLAIM: a state action is valid under claimed state authority
CHALLENGE: federal constitutional conflict
EVIDENCE: text of state action + federal amendment + court record
RESULT: CONTESTED
FORK: preserved
APPEAL_PATH: open
AUTHORITY: false until adjudicated inside the game procedure
```

## Safety and Historical Discipline

- The game does not convert interpretation into adjudication.
- Historical actors are not assigned guilt without cited evidence and procedural context.
- Missing evidence remains missing.
- Player victory does not establish historical truth.
- Game receipts establish only what occurred during play.
- Sensitive events should include educator notes and age guidance.
- Scenario cards must distinguish verified facts, attributed claims, interpretation, and fiction.

## Required JSON Artifacts

```text
CIVIC_WAR_GAME_SCHEMA_v0.1.json
CIVIC_WAR_CORE_DECK_v0.1.json
CIVIC_WAR_SESSION_RECEIPT_v0.1.json
```

Only the game schema is introduced in this commit. Historical deck population remains blocked pending source verification.

## Doctrine

```text
BYTE_EQUALITY      = INTEGRITY_ONLY
ROUTE_EXISTENCE    != AUTHORITY
DOCUMENT_EXISTENCE != TRUTH
INTERPRETATION     != ADJUDICATION
GAME_RESULT        != HISTORICAL_TRUTH
PLAYER_ROLE        != PUBLIC_AUTHORITY
CIVIC_PRESSURE     != LEGAL_VALIDITY
```

## State

```text
ARTIFACT                = CIVIC_WAR_BOARD_GAME_v0.1
PARENT                  = AMERICAN_HISTORY_3D_NAVIGATION_SCHEMA_v0.1
HISTORICAL_VERIFICATION = NOT_PERFORMED
CORE_DECK                = NOT_POPULATED
EXECUTION_AUTHORITY     = FALSE
AUTHORITY_EXPANSION     = FALSE
GATE_1                  = BLOCKED
PROMOTION               = BLOCKED
```
