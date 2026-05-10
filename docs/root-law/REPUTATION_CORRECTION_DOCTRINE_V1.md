# Reputation Correction Doctrine v1

Status: DRAFT_ROOT_LAW_EXTENSION
Root identity: jaywisdom.base
Applies to: learning lab, review flows, correction logs, badge logic, challenge windows, and reputation-bound roles.

## Verdict

A correction is not a penalty.
A correction is a neutral state of becoming until replay proves the repair.

Once the correction is timely, transparent, sourced, and replayable, the repair may count as positive reputation for transparency.

## Core Rule

```text
Correction begins neutral.
Verified repair becomes positive.
Concealment becomes negative.
```

## Why

The system must not punish authentic growth. A living document changes because the individual is still thinking, learning, and accepting responsibility. But the system also must not reward careless error by default.

Therefore, correction is interpreted in phases.

## Correction States

```text
CORRECTION_DECLARED
- neutral
- author or reviewer admits a change is needed
- no reputation gain or loss

CORRECTION_SOURCED
- neutral-positive pending review
- source trail, old claim, new claim, and reason are visible

CORRECTION_REPLAYED
- positive transparency credit
- independent verifier can reproduce the correction path

CORRECTION_CHALLENGED
- unresolved
- no reputation mutation until settled

CORRECTION_SETTLED
- role-relevant reputation may update
- update is receipt-bound, not identity-global

CORRECTION_CONCEALED
- negative trust event
- applies only to the specific role/context/receipt chain
```

## Reputation Interpretation

| Correction Behavior | Reputation Effect | Reason |
| --- | --- | --- |
| Honest correction declared | Neutral | Becoming is not failure. |
| Correction with sources and visible diff | Pending positive | Transparency is present but not yet replayed. |
| Correction independently replayed | Positive for transparency role | Repair is proven. |
| Correction under active challenge | Frozen | Settlement must happen first. |
| Silent edit that hides material change | Negative receipt-bound event | Concealment breaks living document law. |
| Repeated careless errors without review | Role cooldown possible | The issue is process reliability, not identity worth. |

## No Social Score Rule

Reputation must not become a totalizing score for the person.

Allowed:

- role-specific trust state
- receipt-specific transparency credit
- time-bound role cooldowns
- challengeable review outcomes
- exportable correction history

Forbidden:

- permanent identity score
- hidden behavioral scoring
- demographic risk scoring
- donor-controlled reputation
- machine-final moral judgment

## Learning Lab Rule

In the learning environment, a learner who corrects their own claim should not be punished. The correction becomes a teaching artifact.

The correct UI label is:

```text
Correction logged: becoming visible.
```

After replay:

```text
Correction verified: transparency receipt earned.
```

## Worker Bee Boundary

AI employees may:

- detect possible contradictions
- suggest correction drafts
- compare old and new claims
- prepare diffs
- request sources
- route correction for review

AI employees may not:

- silently rewrite the record
- assign moral blame
- convert correction into global score
- settle disputed corrections without human or constitutional review

## Receipt Fields

A CorrectionReceipt should include:

```json
{
  "type": "CorrectionReceipt",
  "root_identity": "jaywisdom.base",
  "previous_claim_hash": "bytes32",
  "corrected_claim_hash": "bytes32",
  "reason_hash": "bytes32",
  "source_trail_hash": "bytes32",
  "diff_hash": "bytes32",
  "declared_by": "address_or_role",
  "review_state": "CORRECTION_DECLARED",
  "challenge_window_ends_at": "timestamp",
  "reputation_effect": "NEUTRAL_UNTIL_REPLAYED"
}
```

## Constitutional Line

```text
The system should reward responsibility, not perfection.
```

## Audit Verdict

REPUTATION_CORRECTION_DOCTRINE_V1_APPLIED

Correction is neutral becoming.
Verified repair is positive transparency.
Concealment is the actual violation.
