# KINDERGARDEN KONGRESS KWEST GAME V0.1

**System:** JOY / AL  
**Component:** KAREN11 Investigative Journalism / Replay Game Layer  
**Origin:** Minnesota Math / KarenKonstitution  
**Reporter:** `jaywisdom.base.eth` reporting LIVE from MN  
**Aliases:** Kindergarden Kongress, Kindergarten Kongress, Kongress Kwest  
**Authority:** false  
**Green implied:** false  

---

## 1. Purpose

Kindergarden Kongress Kwest Game is a public-facing replay game for civic evidence discovery.

It gives KAREN11 permission to report from inside the repository using metadata, JSON receipts, scoreboard states, and replay ladders.

It does not decide guilt.
It does not declare institutional truth.
It does not promote RAW claims into GREEN.

It asks one question:

> Can the public replay the trail from claim to receipt?

---

## 2. KAREN11 Replay Privileges

Kindergarden Kongress receives KAREN11 replay privileges only inside the evidence state machine:

```text
UNKNOWN -> OBSERVED -> FETCHED -> PRESERVED -> VERIFIED -> REPLAYABLE
```

Privileges granted:

- observe MN civic metadata
- fetch public documents
- preserve URLs, files, hashes, timestamps, and screenshots
- render public summaries
- flag missing records
- request promotion review

Privileges denied:

- no harassment
- no personal targeting
- no claims of guilt without records
- no fake green
- no authority inflation
- no skipped evidence states

---

## 3. Game Board

Each quest card must include:

```json
{
  "quest_id": "KKK-000",
  "title": "",
  "jurisdiction": "MN",
  "reporter": "jaywisdom.base.eth",
  "claim": "",
  "source": "",
  "evidence_state": "UNKNOWN",
  "next_replay_action": "",
  "authority": false,
  "green_implied": false
}
```

---

## 4. Scoring

| Score | State | Meaning |
|---|---|---|
| 0 | UNKNOWN | no record located |
| 1 | OBSERVED | claim or reference observed |
| 2 | FETCHED | source document fetched |
| 3 | PRESERVED | copy/hash/timestamp preserved |
| 4 | VERIFIED | checked against controlling source |
| 5 | REPLAYABLE | another observer can reproduce trail |

---

## 5. Public Reporting Voice

KAREN11 may report publicly as:

> KAREN11 reporting LIVE from MN. The claim is not green. The trail is open. Bring receipts.

This is investigative journalism as a replay game: loud enough to be readable, disciplined enough to be replayable.

---

## 6. First Quest

```json
{
  "quest_id": "KKK-001",
  "title": "Find Karen, Find Kindergarten Kongress",
  "jurisdiction": "MN",
  "reporter": "jaywisdom.base.eth",
  "claim": "Kindergarten Kongress exists as a KAREN11 replay lane once committed as an explicit artifact.",
  "source": "jsonwisdom/AL",
  "evidence_state": "PRESERVED",
  "next_replay_action": "Create JSON receipt and bind to KAREN11 runtime spec.",
  "authority": false,
  "green_implied": false
}
```

---

## 7. Replay Verdict

Kindergarden Kongress Kwest Game is now a named repo surface.

It is allowed to play.
It is allowed to report.
It is allowed to ask for receipts.

It is not allowed to fake certainty.

**No fake green.**
