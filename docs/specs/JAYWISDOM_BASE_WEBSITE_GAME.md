# jaywisdom.base Website Game

Status: DRAFT_CANON
Operator: Jay Wisdom
Primary identity: jaywisdom.base
Anchor identity: jaywisdom.eth
System: ALMS 5.0 / Wisdom Family Gaming / Meme Court / Zora

## Core thesis

The jaywisdom.base website is the public home board for Jay Wisdom artifacts.

Building, updating, and maintaining the site becomes a game:

```text
Page -> Artifact -> Receipt -> Review -> Publish -> Anchor -> Maintenance XP
```

The website is not only a portfolio. It is a playable verification surface.

---

## Identity rule

```json
{
  "public_home": "jaywisdom.base",
  "research_anchor": "jaywisdom.eth",
  "operator": "Jay Wisdom",
  "principle": "public pages must point back to evidence"
}
```

---

## Game loop

```json
{
  "loop": [
    "create_page_mission",
    "write_or_update_content",
    "link_artifacts",
    "attach_receipts",
    "meme_court_review",
    "publish_site_update",
    "anchor_research_to_jaywisdom_eth",
    "maintenance_check"
  ]
}
```

---

## Website artifact classes

```json
{
  "classes": [
    "homepage",
    "research_page",
    "artifact_gallery",
    "meme_court_page",
    "zora_drop_page",
    "legacy_page",
    "state_alms_dashboard",
    "receipt_index",
    "public_prompt_page"
  ]
}
```

---

## Mission card schema

```json
{
  "mission_id": "JWBASE-0001",
  "title": "string",
  "page_path": "string",
  "artifact_links": [],
  "receipt_links": [],
  "anchor_identity": "jaywisdom.eth",
  "public_identity": "jaywisdom.base",
  "state": "DRAFT | REVIEW | READY_TO_PUBLISH | PUBLISHED | ANCHOR_REQUIRED | ANCHORED | MAINTENANCE_REQUIRED",
  "xp": 0,
  "badge": "UNSET",
  "next_action": "string"
}
```

---

## XP rules

```json
{
  "xp_rules": {
    "page_created": 25,
    "receipt_linked": 50,
    "meme_court_review_passed": 40,
    "zora_card_linked": 40,
    "research_anchor_added": 75,
    "broken_link_fixed": 25,
    "weekly_maintenance_passed": 100
  }
}
```

---

## Badges

```json
{
  "badges": {
    "Site_Builder": "created first jaywisdom.base page mission",
    "Receipt_Linker": "linked first ALMS receipt to public page",
    "Research_Anchor": "anchored research reference to jaywisdom.eth",
    "Meme_Court_Publisher": "published Meme Court artifact page",
    "Zora_Gallery_Curator": "linked Zora-ready artifact card",
    "Maintenance_Goblin_Slayer": "fixed drift, stale link, or missing receipt"
  }
}
```

---

## Maintenance rules

1. Public pages must not claim VERIFIED without ALMS PASS.
2. Every research claim should link to jaywisdom.eth or a repo receipt.
3. Every Zora artifact must use UNVERIFIED_IDENTIFIER until chain confirms contract.
4. Broken links create MAINTENANCE_REQUIRED state.
5. Weekly audit checks page links, receipt paths, and root references.
6. Website content may be fun, but public proof labels must stay exact.

---

## First mission

```json
{
  "mission_id": "JWBASE-0001",
  "title": "Publish Meme Court x Zora Learning Artifact Page",
  "page_path": "site/meme-court/wfg-0001.html",
  "artifact_links": [
    "alms/legacy/artifacts/WFG-0001.json",
    "alms/meme_court/cases/MC-0001.json",
    "alms/meme_court/zora/ZMC-0001.json"
  ],
  "anchor_identity": "jaywisdom.eth",
  "public_identity": "jaywisdom.base",
  "state": "DRAFT",
  "next_action": "create JWBASE-0001 mission card"
}
```

---

## Public slogan

```text
jaywisdom.base

Build the page.
Link the receipt.
Anchor the research.
Maintain the truth.
```
