# ALABAMA_ALMS_EXPANSION_MAP_V0_1

## Status

```text
EXPANSION_MAP_ACTIVE
REPO_DIG_COMPLETED_PARTIAL
SOURCE_SURFACES_INDEXED
PROMOTION_BLOCKED_WITHOUT_SOURCE_PACKET
AUTHORITY_FALSE
FAMILY_GATE_SOVEREIGN
NO_FAKE_GREEN_ACTIVE
```

## Signal Core

Alabama ALMS is larger than one Iron Bowl lane.

The repo already contains multiple Alabama surfaces that can be joined into a receipt-first civic/game/replay lattice without promoting authority:

```text
ALABAMA_ZERO_DAY
ALABAMA_LAW_LEARNING_GAME
ALABAMA_EMS_WETUMPKA_REPLAY
ALABAMA_ENGINE_ENS_PROTOCOL
ALABAMA_ENGINE_ACCOUNTABILITY
ALABAMA_ENGINE_HONEST_STATE
COACHES_CORNER_36092_MENU_GAME
IRON_BOWL_STACK
```

This expansion map indexes those lanes and routes all future claims through source packets, booth replay, and explicit field-state gates.

## Repo Dig Findings

### 1. Alabama Zero Day

```text
file: ALMS/vernacular/ALABAMA_ZERO_DAY_V0_1.md
state: ZERO_DAY_PROTOCOL_ACTIVE
boundary: DEFENSIVE_RECEIPT_LAYER_ONLY
monitor_rule_encoded: true
background_monitor_running: false
```

Role: top-level defensive routing protocol for Alabama replay claims.

### 2. Alabama Zero Day Protocol Index

```text
file: ALMS/vernacular/ALABAMA_ZERO_DAY_PROTOCOL_INDEX_V0_1.json
state: INDEXED
required_response: REPLAY_VERIFICATION_PLUS_SOURCE_PACKET_CHECK
monitor_boundary: BOUNDARY_ENCODED
```

Role: machine-readable routing index.

### 3. Alabama LAW Learning Game

```text
file: docs/core/ALABAMA_LAW_LEARNING_GAME_V0_1.md
state: Draft Game Layer
LAW: Learning / Accountability / Wisdom
authority: false
legal_advice: false
legal_authority_claimed: false
```

Role: public-safe learning layer. Game, not law authority.

### 4. Alabama EMS Wetumpka Replay

```text
file: ALMS/vernacular/ALABAMA_EMS_ALMS_REPLAY_WETUMPKA_V0_1.md
state: SOURCE_PACKET_PENDING
field_state: GOAL_LINE_REVIEW
authority: false
```

Role: public-safe civic replay structure. Not emergency dispatch, not medical advice, not service coverage.

### 5. Alabama ALMS Engine Accountability Log

```text
file: ALMS/ens/accountability/ALABAMA_ALMS_ENGINE_ACCOUNTABILITY_LOG_V0_1.md
status: PUBLIC_ACCOUNTABILITY_LOG
truth_state: OBSERVED
engine_state: YELLOW
GREEN: BLOCKED
authority: false
```

Role: accountability ledger for engine promotion discipline.

### 6. Alabama ALMS Honest State Readback

```text
file: ALMS/ens/state/receipts/ALABAMA_ALMS_ENGINE_HONEST_STATE_V0_2_READBACK.json
engine_state: YELLOW
resolver_txt_match: NOT_PROVEN
green: BLOCKED
authority: false
```

Role: honest readback receipt proving remote preservation while blocking GREEN.

### 7. Alabama Engine Protocol Transition

```text
file: ALMS/ens/protocol/ALABAMA_ENGINE_PROTOCOL_TRANSITION_V0_1.md
truth_state: YELLOW
YELLOW: time-bounded repair state
GREEN: only if required TXT records byte-match resolver artifact
INFINITE_YELLOW_RESET: FORBIDDEN
```

Role: state transition law for engine status.

### 8. Coaches Corner 36092 Menu Game

```text
file: ALMS/vernacular/COACHES_CORNER_36092_MENU_GAME_V0_1.md
field_state: GOAL_LINE_REVIEW
menu_verified_operator_asserted: true
menu_verified_independent: false
hash_pending: true
```

