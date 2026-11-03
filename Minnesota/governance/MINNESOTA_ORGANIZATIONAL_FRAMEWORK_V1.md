# Minnesota Organizational Framework v1

## Status

`DRAFT_FOR_HUMAN_REVIEW`

This framework governs how Minnesota organizational decisions, reviews, and public-evidence work preserve participation.

## Core principle

A person is not represented merely because a vote was counted or because silence was recorded.

For women participating in Minnesota work, the record must be capable of preserving:

- authored opinions;
- factual concerns;
- objections and dissent;
- proposed alternatives;
- conditions for support;
- questions left unanswered;
- evidence references;
- requested remedies or changes;
- whether the final decision actually responded to the contribution.

A vote is one event. An opinion is evidence with content, authorship, context, and consequence.

## Required separation

The system MUST keep these as separate fields and events:

```text
PARTICIPATION
OPINION
EVIDENCE
VOTE
DECISION
RESPONSE
IMPLEMENTATION EFFECT
```

It MUST NOT translate any of the following into agreement:

```text
SILENCE
ABSENCE
NONRESPONSE
ABSTENTION
LACK OF ACCESS
UNRECORDED COMMENT
WITHHELD CONSENT
```

## Opinion states

An opinion record may express one or more of these positions without being reduced to a binary vote:

```text
SUPPORTS
OPPOSES
CONDITIONAL_SUPPORT
PROPOSES_ALTERNATIVE
REQUESTS_MORE_EVIDENCE
RAISES_RISK
DISSENTS
ABSTAINS_WITH_REASON
WITHHOLDS_POSITION
UNRESOLVED
```

These states describe the contribution. They do not create execution authority.

## Required decision trace

Every material opinion included in a decision process SHOULD receive a disposition:

```text
ADOPTED
PARTIALLY_ADOPTED
NOT_ADOPTED_WITH_REASON
DEFERRED_WITH_TRIGGER
REQUIRES_MORE_EVIDENCE
OUT_OF_SCOPE_WITH_REASON
UNANSWERED
```

The decision record must identify what changed, what did not change, and why. A generic statement such as “feedback was considered” is insufficient.

## Women’s opinion safeguard

When a process specifically seeks or relies on women’s participation, the record MUST preserve women’s contributions as first-class opinion records rather than only reporting turnout, vote totals, attendance, or silence.

The system SHOULD report:

- number of authored opinion records;
- number receiving a substantive response;
- number adopted or partially adopted;
- number left unanswered;
- recurring concerns across independently authored opinions;
- barriers that prevented participation or publication;
- any difference between the recorded vote and the underlying written opinion.

Self-identification is voluntary. No participant is required to disclose sensitive identity information publicly. Public release requires an explicit publication choice or a documented lawful basis.

## Minority and dissent preservation

Minority reports and dissenting opinions must remain attached to the same decision graph as the prevailing decision. They must not be deleted, summarized beyond recognition, or treated as procedural noise.

```text
MAJORITY DECISION != COMPLETE RECORD
```

## Authority boundary

Opinions inform, challenge, and improve decisions. They do not independently create execution authority.

```text
OPINION_RECEIVED      = EVIDENCE
OPINION_RESPONDED_TO  = ACCOUNTABILITY
VOTE_RECORDED         = PROCEDURAL_EVENT
DECISION_AUTHORIZED   = SEPARATE_AUTHORITY_ACT
```

## Replay requirement

A replayable organizational decision should answer:

1. Who was invited or able to participate?
2. What did each person actually say?
3. What evidence did they rely on?
4. What alternatives did they propose?
5. What response did the organization provide?
6. What changed because of the opinion?
7. What remained unresolved?
8. Who authorized the final action?

## Governance invariants

```text
NO_FAKE_GREEN                    = TRUE
SILENCE_IS_NOT_CONSENT           = TRUE
VOTE_IS_NOT_COMPLETE_OPINION     = TRUE
DISSENT_PRESERVED                = TRUE
HUMAN_REVIEW_REQUIRED            = TRUE
MODEL_AUTHORITY                  = FALSE
PUBLICATION_CONSENT_REQUIRED     = TRUE_UNLESS_LAWFULLY_OVERRIDDEN
```

## Companion schema

Machine-readable opinion records conform to:

`Minnesota/governance/WOMENS_OPINION_RECORD_SCHEMA_V1.json`
