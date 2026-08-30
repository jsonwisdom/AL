# Bandwidth Schedule v0.1-θ

**Parent:** `PEDAGOGICAL_MEDIA_MODES_v0.1-theta`  
**Classification:** Session scheduling & bandwidth allocation (simulation only)  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Vessel status:** EMPTY_VESSEL  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Define when shared simulation bandwidth is reserved for Governor / operational use versus when it is released to the public for entertainment and pedagogical media modes (cold cases, reenactments, learning video, teaching props, 80s RePlay, JSON movie streams).

```text
GOVERNOR_BANDWIDTH     = PRIORITY_WINDOW
PUBLIC_ENTERTAINMENT   = WHEN_GOVERNORS_NOT_USING
EVERYTHING_ELSE        = GAME_ON
SCHEDULE               ≠ AUTHORITY
SCHEDULE               ≠ GATE_1_OPEN
SCHEDULE               ≠ SOURCE_ADMISSION
```

## 2. Named Window

```text
PRIORITY_WINDOW = 08:00 – 16:00  (session-local clock, inclusive start / exclusive end unless otherwise posted)
```

During the priority window, Governor and operational sessions (gate review, admission work, steward process, CI/harness) take precedence if declared active.

When no Governor session holds the bandwidth during that window — or outside the window entirely — bandwidth is available for public entertainment and pedagogical media.

## 3. Allocation Rules

| Clock | Default posture |
|-------|-----------------|
| **08:00 – 16:00** | Governor priority if a Governor session is active; otherwise public entertainment may use the channel |
| **All other hours** | **Game ON** — public entertainment and pedagogical media modes fully open |

“Game ON” means the modes defined in `PEDAGOGICAL_MEDIA_MODES_v0.1-theta` (cold cases, reenactments, learning videos, teaching props, 80s RePlay, JSON streaming) may run without waiting for Governor release, subject to ordinary fail-closed rules.

## 4. Non-Interference

- Schedule does not open Gate 1.
- Schedule does not admit primary sources or assign mass.
- Schedule does not merge roles or weaken Separation of Duties.
- Schedule does not create public office or historical truth.
- A public entertainment session never outranks an explicitly declared active Governor session inside the priority window.

## 5. Declaration of Hold

A Governor session that needs the priority window SHOULD emit a short receipt or session notice:

```text
BANDWIDTH_HOLD
window: 08:00–16:00 (or sub-interval)
authority: false
gate_1: BLOCKED
```

Absent an active hold, the public may treat the channel as free for entertainment even inside 08:00–16:00.

## 6. Labels

Public sessions remain labeled:

```text
ENTERTAINMENT_ONLY  |  PEDAGOGICAL_ONLY
SIMULATION_ONLY
AUTHORITY = FALSE
GATE_1 = BLOCKED
```

## 7. Current State

```text
ARTIFACT              = BANDWIDTH_SCHEDULE_v0.1-theta
PRIORITY_WINDOW       = 08:00–16:00
PUBLIC_DEFAULT        = WHEN_GOVERNORS_NOT_USING
OFF_WINDOW            = GAME_ON
GATE_1                = BLOCKED
VESSEL_STATUS         = EMPTY_VESSEL
AUTHORITY             = FALSE
CORE_DOCKET           = EMPTY
PROMOTION             = BLOCKED
```

## 8. Promotion Boundary

This schedule is a simulation convenience. It does not bind real-world infrastructure, legal bandwidth, or any public network. It only orders attention inside the pedagogical substrate.

😎
