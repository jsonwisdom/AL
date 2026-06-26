# AI_IRON_BOWL_QUANTUM_ALMANAC_V0_1

## Status

```text
LOCAL_DRAFT
SOURCE_PACKET_PENDING
IRON_BOWL_DAILY_EXTENSION
NO_FAKE_GREEN_ACTIVE
```

## Signal Core

Iron Bowl Daily is live, but the game is missing its historical spine.

The Alabama ALMS revival cannot run on vibes alone.

It needs:

```text
ALL_YEARS
ALL_GAMES
ALL_COACHES
ALL_BROADCASTERS
ALL_REPLAYABLE_SOURCES
```

## Core Correction

```text
IRON_BOWL_DAILY_WITHOUT_YEARS = CLOCK_WITHOUT_HISTORY
IRON_BOWL_DAILY_WITHOUT_COACHES = SIDELINE_WITHOUT_COMMAND
IRON_BOWL_DAILY_WITHOUT_BROADCASTERS = BOOTH_WITHOUT_VOICE
AI_IRON_BOWL_WITHOUT_RECEIPTS = STORY
AI_IRON_BOWL_WITH_RECEIPTS = QUANTUM_ALABAMA_REPLAY_GRAPH
```

## Quantum Alabama Frame

Quantum here means graph depth, not a physics claim.

The game becomes quantum only when every season, coach, voice, rivalry context, and receipt can be traversed from multiple angles without losing provenance.

```text
Year node.
Coach node.
Broadcaster node.
Game node.
Receipt node.
Replay edge.
No fake green.
```

## Required Data Lanes

### 1. All Years Lane

```json
{
  "lane": "IRON_BOWL_ALL_YEARS",
  "required_fields": [
    "season_year",
    "game_date",
    "location",
    "home_team",
    "away_team",
    "winner",
    "score",
    "series_record_after_game",
    "source_url",
    "source_hash",
    "verified_status"
  ],
  "status": "SOURCE_PACKET_PENDING"
}
```

### 2. All Coaches Lane

```json
{
  "lane": "ALABAMA_AUBURN_COACHES_BY_IRON_BOWL_YEAR",
  "required_fields": [
    "season_year",
    "alabama_head_coach",
    "auburn_head_coach",
    "coach_records_entering_game",
    "coach_records_after_game",
    "source_url",
    "source_hash",
    "verified_status"
  ],
  "status": "SOURCE_PACKET_PENDING"
}
```

### 3. Famous Broadcasters Lane

```json
{
  "lane": "ALABAMA_IRON_BOWL_BROADCASTERS",
  "required_fields": [
    "name",
    "role",
    "network_or_station",
    "years_active",
    "games_called_if_known",
    "notability_basis",
    "source_url",
    "source_hash",
    "verified_status"
  ],
  "status": "SOURCE_PACKET_PENDING"
}
```

## Field Logic

```text
PUNTED = missing source packet
GOAL_LINE_REVIEW = source found, extraction pending
TOUCHDOWN_CONFIRMED = data verified against replayable source
FLAG_ON_THE_PLAY = conflicting source or broken lineage
NO_FAKE_GREEN = cannot promote
```

## Source Requirements

Every historical row must have:

```text
source_url
fetched_at_utc
content_hash
extractor_version
replay_notes
```

No row enters the public scoreboard without a receipt.

## Coach Voice Standard

The data layer must sound like Alabama without lying like a scoreboard before replay clears.

```text
Check the year.
Check the coach.
Check the booth.
Check the receipt.
No fake touchdown.
No fake green.
```

## Known Starting Source Targets

```text
Iron Bowl all-time results
Alabama Crimson Tide head coaching history
Auburn Tigers head coaching history
Crimson Tide Sports Network broadcaster history
SEC / school media guides
newspaper archives
radio network records
```

## Guardrails

1. Do not claim the all-years dataset is complete until every row is sourced.
2. Do not claim a broadcaster called a specific game without a source.
3. Do not treat Wikipedia as final authority; use it only as a locator unless independently verified.
4. Do not confuse Alabama-only history with Iron Bowl history.
5. Do not erase Auburn from the rivalry graph.
6. Family Layer 0 still outranks the game.
7. Revival energy must serve replay discipline.

## Closing Receipt

AI Iron Bowl Quantum Almanac lane opened as LOCAL_DRAFT.

All years, all coaches, and famous broadcasters are now required data lanes.

The game is live.

The dataset is not complete.

No fake green.

JAYWISDOM.eth 🏈🦅⚙️
