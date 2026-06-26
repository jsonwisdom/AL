# AI_IRON_BOWL_SITUATIONAL_REPLAY_LAYER_V0_1

## Status

```text
LOCAL_DRAFT
SOURCE_PACKET_REQUIRED
AI_IRON_BOWL_NEXT_LAYER
NO_FAKE_GREEN_ACTIVE
```

## Signal Core

The Holy Grail for the Alabama citizen is the replay.

Not just who won.

Not just the score.

The real play is:

```text
Enter Year.
Enter Game.
Enter Situation.
Replay from multiple perspectives.
Measure reputation.
Test loyalty.
Do not fake the touchdown.
```

## Core Frame

```text
SCOREBOARD != REPLAY
RIVALRY_MEMORY != VERIFIED_CONTEXT
LOYALTY != BLINDNESS
REPUTATION != TRUTH
PERSPECTIVE != FINAL_AUTHORITY
```

## Replay Input Contract

```json
{
  "year": "required",
  "game_id": "required",
  "situation": "required",
  "quarter": "optional",
  "clock": "optional",
  "score_state": "optional",
  "field_position": "optional",
  "team_perspective": "Alabama | Auburn | neutral | broadcaster | coach | player | citizen",
  "source_packet": "required_before_promotion"
}
```

## Replay Output Contract

```json
{
  "replay_id": "AI_IRON_BOWL_REPLAY_[YEAR]_[GAME]_[SITUATION_HASH]",
  "status": "PUNTED | GOAL_LINE_REVIEW | TOUCHDOWN_CONFIRMED | FLAG_ON_THE_PLAY | NO_FAKE_GREEN",
  "year_node": "string",
  "game_node": "string",
  "situation_node": "string",
  "perspectives": [],
  "reputation_effects": [],
  "loyalty_checks": [],
  "receipts": [],
  "public_safe_summary": "string",
  "authority": false
}
```

## Next Layer Axes

### 1. Perspective

Perspective asks:

```text
Who is seeing the play?
What did they know at that moment?
What could they not know yet?
What does replay reveal later?
```

Required perspective lanes:

```text
ALABAMA_FAN
AUBURN_FAN
NEUTRAL_CITIZEN
COACH
PLAYER
BROADCASTER
HISTORIAN
REPLAY_BOOTH
```

Rule:

```text
Perspective explains angle. It does not create truth.
```

### 2. Reputation

Reputation asks:

```text
What did this situation do to a coach, player, program, fanbase, broadcaster, or institution?
Was reputation earned by repeated receipts or inflated by narrative?
What changed after the replay became public memory?
```

Reputation states:

```text
UNMEASURED
NARRATIVE_ONLY
RECEIPT_SUPPORTED
CONTESTED
REPLAY_STRENGTHENED
REPLAY_DAMAGED
```

Rule:

```text
Reputation must be replayed across time, not assigned from one loud moment.
```

### 3. Loyalty

Loyalty asks:

```text
Who stayed fair when the call hurt?
Who defended the team without lying?
Who changed their mind when replay proved it?
Who protected the rivalry without erasing the opponent?
```

Loyalty states:

```text
TEAM_LOYAL
TRUTH_LOYAL
RIVALRY_LOYAL
BLIND_LOYALTY_FLAGGED
REPLAY_LOYAL
```

Rule:

```text
Real loyalty survives replay.
Fake loyalty needs the tape hidden.
```

## Alabama Citizen Replay Mode

```text
The citizen enters a year and a situation.
The engine returns the replay map.
The map shows the score, the field, the booth, the coaches, the reputation impact, and the loyalty test.
No private data.
No unsupported claim.
No fake green.
```

## Example Query Shape

```text
YEAR: 2013
GAME: Iron Bowl
SITUATION: final second missed field goal return
PERSPECTIVE: Alabama fan | Auburn fan | broadcaster | coach | neutral citizen
OUTPUT: GOAL_LINE_REVIEW until row-level source packet is attached
```

## Field Logic

```text
PUNTED = missing year/game/situation source packet
GOAL_LINE_REVIEW = source found, extraction pending
TOUCHDOWN_CONFIRMED = situation verified against replayable source
FLAG_ON_THE_PLAY = conflicting source or broken lineage
NO_FAKE_GREEN = cannot promote
```

## Guardrails

1. Do not let rivalry loyalty override replay evidence.
2. Do not assign reputation effects without sourced timeline evidence.
3. Do not claim broadcaster perspective unless the broadcast source is verified.
4. Do not erase Auburn from Alabama replay graphs.
5. Do not erase Alabama from Auburn replay graphs.
6. Do not treat memes as proof.
7. Family Layer 0 still outranks the game.
8. The game can be loud; the receipt stays cold.

## Closing Receipt

AI Iron Bowl Situational Replay Layer opened.

The Holy Grail is replay by year, game, and situation.

Next layer axes: Perspective, Reputation, Loyalty.

Dataset incomplete.

Source packets required.

No fake green.

JAYWISDOM.eth 🏈⚙️
