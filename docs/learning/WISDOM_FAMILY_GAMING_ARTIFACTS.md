# Wisdom Family Gaming — Learning Mode ON

Status: ACTIVE_LEARNING_GUIDE
Operator: Jay Wisdom
Identity: jaywisdom.base / jaywisdom.eth

## Goal

Teach the Wisdom Family system how to create artifacts safely, clearly, and repeatably.

An artifact is not just content. An artifact is a packaged object with:

- purpose
- creator
- source
- version
- receipt status
- optional hash
- public caption
- next action

---

## Artifact creation loop

```text
Idea -> Draft -> Structure -> Receipt -> Version -> Publish -> Replay
```

Machine form:

```json
{
  "loop": [
    "idea",
    "draft",
    "structure",
    "receipt",
    "version",
    "publish",
    "replay"
  ]
}
```

---

## Artifact classes

```json
{
  "artifact_classes": [
    "spec",
    "prompt",
    "receipt",
    "image_prompt",
    "zora_drop",
    "social_post",
    "audit_card",
    "learning_card",
    "game_card",
    "legacy_record"
  ]
}
```

---

## Basic artifact schema

```json
{
  "artifact_id": "WFG-0001",
  "title": "string",
  "class": "spec | prompt | receipt | image_prompt | zora_drop | social_post | audit_card | learning_card | game_card | legacy_record",
  "creator": "Jay Wisdom / Wisdom Family",
  "identity": "jaywisdom.base",
  "purpose": "string",
  "source_paths": [],
  "hash": "sha256:<64-hex> | UNSET",
  "state": "DRAFT | LOCKED | REPLAY_REQUIRED | REPLAY_PASSED | PUBLISHED | BLOCKED",
  "caption": "string",
  "next_action": "string"
}
```

---

## Learning mode rules

1. Start small.
2. Name the artifact before expanding it.
3. Do not claim verified unless there is a receipt.
4. Use `UNSET` when the hash is not computed yet.
5. Humor is allowed; fake verification is not.
6. Family authorship must remain visible.
7. Every public artifact should have a next action.

---

## Game mechanic

Each artifact becomes a card.

```json
{
  "card_type": "artifact_card",
  "levels": {
    "level_1": "idea named",
    "level_2": "draft written",
    "level_3": "structured JSON added",
    "level_4": "receipt/hash added",
    "level_5": "published or replayed"
  }
}
```

---

## Example: learning card

```json
{
  "artifact_id": "WFG-0001",
  "title": "How to Create Artifacts",
  "class": "learning_card",
  "creator": "Jay Wisdom / Wisdom Family",
  "identity": "jaywisdom.base",
  "purpose": "teach artifact creation through Wisdom Family Gaming",
  "source_paths": ["docs/learning/WISDOM_FAMILY_GAMING_ARTIFACTS.md"],
  "hash": "UNSET",
  "state": "DRAFT",
  "caption": "Create the object. Name the proof. Level up the receipt.",
  "next_action": "create first artifact card JSON"
}
```

---

## Public caption

```text
Wisdom Family Gaming
Learning Mode = ON

Create the object.
Name the proof.
Level up the receipt.

jaywisdom.base
```

---

## Next build step

```json
{
  "next": "create alms/legacy/artifacts/WFG-0001.json",
  "then": "fold artifact cards into Wisdom Family Legacy registry",
  "then_after": "publish first learning-mode Zora/social card"
}
```
