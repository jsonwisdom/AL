# COACHES_CORNER_36092_MENU_GAME_V0_1

## Status

```text
LOCAL_DRAFT
MENU_SOURCE_PACKET_ACTIVE_USER_SUPPLIED
GOAL_LINE_REVIEW
NO_FAKE_GREEN_ACTIVE
```

## Place

```text
Name: Coaches Corner Sports Bar & Grill
Address: 203 Orline St, Wetumpka, AL 36092
Locality: Wetumpka, Alabama
Game Layer: Alabama Iron Bowl Menu Game
Operator: Jaywisdom.eth / jaywisdom.base.eth
```

## Booth Boundary

This artifact records a user-supplied menu source packet for game-layer replay.

Independent public web verification was not completed in this run.

Before this artifact can advance to `TOUCHDOWN_CONFIRMED`, it requires:

```text
official_menu_url_or_photo
fetched_at_utc
content_hash
source_notes
replay_operator
```

## Core Rule

```text
REAL_PLACE_GETS_REAL_CREDIT
MENU_GETS_NO_FAKE_ITEMS
SOURCE_PACKET_FIRST
BRAGGING_RIGHTS_AFTER_REPLAY
NO_FAKE_GREEN
```

## Menu Game Modes

### 1. Roll Tide Plate

Strongest entree.

```json
{
  "play_id": "ROLL_TIDE_PLATE_001",
  "primary_item": "Big Daddy Stuffed Burger",
  "price_user_supplied": "$12.49",
  "description_user_supplied": "Double patty stuffed with bacon and cheese, classic toppings.",
  "alternate_command_item": "Ribeye",
  "alternate_price_user_supplied": "$22.99",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "USER_SUPPLIED_OFFICIAL_SITE_PACKET_PENDING_HASH"
}
```

### 2. War Eagle Special

Chaos item.

```json
{
  "play_id": "WAR_EAGLE_SPECIAL_001",
  "primary_item": "Buffalo Wings",
  "description_user_supplied": "17 sauces including 911 and Boom Boom.",
  "alternate_item": "Fried Green Tomatoes",
  "alternate_price_user_supplied": "$3.99",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "USER_SUPPLIED_OFFICIAL_SITE_PACKET_PENDING_HASH"
}
```

### 3. Coach's Corner Combo

Main + side + drink.

```json
{
  "play_id": "COACHES_CORNER_COMBO_001",
  "main_item": "Mighty Fine Burger",
  "side_item": "Cheese Grits",
  "drink": "Fountain Drink",
  "estimated_range_user_supplied": "~$18 range",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "USER_SUPPLIED_OFFICIAL_SITE_PACKET_PENDING_HASH"
}
```

### 4. Fourth Quarter Snack

Fast field fuel.

```json
{
  "play_id": "FOURTH_QUARTER_SNACK_001",
  "primary_item": "Cheesy Fries with Bacon",
  "price_user_supplied": "$8.99",
  "alternate_item": "Popcorn Shrimp",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "USER_SUPPLIED_OFFICIAL_SITE_PACKET_PENDING_HASH"
}
```

## Daily Specials Lane

```json
{
  "daily_specials_user_supplied": [
    {
      "day": "Tuesday",
      "item": "Catfish",
      "field_state": "GOAL_LINE_REVIEW"
    },
    {
      "day": "Thursday",
      "item": "All-you-can-eat wings",
      "field_state": "GOAL_LINE_REVIEW"
    }
  ],
  "source_status": "USER_SUPPLIED_OFFICIAL_SITE_PACKET_PENDING_HASH"
}
```

## Local Reputation Layer

```json
{
  "local_reputation_user_supplied": [
    "real Alabama spot",
    "river view",
    "HGTV fame",
    "family vibe",
    "wings legend"
  ],
  "verification_state": "GOAL_LINE_REVIEW",
  "promotion_allowed": false
}
```

## Iron Bowl Field Logic

```text
PUNTED = no menu source
GOAL_LINE_REVIEW = menu source supplied, hash/public verification pending
TOUCHDOWN_CONFIRMED = official source or photo verified with hash
FLAG_ON_THE_PLAY = conflicting menu, unclear price, stale source, or broken lineage
NO_FAKE_GREEN = cannot promote
```

## Bragging Rights Payload Draft

```json
{
  "artifact": "COACHES_CORNER_36092_MENU_GAME_V0_1",
  "place": "Coaches Corner Sports Bar & Grill",
  "locality": "Wetumpka, AL 36092",
  "credit_to": "Coaches Corner Sports Bar & Grill",
  "replay_operator": "jaywisdom.eth",
  "base_identity": "jaywisdom.base.eth",
  "menu_verified": false,
  "field_state": "GOAL_LINE_REVIEW",
  "authority": false,
  "no_fake_green": true
}
```

## Family Gate

Family Gate remains table rule #1.

```text
Family safety, privacy, consent, and repair outrank every artifact, token, claim, dashboard, game, and menu replay.
```

## Required Next Receipt

```text
MENU_SOURCE_PACKET_VERIFIED
```

Required payload:

```json
{
  "official_menu_url_or_photo": "required",
  "fetched_at_utc": "required",
  "content_hash": "required",
  "verified_items": [
    "Big Daddy Stuffed Burger",
    "Ribeye",
    "Buffalo Wings",
    "Fried Green Tomatoes",
    "Mighty Fine Burger",
    "Cheese Grits",
    "Fountain Drink",
    "Cheesy Fries with Bacon",
    "Popcorn Shrimp"
  ],
  "verified_status": "required"
}
```

## Closing Receipt

Coaches Corner 36092 Menu Game opened.

Menu packet active from user-supplied official-site claim.

Independent public verification pending.

Game is live.

No fake green.

Roll Tide.

JAYWISDOM.eth 🏈⚙️
