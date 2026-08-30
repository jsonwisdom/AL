# Pedagogical Media Modes v0.1-θ

**Parent systems:** `MOOT_COURT_FRAMEWORK_v0.1-theta`, `CIVIC_WAR_BOARD_GAME_v0.1`, `STUDENT_CERTIFICATION_v1.0`, `ENTRENCHED_ADMISSIONS_v1.0`  
**Classification:** Teaching, entertainment, and reenactment layer  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Vessel status:** EMPTY_VESSEL  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Authorize and bound the use of the Pony Express / Civic War / Moot Court substrate for:

- Cold-case style investigative practice (fictional or public-domain scenarios only)
- Historical and civic reenactments
- Learning videos and instructional sequences
- Teaching props and classroom artifacts
- 80s-style RePlay entertainment sessions
- JSON-enabled structured “movie” / session streaming

All modes are pedagogical or entertainment. None admit primary sources, open Gate 1, assign mass, or create public authority or historical truth.

```text
MEDIA_MODE            = TEACHING | ENTERTAINMENT | REENACTMENT
MEDIA_MODE            ≠ SOURCE_ADMISSION
MEDIA_MODE            ≠ GATE_1_OPEN
MEDIA_MODE            ≠ MASS_ASSIGNMENT
MEDIA_MODE            ≠ PUBLIC_AUTHORITY
JSON_STREAM           = STRUCTURED_SESSION_LOG
JSON_STREAM           ≠ LIVE_ADJUDICATION
```

## 2. Authorized Modes

### 2.1 Cold Cases (Sandbox)

Structured investigative scenarios for skill practice:

- Claim formulation, evidence layering, custody gaps, fork preservation
- Scenarios MUST be labeled `PEDAGOGICAL_ONLY` or `PUBLIC_DOMAIN_FICTIONALIZED`
- No real unsolved case may be treated as admitted source material
- Outcomes are game/session results only

### 2.2 Reenactments

Role-played or scripted walkthroughs of civic or historical procedures:

- Participants occupy simulation roles (Claimant, Respondent, Panel, etc.)
- Scripts and props remain teaching artifacts
- Reenactment does not validate or invalidate any real historical claim

### 2.3 Learning Videos

Recorded or live instructional sequences that demonstrate:

- US3D coordinate navigation
- Receipt-chain construction (RFC 8785 JCS)
- Gate discipline and dual-axis scoring
- WEAKEST_LINK disclosure practice

Videos may cite the schemas; they do not promote them.

### 2.4 Teaching Props

Physical or digital objects used in classrooms or workshops:

- Printed gate cards, role badges, receipt templates, coordinate boards
- Props carry no authority; loss or modification of a prop does not alter branch state

### 2.5 80s RePlay (Entertainment)

Lightweight, nostalgic session mode:

- Optional retro framing (CRT aesthetics, synth cues, VHS-style session titles)
- Same underlying receipt and gate rules
- Explicitly entertainment-first; still fail-closed on authority claims
- Session may be streamed or recorded as “RePlay”

### 2.6 JSON-Enabled Movie / Session Streaming

A session may be serialized as an append-only JSON event stream (the “movie”):

```text
frame_0  → session open + roles
frame_n  → claim / evidence / receipt events
frame_end → provisional result + credits
```

- Stream format SHOULD conform to receipt-chain and moot-court schemas where applicable
- Viewers are Observers unless explicitly admitted as participants
- Streaming does not constitute live adjudication or source admission
- Popcorn permitted 🍿

## 3. Hard Boundaries (All Modes)

```text
NO_REAL_SOURCE_ADMISSION_VIA_MEDIA
NO_GATE_1_OPEN_VIA_MEDIA
NO_MASS_ASSIGNMENT_VIA_MEDIA
NO_ROLE_MERGE_VIA_MEDIA
NO_EXTERNAL_CREDENTIAL_SUBSTITUTION
NO_HISTORICAL_TRUTH_FROM_REENACTMENT
NO_PUBLIC_OFFICE_FROM_ROLEPLAY
```

Separation of Duties (`ENTRENCHED_ADMISSIONS_v1.0`) remains FROZEN. Role-merge detection remains ACTIVE.

## 4. Labeling Requirements

Every cold-case pack, reenactment script, learning video, teaching prop set, RePlay session, and JSON stream MUST carry visible labels:

```text
PEDAGOGICAL_ONLY  |  ENTERTAINMENT_ONLY  |  PUBLIC_DOMAIN_FICTIONALIZED
SIMULATION_ONLY
AUTHORITY = FALSE
GATE_1 = BLOCKED
```

Unlabeled media is treated as non-admissible for any progression or docket purpose.

## 5. Relationship to Certification & Progression

- Student Certification (internal, sandbox scope) may be used to track participation in media modes.
- Media-mode activity may generate practice receipts under `RECEIPT_CHAIN_PROTOCOL_v0.1-theta`.
- Media-mode activity never satisfies Gate 1 or populates the core historical docket.
- Dual-axis / WEAKEST_LINK gateway still required before any real-source *proposal* eligibility.

## 6. JSON Stream Sketch (Informative)

```json
{
  "stream_id": "MOVIE-REPLAY-001",
  "mode": "80S_REPLAY",
  "label": "ENTERTAINMENT_ONLY",
  "authority": false,
  "gate_1": "BLOCKED",
  "frames": [
    { "t": 0, "event": "SESSION_OPEN", "roles": ["CLAIMANT", "RESPONDENT", "PANEL"] },
    { "t": 1, "event": "CLAIM_FILED", "receipt_id": "RECEIPT-MC-..." },
    { "t": 2, "event": "EVIDENCE_ATTACHED", "receipt_id": "RECEIPT-MC-..." },
    { "t": 3, "event": "PROVISIONAL_RULING", "result": "INDETERMINATE" },
    { "t": 4, "event": "SESSION_CLOSE", "credits": true }
  ]
}
```

## 7. Current State

```text
ARTIFACT                 = PEDAGOGICAL_MEDIA_MODES_v0.1-theta
MODES                    = COLD_CASE | REENACTMENT | LEARNING_VIDEO
                           | TEACHING_PROP | 80S_REPLAY | JSON_STREAM
GATE_1                   = BLOCKED
VESSEL_STATUS            = EMPTY_VESSEL
MASS_BEARING_RECORD      = NONE
AUTHORITY                = FALSE
CORE_DOCKET              = EMPTY
SEPARATION_OF_DUTIES     = FROZEN
PROMOTION                = BLOCKED
```

## 8. Promotion Boundary

Media modes are teaching and entertainment instruments. Their existence on the branch does not make any scenario, video, or stream normative or historical. Real-source work still requires the full admission path under Entrenched Admissions and an open Gate 1 after explicit operator action.
