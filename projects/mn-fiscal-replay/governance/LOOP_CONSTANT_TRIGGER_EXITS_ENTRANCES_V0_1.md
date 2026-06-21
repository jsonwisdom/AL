# Loop Constant — Trigger Exits and Entrances v0.1

**Artifact:** `LOOP_CONSTANT_TRIGGER_EXITS_ENTRANCES_V0_1`  
**Lane:** `MN_FISCAL_REPLAY`  
**Status:** `DOCTRINE_RECORDED`  
**NO_FAKE_GREEN:** `ACTIVE`  

---

## Core Rule

A loop is not a chat rhythm. A loop is a governed state machine.

```text
INTENT → ENTRY_TRIGGER → ACTION → CHECK → RECEIPT → EXIT_DECISION → NEXT_ENTRY
```

The loop remains constant. Only the state changes.

---

## Loop Constant

```text
LOOP_CONSTANT = TRUE
```

Meaning:

1. Every build pass must have an entry condition.
2. Every edit must have a check.
3. Every check must produce an observable result.
4. Every result must decide whether the system exits, retries, escalates, or blocks.
5. No green claim is valid without the exit condition being satisfied.

---

## Entry Triggers

An entrance is allowed only when one of these triggers fires:

| Trigger | Meaning | Allowed Action |
|---|---|---|
| `USER_INTENT_RECEIVED` | User states the desired end state. | Plan or patch. |
| `PUBLIC_PAGE_MISMATCH` | Live page differs from expected design/state. | Patch served route. |
| `LINK_BEHAVIOR_FAILURE` | Main user path ejects to wrong surface. | Convert to on-page summary or correct route. |
| `RAW_RECEIPT_AS_FRONT_DOOR` | Machine data is exposed as public homepage. | Build human-readable summary layer. |
| `CLAIM_RISK_DETECTED` | Wording implies unsupported allegation. | De-escalate language. |
| `ROUTE_404` | Public route fails. | Create or sync served path. |
| `CACHE_STALE` | Live page likely serving old content. | Use cache-busted verification URL. |
| `CI_OR_REPLAY_FAILURE` | A verifier reports failure. | Read failure, patch, rerun. |
| `HUMAN_REVIEW_DELTA` | External review identifies trust gap. | Convert review into concrete requirements. |

---

## Exit Conditions

A loop may exit only through one of these states:

| Exit | Meaning | Public Claim Allowed? |
|---|---|---|
| `PASS_GREEN` | All defined checks pass. | Yes, scoped to passed checks only. |
| `PASS_WITH_LIMITS` | Core checks pass, but known limitations remain. | Yes, with limitation disclosure. |
| `BLOCKED_PENDING_EVIDENCE` | Required evidence is missing. | No. |
| `BLOCKED_PENDING_REVIEW` | Human or CI review is not complete. | No. |
| `ROUTE_UNVERIFIED` | Public route cannot be verified. | No. |
| `SOURCE_MISSING` | Source file/manifest/receipt missing. | No. |
| `OPERATOR_ESCALATION_REQUIRED` | Tooling cannot safely complete the next step. | No. |

---

## Website Loop Gate

For `https://jsonwisdom.github.io/AL/mn-fiscal-replay/`, the loop is not green until these checks pass:

```text
PUBLIC_ROUTE_LOADS
SERVED_DOCS_ROUTE_UPDATED
ROOT_ROUTE_MATCHES_DOCS_ROUTE
PRIMARY_BUTTONS_STAY_ON_PAGE
RAW_GITHUB_LINKS_ARE_SECONDARY
OFFICIAL_SOURCE_PDF_VISIBLE
NO_UNSUPPORTED_FRAUD_OR_ALTERATION_CLAIM
PUBLIC_LANGUAGE_DE_ESCALATED
MOBILE_VIEWPORT_READABLE
NO_FAKE_GREEN_DISCLOSED_IN TECHNICAL_GLOSSARY_OR_POLICY_LAYER
```

---

## Trigger-to-Action Map

```text
IF 404:
  create_or_sync_served_route
  verify_with_cache_buster

IF old design appears:
  identify_served_path
  update_served_path
  verify content hash / visible marker

IF buttons eject to GitHub:
  convert primary buttons to on-page anchors
  keep raw receipts as secondary technical links

IF page reads as internal dashboard:
  replace internal names with public functional labels
  move internal doctrine to glossary

IF claim language sounds conspiratorial:
  de-escalate to neutral civic-audit wording
  preserve receipt-bound truth

IF user reports mismatch:
  treat report as a trigger, not complaint noise
  inspect served file before defending prior state
```

---

## Doctrine Lock

```text
PROMPT = INTENT
LOOP = GOVERNANCE
CHECKS = RECEIPTS
EXIT = CLAIM_BOUNDARY
GREEN = ONLY_AFTER_EXIT_CONDITION
```

---

## Current Application

For the MN Fiscal Replay public page, the active loop is:

```text
USER_INTENT_RECEIVED
→ PUBLIC_REGISTER_REDESIGN
→ SERVED_ROUTE_SYNC
→ ON_PAGE_EVIDENCE_LINKS
→ LIVE_PAGE_REVIEW
→ NEXT_TRIGGER_OR_EXIT
```

Current exit status remains:

```text
PASS_WITH_LIMITS
```

Known limitation:

```text
Technical receipt links still point to GitHub by design, but primary public evidence paths now remain on-page.
```
