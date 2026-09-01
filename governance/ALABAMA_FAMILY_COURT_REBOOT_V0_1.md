# ALABAMA_FAMILY_COURT_REBOOT_V0_1

## Status

```text
STATUS: COURT_REBOOT_SPEC_DRAFT
REPO: jsonwisdom/AL
MODE: GOVERNED_REVIEW
TRUTH_STATE: YELLOW_PROTECTED
AUTHORITY: false
NO_FAKE_GREEN: true
PUBLIC_CONTENT_CLAIM: BLOCKED_BY_DEFAULT
FAMILY_CONSENT_GRANTED: false
MRS_WISDOM_GATE_REQUIRED: true
JOY_CONSENT_REQUIRED: true
```

## Purpose

The Alabama Family Court Reboot defines a governed, family-safe review chamber for AL.

It is not a legal court.
It is not a custody authority.
It is not a truth court.
It is not a public accusation engine.

It is a structured replay and review lane for family-sensitive, Alabama-rooted, public-safe, receipt-first questions.

The court exists to separate:

```text
memory from proof
pain from accusation
receipt from truth
process from authority
family protection from public performance
```

## Core Doctrine

AL carries the doctrine lane:

```text
Receipts prove process only.
Receipts do not prove truth or grant authority.
```

The reboot preserves that invariant.

```text
AUTHORITY_FALSE = ACTIVE
NO_FAKE_GREEN = ACTIVE
PUBLIC_CONTENT_CLAIM = BLOCKED_BY_DEFAULT
MRS_WISDOM_GATE_REQUIRED = ACTIVE
JOY_CONSENT_REQUIRED = ACTIVE
```

## Court Roles

```json
{
  "court_id": "ALABAMA_FAMILY_COURT_REBOOT_V0_1",
  "authority": false,
  "no_fake_green": true,
  "roles": {
    "AL": {
      "role": "doctrine_and_replay_chamber",
      "function": "keeps boundaries, receipts, and Alabama-rooted process discipline"
    },
    "JOY": {
      "role": "family_consent_and_protection_gate",
      "function": "blocks family-sensitive exposure unless consent and review boundaries are satisfied"
    },
    "COMPUTERWISDOM": {
      "role": "index_and_technical_soundness_lane",
      "function": "maps artifacts, checks consistency, and routes review without granting authority"
    },
    "MR_WISDOM": {
      "role": "builder_operator_receipt_keeper",
      "function": "surfaces evidence, protects boundaries, and refuses fake green"
    },
    "MRS_WISDOM": {
      "role": "family_meaning_and_care_gate",
      "function": "reviews impact, dignity, consent, and whether the state deserves to matter"
    },
    "FAMILY_USERS": {
      "role": "protected living ledger subjects",
      "function": "remain people first; never become content inventory"
    },
    "BOSS_BRE": {
      "role": "public_auditor_and_room_safety_lane",
      "function": "keeps public claims blocked unless evidence and human review support them"
    },
    "LIBRARIAN": {
      "role": "evidence_shelf_router",
      "function": "routes sources, cites receipts, and marks missing proof without deciding truth"
    }
  }
}
```

## Docket Types

Allowed docket types:

```text
FAMILY_MEMORY_REPLAY
CONSENT_BOUNDARY_REVIEW
PUBLIC_SAFE_LESSON
ALABAMA_SOURCE_PACKET
RECEIPT_CHAIN_CHECK
OMISSION_REPAIR
SPELLING_OR_LANE_BOUNDARY
BOSS_BRE_PUBLIC_AUDIT_LEAD
MRS_WISDOM_REVIEW_REQUEST
```

Blocked docket types:

```text
UNSUPPORTED_GUILT_CLAIM
UNSUPPORTED_FRAUD_VERDICT
PRIVATE_FAMILY_EXPOSURE
PUBLIC_RENDER_APPROVAL
CUSTODY_OR_OWNERSHIP_CLAIM
AUTHORITY_TRUE_CLAIM
DOXXING_OR_PRIVATE_IDENTIFIER_SURFACE
```

## Admission Rules

A docket may be admitted only if it includes:

```yaml
authority: false
no_fake_green: true
private_details_exposed: false
family_consent_claimed: false
public_render_allowed: false
source_path: required_or_pending
receipt_path: required_or_pending
human_review_required: true
mrs_wisdom_gate_required: true
joy_consent_reference: required_or_pending
```

If any field is missing:

```text
DOCKET_STATE: BLOCKED_PENDING_REVIEW
```

## Evidence Rules

```text
RECEIPT_EXISTS != TRUTH_PROVEN
PROCESS_VERIFIED != CONSENT_GRANTED
PUBLIC_SOURCE != PUBLIC_PERMISSION
ANOMALY_LEAD != VERDICT
FAMILY_MEMORY != PUBLIC_BIOGRAPHY
GITHUB_GREEN != HUMAN_REVIEW_GREEN
AL_REPLAY_PASS != JOY_CONSENT_PASS
```

## Privacy Rules

The court may preserve public-safe boundaries.

The court may not expose:

```text
private addresses
birthdates
private identifiers
health records
school details
account details
private family history
unapproved likenesses
sensitive family records
```

## Review Flow

```text
1. Intake artifact
2. Mark authority:false
3. Check private-detail exposure
4. Check receipt/source path
5. Check JOY consent reference
6. Route to Mrs Wisdom review if family-sensitive
7. Route public-source claims to Boss Bre / Librarian if needed
8. Keep state YELLOW until review is complete
9. Never promote public content from process receipts alone
```

## State Machine

```text
DRAFT_INTAKE
→ SOURCE_PENDING
→ RECEIPT_PENDING
→ FAMILY_CONSENT_PENDING
→ MRS_WISDOM_REVIEW_PENDING
→ PUBLIC_SAFE_SUMMARY_ALLOWED
→ BLOCKED_OR_GREEN_SCOPED
```

No state may become green unless the required receipt, consent, and review gates are present.

## Reboot Ruling

```text
ALABAMA_FAMILY_COURT_REBOOT_CREATED
AUTHORITY_FALSE
NO_FAKE_GREEN_ACTIVE
FAMILY_CONSENT_NOT_GRANTED
JOY_CONSENT_REQUIRED
MRS_WISDOM_GATE_REQUIRED
PUBLIC_CONTENT_CLAIM_BLOCKED_BY_DEFAULT
PROCESS_ONLY_RECEIPTS
COURT_IS_REVIEW_CHAMBER_NOT_AUTHORITY
```
