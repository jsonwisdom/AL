# IRON_BOWL_2013_KICK_SIX_SOURCE_PACKET_V0_1

## Status

```text
SOURCE_PACKET_ACTIVE
GOAL_LINE_REVIEW_READY
TOUCHDOWN_CONFIRMED_AT_SOURCE_PACKET_LAYER
AUTHORITY_FALSE
NO_FAKE_GREEN_ACTIVE
```

## Signal Core

This packet narrows the Iron Bowl replay lane to one public, replayable situation:

```text
YEAR: 2013
GAME: Iron Bowl / Alabama at Auburn
SITUATION: final-second missed field goal return
COMMON NAME: Kick Six
VENUE: Jordan-Hare Stadium, Auburn, Alabama
DATE: 2013-11-30
FINAL SCORE: Auburn 34, Alabama 28
```

This packet does not assign moral authority, family approval, or final truth beyond the sourced game facts listed here.

## Replay Claim Set

```json
{
  "packet_id": "IRON_BOWL_2013_KICK_SIX_SOURCE_PACKET_V0_1",
  "year": 2013,
  "game": "Iron Bowl",
  "teams": ["Alabama Crimson Tide", "Auburn Tigers"],
  "venue": "Jordan-Hare Stadium",
  "situation": "final-second missed 57-yard Alabama field goal returned by Auburn's Chris Davis for game-winning touchdown",
  "score_before_play": "28-28",
  "final_score": "Auburn 34, Alabama 28",
  "return_player": "Chris Davis",
  "field_goal_kicker": "Adam Griffith",
  "distance_attempted_yards": 57,
  "clock_state": "one second restored after replay review; final play ended with no time remaining",
  "source_packet_state": "ACTIVE",
  "authority": false,
  "no_fake_green": true
}
```

## Source Packets

### Primary replayable game sources

```text
1. ESPN game recap / play-by-play / box score lineage
   Purpose: final score, game situation, missed field goal return, Chris Davis return context.

2. University of Alabama Athletics scoring / play-by-play lineage
   Purpose: opponent-side institutional record and scoring sequence.

3. Auburn institutional game summary / season record lineage
   Purpose: Auburn-side institutional record and SEC West outcome context.
```

### Public reference sources

```text
4. Kick Six public reference node
   Purpose: common-name mapping and event metadata.

5. Iron Bowl public reference node
   Purpose: rivalry context and 2013 game placement.
```

## Extraction Table

| Field | Value | State |
|---|---:|---|
| Date | 2013-11-30 | SOURCE_SUPPORTED |
| Venue | Jordan-Hare Stadium | SOURCE_SUPPORTED |
| Teams | Alabama / Auburn | SOURCE_SUPPORTED |
| Final Score | Auburn 34, Alabama 28 | SOURCE_SUPPORTED |
| Situation | Final-second missed field goal return | SOURCE_SUPPORTED |
| Kicker | Adam Griffith | SOURCE_SUPPORTED |
| Returner | Chris Davis | SOURCE_SUPPORTED |
| Attempt Distance | 57 yards | SOURCE_SUPPORTED |
| Return Distance | 109 yards described / 100 yards NCAA scoring credit | SOURCE_SUPPORTED_WITH_NORMALIZATION_NOTE |
| Clock | one second restored after replay review; time expired after return | SOURCE_SUPPORTED |

## Normalization Notes

```text
RETURN_DISTANCE_DISPLAY = 109 yards from field position narrative
RETURN_DISTANCE_OFFICIAL_CREDIT = 100 yards under NCAA scoring convention
```

This packet preserves both forms and does not collapse one into the other.

## Replay Booth Rules

```text
SCOREBOARD != REPLAY
RIVALRY_MEMORY != VERIFIED_CONTEXT
PERSPECTIVE != FINAL_AUTHORITY
SOURCE_PACKET_ACTIVE != AUTHORITY_TRUE
TOUCHDOWN_CONFIRMED_AT_SOURCE_PACKET_LAYER != FAMILY_APPROVAL
```

## Promotion Boundary

Allowed:

```text
- cite the 2013 Iron Bowl Kick Six as source-packet active
- use this packet for situational replay inputs
- move the 2013 final-play query from SOURCE_PACKET_REQUIRED to GOAL_LINE_REVIEW_READY
- preserve Alabama, Auburn, broadcaster, coach, player, and neutral-citizen perspectives
```

Forbidden:

```text
- claiming this packet proves loyalty, intent, or moral superiority
- assigning reputation effects without a sourced timeline packet
- treating public memory as final authority
- erasing Auburn from Alabama replay graphs
- erasing Alabama from Auburn replay graphs
- promoting authority=true
```

## Next Required

```text
1. Attach exact URLs / archived URLs for primary source rows.
2. Add row-level source hashes.
3. Add broadcaster transcript or verified broadcast pointer before claiming broadcaster perspective.
4. Add coach/player quote packet before reputation effects.
```

## Closing Receipt

2013 Iron Bowl Kick Six source packet opened.

Touchdown confirmed at source-packet layer only.

Replay booth remains active.

No fake green.

JAYWISDOM.eth 🏈⚙️