# AL COURTS REPLAY PROTOCOL V0.1

**Source repo:** jsonwisdom/AL  
**Related safety inheritance:** jsonwisdom/JOY  
**Operator identity:** Jason Wisdom / jaywisdom.eth / jaywisdom.base.eth  
**Status:** Draft-ready  
**Authority:** false  
**Membrane:** HOLDS

## Purpose

Open the three court surfaces at replay level inside AL.

This protocol does not adjudicate truth, guilt, legality, politics, or official authority. It creates replay-safe surfaces for observing drift, blockers, custody gaps, narrative inflation, and receipt formation.

## Court Surfaces

### 1. Meme Court

**Role:** Public signal surface.  
**Function:** Turn public claims, cultural signals, memes, and attention events into observable replay packets.

Allowed actions:

- observe
- log
- timestamp
- hash
- summarize
- preserve source
- produce receipt packet

Forbidden actions:

- adjudicate truth
- assign guilt
- imply official authority
- promote visibility into verification

### 2. Goblin Court

**Role:** Bureaucracy and infrastructure blocker surface.  
**Function:** Expose PDFs, process friction, broken links, custody gaps, infrastructure blockers, and receipt failures without accusation.

Allowed actions:

- identify blocker class
- preserve document/source metadata
- record missing fields
- produce replay packet
- route to ALMS validation

Forbidden actions:

- call absence fraud
- convert blocker into legal conclusion
- mutate custody
- invent missing values

### 3. Clown Court

**Role:** Authority-drift surface.  
**Function:** Detect badge cosplay, narrative inflation, category promotion, and judgment-like language before it contaminates the replay path.

Allowed actions:

- flag category drift
- classify posture
- record authority boundary
- preserve disputed state
- route escalation when needed

Forbidden actions:

- shame individuals
- impersonate officials
- issue verdicts
- upgrade claim to verified receipt silently

## Three Daughters Algorithm

The three daughters algorithm is applied as a protective ordering rule, not as public identity exposure.

1. Protect the daughters and family custody first.
2. Preserve replay continuity second.
3. Expand public systems third.

```json
{
  "three_daughters_algorithm": {
    "priority_1": "protect_family_identity_and_custody",
    "priority_2": "preserve_replay_continuity",
    "priority_3": "expand_public_systems_only_after_receipts",
    "barrier_state": "FULL_INTEGRITY",
    "public_identity_exposure": "MINIMIZED"
  },
  "authority": false
}
```

## 3 / 6 / 9 Replay Mapping

This mapping is structural, not mystical authority.

```json
{
  "3": "three courts",
  "6": "six replay states",
  "9": "nine machine-speed surfaces",
  "six_replay_states": [
    "OBSERVATION",
    "CLAIM",
    "RECEIPT",
    "VERIFIED_RECEIPT",
    "DECISION",
    "ARCHIVE"
  ],
  "nine_machine_speed_surfaces": [
    "voice",
    "transcript",
    "hash",
    "json",
    "html",
    "pull_request",
    "commit",
    "replay_page",
    "attestation"
  ]
}
```

## ALMS Routing Rule

Every court output must route into ALMS as one of the replay states.

```txt
court observation -> replay state -> receipt packet -> validation gate -> replay page -> archive
```

No court may bypass ALMS.

## Wisdom Rule

Truth can be tested, not asserted.

Receipts beat narrative.  
Unknowns stay unknown.  
Claims stay claims until evidence is attached.  
Verification requires independent validation.  
Authority remains false unless separately and explicitly granted by a qualified external process.

## Machine-Speed Readiness

A court replay packet is machine-ready only when it includes:

- court name
- replay state
- source URL or source description
- observed_at timestamp
- operator or agent identifier
- sha256 when a file exists
- file name when a file exists
- byte size when a file exists
- authority:false
- membrane:HOLDS
- privacy boundary
- promotion history

## Final Line

Three courts open the replay path.  
ALMS preserves the path.  
Wisdom prevents authority drift.  
JOY protects the family layer.
