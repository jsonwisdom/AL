# ALABAMA_EMS_ALMS_REPLAY_WETUMPKA_V0_1

## Status

```text
LOCAL_DRAFT
SOURCE_PACKET_PENDING
ALABAMA_EMS_REPLAY_LAYER
NO_FAKE_GREEN_ACTIVE
```

## Coach Wisdom Context

```text
Lunch surface: Coach's Corner / @coachescorner
Locality: Wetumpka, AL
Mode: Alabama citizen replay
```

This artifact uses the user-supplied Wetumpka / Coach's Corner context as a localization surface only.

It does not verify a venue, business status, public agency, emergency provider, address, hours, or service coverage.

## EMS Boundary

```text
ALABAMA_EMS_REPLAY != EMERGENCY_DISPATCH
ALABAMA_EMS_REPLAY != MEDICAL_ADVICE
ALABAMA_EMS_REPLAY != SERVICE_COVERAGE_CLAIM
ALABAMA_EMS_REPLAY = PUBLIC_SAFE_CIVIC_REPLAY_STRUCTURE
```

For any real emergency, use local emergency services / 911.

## Purpose

Replay Alabama EMS through ALMS as a public-safe civic verification lane.

The lane asks:

```text
What locality?
What jurisdiction?
What agency or service surface?
What public source proves it?
What citizen-facing information is verified?
What remains unknown?
```

## Localization Seed

```json
{
  "localization_id": "AL_LOCALIZATION_WETUMPKA_COACHESCORNER_V0_1",
  "state": "Alabama",
  "locality": {
    "city": "Wetumpka",
    "county": "SOURCE_PACKET_PENDING",
    "source_status": "USER_SUPPLIED"
  },
  "venue_or_surface": {
    "name": "Coach's Corner",
    "handle_or_alias": "@coachescorner",
    "surface_type": "restaurant",
    "source_status": "USER_SUPPLIED"
  },
  "verification": {
    "field_state": "GOAL_LINE_REVIEW",
    "verified_status": "SOURCE_PACKET_PENDING",
    "no_fake_green": true
  },
  "authority": false
}
```

## EMS Replay Input Contract

```json
{
  "year": "optional",
  "state": "Alabama",
  "city": "required",
  "county": "required_before_promotion",
  "agency_or_surface": "required_before_promotion",
  "situation": "required",
  "citizen_question": "required",
  "source_packet": "required_before_promotion"
}
```

## EMS Replay Output Contract

```json
{
  "replay_id": "AL_EMS_REPLAY_[CITY]_[SITUATION_HASH]",
  "field_state": "PUNTED | GOAL_LINE_REVIEW | TOUCHDOWN_CONFIRMED | FLAG_ON_THE_PLAY | NO_FAKE_GREEN",
  "public_safe_summary": "string",
  "verified_facts": [],
  "unknowns": [],
  "source_packets": [],
  "authority": false
}
```

## Field Logic

```text
PUNTED = missing locality or source packet
GOAL_LINE_REVIEW = locality/situation present, source packet pending
TOUCHDOWN_CONFIRMED = public source packet verified
FLAG_ON_THE_PLAY = conflicting agency, jurisdiction, or service information
NO_FAKE_GREEN = cannot promote
```

## Source Packet Requirements

```text
official city/county/state source if available
agency or department public page if applicable
fetched_at_utc
content_hash
extractor_version
replay_notes
```

## Guardrails

1. Do not provide emergency instructions beyond directing real emergencies to 911/local emergency services.
2. Do not claim service coverage without official source packet.
3. Do not claim agency status without official source packet.
4. Do not claim venue status, hours, address, or affiliation without source packet.
5. Do not confuse restaurant localization with EMS authority.
6. Family Layer 0 still outranks the game.
7. No fake green.

## Closing Receipt

Alabama EMS ALMS replay lane opened for Wetumpka localization.

Coach Wisdom lunch surface indexed as user-supplied localization only.

EMS claims remain SOURCE_PACKET_PENDING.

No fake green.

JAYWISDOM.eth 🏈⚙️
