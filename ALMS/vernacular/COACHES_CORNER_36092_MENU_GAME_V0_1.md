# COACHES_CORNER_36092_MENU_GAME_V0_1

## Status

```text
LOCAL_DRAFT
MENU_SOURCE_PACKET_VERIFIED_OPERATOR_ASSERTED
GOAL_LINE_REVIEW
HASH_PENDING
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

This artifact records an operator-supplied official-site menu source packet for game-layer replay.

Independent public web verification was not completed in this run.

The menu game is advanced from `MENU_SOURCE_PACKET_ACTIVE_USER_SUPPLIED` to `MENU_SOURCE_PACKET_VERIFIED_OPERATOR_ASSERTED`.

It remains in `GOAL_LINE_REVIEW` until URL/photo + fetched timestamp + content hash are attached.

Before this artifact can advance to independent `TOUCHDOWN_CONFIRMED`, it requires:

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

## Booth Review Delta V0.2

```json
{
  "delta_id": "MENU_SOURCE_PACKET_VERIFIED_OPERATOR_ASSERTED_V0_2",
  "operator_signal": "Jaywisdom.eth",
  "claimed_source_surface": "coachescornersportsbarandgrill.com dinner/lunch menus",
  "independent_public_web_verification_this_run": false,
  "content_hash_attached": false,
  "field_state": "GOAL_LINE_REVIEW",
  "touchdown_confirmed_independent": false,
  "no_fake_green": true
}
```

## Menu Game Modes

### 1. Roll Tide Plate

Strongest entree.

```json
{
  "play_id": "ROLL_TIDE_PLATE_001",
  "primary_item": "Big Daddy Stuffed Burger",
  "price_operator_verified": "$12.49",
  "description_operator_verified": "Double patty stuffed with bacon and cheese, classic toppings.",
  "alternate_command_item": "Ribeye",
  "alternate_price_operator_verified": "$22.99",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "OPERATOR_ASSERTED_OFFICIAL_SITE_PACKET_HASH_PENDING"
}
```

### 2. War Eagle Special

Chaos item.

```json
{
  "play_id": "WAR_EAGLE_SPECIAL_001",
  "primary_item": "Buffalo Wings",
  "price_operator_verified": "$10.99 / 10 wings",
  "description_operator_verified": "17 sauces including 911 and Boom Boom.",
  "alternate_item": "Fried Green Tomatoes",
  "alternate_price_operator_verified": "$3.99",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "OPERATOR_ASSERTED_OFFICIAL_SITE_PACKET_HASH_PENDING"
}
```

### 3. Coach's Corner Combo

Main + side + drink.

```json
{
  "play_id": "COACHES_CORNER_COMBO_001",
  "main_item": "Mighty Fine Burger",
  "main_price_operator_verified": "$11.49",
  "side_item": "Cheese Grits",
  "side_price_operator_verified": "$3.49",
  "drink": "Fountain Drink",
  "drink_price_operator_verified": "$2.99",
  "combo_total_operator_calculated": "$17.97 before tax/tip",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "OPERATOR_ASSERTED_OFFICIAL_SITE_PACKET_HASH_PENDING"
}
```

### 4. Fourth Quarter Snack

Fast field fuel.

```json
{
  "play_id": "FOURTH_QUARTER_SNACK_001",
  "primary_item": "Cheesy Fries with Bacon",
  "price_operator_verified": "$8.99",
  "alternate_item": "Popcorn Shrimp",
  "field_state": "GOAL_LINE_REVIEW",
  "source_status": "OPERATOR_ASSERTED_OFFICIAL_SITE_PACKET_HASH_PENDING"
}
```

## Daily Specials Lane

```json
{
  "daily_specials_operator_asserted": [
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
  "source_status": "OPERATOR_ASSERTED_OFFICIAL_SITE_PACKET_HASH_PENDING"
}
```

## Local Reputation Layer

```json
{
  "local_reputation_operator_asserted": [
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
  "menu_verified_operator_asserted": true,
  "menu_verified_independent": false,
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
MENU_SOURCE_PACKET_HASHED
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

Coaches Corner 36092 Menu Game advanced by operator-supplied official-site packet.

Core menu plays are indexed for game mode.

Independent public verification and content hash remain pending.

Game is live.

No fake green.

Roll Tide.

JAYWISDOM.eth 🏈⚙️