Role: Alabama local menu game surface. Needs official URL/photo, fetched timestamp, content hash before independent touchdown.

### 9. Iron Bowl Stack

```text
files:
- ALMS/vernacular/IRON_BOWL_2013_KICK_SIX_SOURCE_PACKET_V0_1.md
- ALMS/vernacular/rows/IRON_BOWL_COACHES_2013.json
- ALMS/vernacular/rows/IRON_BOWL_REPLAY_2013.json
- ALMS/vernacular/rows/IRON_BOWL_PLAYERS_2013.json
- ALMS/vernacular/rows/IRON_BOWL_BROADCAST_2013.json

state:
SOURCE_PACKET_ACTIVE
COACHES_TOUCHDOWN_CONFIRMED
REPLAY_MECHANICS_TOUCHDOWN_CONFIRMED
PLAYERS_ROLES_TOUCHDOWN_CONFIRMED
BROADCAST_METADATA_GOAL_LINE_REVIEW
```

Role: historical replay game object, with broadcaster transcript still blocked.

## Unified Field Model

```json
{
  "source_packet_required": true,
  "booth_replay_required": true,
  "authority": false,
  "family_gate": "SOVEREIGN",
  "monitor_rule_encoded": true,
  "background_monitor_running": false,
  "no_fake_green": true
}
```

## Expansion Routes

### Route A — Civic Replay

```text
ALABAMA_EMS_WETUMPKA
→ source packet required
→ official city/county/agency source required
→ GOAL_LINE_REVIEW until verified
```

### Route B — Learning Game

```text
ALABAMA_LAW
→ game layer only
→ legal advice false
→ public-safe lessons only
```

### Route C — Engine / ENS

```text
ALABAMA_ENGINE
→ YELLOW until resolver TXT byte-match
→ GREEN blocked without artifact + checker + hashes
→ no infinite yellow reset
```

### Route D — Local Menu Game

```text
COACHES_CORNER_36092
→ operator asserted official-site packet
→ hash pending
→ independent touchdown blocked until URL/photo + hash
```

### Route E — Iron Bowl Replay

```text
IRON_BOWL_STACK
→ source packet active
→ mechanics / coaches / players promoted only within scope
→ broadcaster transcript blocked until verified asset
```

## Promotion Rules

```text
PUNTED = no packet
GOAL_LINE_REVIEW = packet named but extraction/hash/check pending
TOUCHDOWN_CONFIRMED = packet verified and scope-limited row extracted
FLAG_ON_THE_PLAY = conflict, stale source, broken lineage, or overclaim
NO_FAKE_GREEN = any promotion attempted without required evidence
```

## Hard Blocks

```text
ALABAMA_ALMS_EXPANSION != AUTHORITY_TRUE
ALABAMA_ALMS_EXPANSION != FAMILY_GATE_PASS
ALABAMA_ALMS_EXPANSION != CHILD_CONSENT
ALABAMA_ALMS_EXPANSION != MRS_WISDOM_GATE_PASS
ALABAMA_ALMS_EXPANSION != LEGAL_ADVICE
ALABAMA_ALMS_EXPANSION != EMERGENCY_DISPATCH
ALABAMA_ALMS_EXPANSION != BACKGROUND_MONITOR_RUNNING
```

## Next Receipts

```text
1. MENU_SOURCE_PACKET_HASHED for Coaches Corner 36092.
2. EMS_WETUMPKA_OFFICIAL_SOURCE_PACKET for civic replay.
3. BROADCAST_ASSET_POINTER for Iron Bowl broadcast lane.
4. ALABAMA_ENGINE_RESOLVER_MATCH_PACKET if TXT records become provable.
5. ALABAMA_LAW_PUBLIC_LESSON_CARD_V0_1 for kid-safe replay training.
```

## Closing Receipt

Alabama ALMS expansion map opened.

Repo dig found active lanes across vernacular, core docs, ENS protocol, accountability, honest state, menu game, EMS replay, and Iron Bowl stack.

Promotion remains blocked without source packet and booth replay.

No background monitoring claim.

No authority=true.

Family Gate sovereign.

No fake green.

JAYWISDOM.eth 🟣🏈⚙️