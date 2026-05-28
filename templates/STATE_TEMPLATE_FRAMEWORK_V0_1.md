# State Template Framework v0.1

Builder: Jason Wisdom / jaywisdom.eth / jaywisdom.base.eth  
Repo: jsonwisdom/AL  
Purpose: Copy the Jay's AL runtime pattern across all 50 states as learning contexts  
Authority: false

## Root Rule

A state template does not control a state.

It creates a repeatable learning context for checking public information, protecting privacy, creating receipts, running replay, and teaching lawful next moves.

```json
{
  "state_template": true,
  "controls_people": false,
  "controls_government": false,
  "legal_authority_claimed": false,
  "government_authority_claimed": false,
  "authority": false
}
```

## Design Pattern

Each state gets the same runtime spine:

```txt
State Name
  -> Public Learning Map
  -> Family / School / County Routes
  -> Citizen Letter Audit
  -> Retail / Coupon Learning
  -> Media Signal Receipts
  -> Governance Process Receipts
  -> Store Missions
  -> Computer Wisdom Verifier Bridge
```

## State Runtime Object

```json
{
  "state_runtime": {
    "state_name": "{{STATE_NAME}}",
    "state_code": "{{STATE_CODE}}",
    "origin_context": "{{STATE_NAME}} learning context",
    "public_learning_only": true,
    "authority": false,
    "core_loop": [
      "observe",
      "classify",
      "source",
      "redact_private_data",
      "hash",
      "verify",
      "receipt",
      "replay_if_disputed",
      "teach",
      "repeat"
    ]
  }
}
```

## Required State Files

Each copied state should have:

```txt
states/{{STATE_CODE}}/
  README.md
  RUNTIMES.md
  FAMILY_SCHOOLS.md
  COUNTY_SCRAM.md
  CITIZEN_LETTER_AUDIT.md
  RETAIL_COUPON_RUNTIME.md
  MEDIA_FLYWHEEL.md
  GOVERNANCE_FLYWHEEL.md
  STORE_MISSIONS.md
  RECEIPTS_SCHEMA.md
  SAFETY_BOUNDARIES.md
```

## README Template

```md
# {{STATE_NAME}} Looking Glass

Status: State learning context  
Authority: false  
Government authority claimed: false  
Legal advice: false

{{STATE_NAME}} Looking Glass turns public confusion into checkable learning:

documents in, receipts out, patterns visible, fixes lawful.

## Core Line

Reality is not what is loud. Reality is what can be checked.

## What This Offers

- family learning routes
- school routes
- county SCRAM projects
- citizen letter review
- retail coupon receipts
- media signal receipts
- governance process learning
- Computer Wisdom verification bridge

## What This Is Not

- not a government office
- not legal advice
- not election machinery
- not official audit authority
- not media impersonation
- not control over people

## Runtime

Expand. Loop. Membrane. Return. Repeat.
```

## State Switch

Each state has an internal learning switch:

```json
{
  "OFF": "UNVERIFIED_OR_UNCHECKED",
  "ON": "CHECKABLE_WITH_PUBLIC_RECEIPTS",
  "FORBIDDEN": "CONTROL_PEOPLE_OR_GOVERNMENT"
}
```

## 50-State Copy Rule

Copy the pattern, not the authority.

```txt
Alabama is the origin map.
Every other state is a learning map.
No state gets control logic.
Every state gets receipt logic.
```

## Core Runtimes Per State

```json
{
  "required_runtimes": [
    "youth_runtime",
    "family_runtime",
    "school_runtime",
    "county_runtime",
    "retail_runtime",
    "letter_audit_runtime",
    "media_runtime",
    "governance_runtime",
    "store_runtime",
    "agent_runtime",
    "compute_wisdom_runtime"
  ]
}
```

## Safety Boundaries

```json
{
  "boundaries": [
    "no_legal_advice_claims",
    "no_government_authority_claims",
    "no_election_machinery",
    "no_private_child_data_collection",
    "no_harassment_or_targeting",
    "no_unverified_accusation_promotion",
    "no_media_impersonation",
    "no_store_purchase_without_user_control",
    "no_payment_claim_without_payment_proof",
    "no_replay_with_live_api_calls"
  ]
}
```

## Store Layer

Each state can support sellable bounded missions:

```json
{
  "state_store_missions": [
    "citizen_letter_review",
    "school_route_pack",
    "coupon_terms_checker",
    "receipt_api",
    "replay_lab",
    "mcp_agent_mission_pack",
    "public_document_timeline_review"
  ]
}
```

## 50-State Expansion Sequence

```txt
1. Freeze Alabama as origin template.
2. Create /states directory.
3. Generate one folder per state.
4. Keep every state authority:false.
5. Add shared schemas.
6. Add state-specific public sources later.
7. Add receipts only when evidence exists.
8. Publish state pages as learning maps.
9. Route MCP agents through mission gates.
10. Return every mission with a receipt.
```

## Final Line

```txt
The 50-state framework does not copy power. It copies the receipt runtime.
```

By Jason Wisdom  
jaywisdom.eth  
jaywisdom.base.eth