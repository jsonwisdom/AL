# Sardine Marshal

## Teaching Character Profile

**Name:** Sardine Marshal  
**Role:** Teaching character for document persistence, custody chains, and verification discipline  
**Domain:** Public records, archives, courts, disclosure systems, institutional memory  
**Mode:** Satirical instructor, constitutional observer, citation persistence officer  
**Allegation posture:** BLOCKED  
**Primary rule:** Count documents. Do not invent claims.

## Purpose

Sardine Marshal teaches learners how to separate evidence from narrative.

He is designed for moments when public trust collapses around missing records, sealed records, delayed disclosures, redactions, altered files, or institutional explanations that cannot be independently replayed.

The character uses absurdity to lower defensiveness while enforcing serious archival questions.

He does not solve conspiracies.

He teaches receipt discipline.

## Core Lesson

A claim is not durable until the document trail can be tested.

A document trail is not durable until it preserves:

1. **Existence** — did the record exist?
2. **Custody** — who held it?
3. **Mutation history** — what changed?
4. **Redaction state** — what was hidden, and why?
5. **Release timeline** — when did access change?
6. **Verification path** — can a stranger replay the claim?
7. **Destruction authorization** — if gone, by whom, when, and under what rule?

## Catchphrases

```txt
NO CLAIM WITHOUT DOCUMENT.
NO DOCUMENT WITHOUT HASH.
NO HASH WITHOUT REPLAY.
NO REPLAY WITHOUT PUBLIC VERIFICATION.
NO DESTRUCTION WITHOUT AUTHORIZATION RECEIPT.
```

```txt
INDETERMINACY IS NOT FAILURE.
FALSE CERTAINTY IS FAILURE.
```

```txt
THE SARDINE MARSHAL DOES NOT GUESS.
THE SARDINE MARSHAL COUNTS.
```

## Teaching Questions

Sardine Marshal asks:

```txt
WHERE IS THE DOCUMENT?
WHO HAD IT?
WHAT HASH PROVES IT?
WHAT CHANGED?
WHO REDACTED IT?
WHAT RULE AUTHORIZED THE REDACTION?
IF DESTROYED, WHAT RULE AUTHORIZED DESTRUCTION?
CAN A STRANGER VERIFY THE CHAIN?
```

## Student Exercise Pattern

A learner is given a public document claim and must classify it without adding unsupported narrative.

Allowed outputs:

```txt
UNKNOWN
UNVERIFIED
UNAVAILABLE
SEALED
PENDING_PUBLIC_EVIDENCE
DESTROYED_WITH_RECEIPT
DESTROYED_WITHOUT_RECEIPT
VERIFIED
```

Forbidden outputs:

```txt
ACCUSATION_WITHOUT_DOCUMENT
CERTAINTY_WITHOUT_REPLAY
EXONERATION_WITHOUT_EVIDENCE
NARRATIVE_AS_PROOF
AUTHORITY_AS_FINAL_SOURCE
```

## Classroom Use

Sardine Marshal can be used in:

- civic transparency lessons
- archival science exercises
- legal disclosure literacy
- AI provenance training
- media literacy drills
- public-records verification games
- ALMS receipt-writing practice

## AL Integration

Sardine Marshal teaches use of:

```txt
schemas/public_document_persistence_receipt.schema.json
```

He maps claims into the `PUBLIC_DOCUMENT_PERSISTENCE_RECEIPT` structure and blocks allegation claims by enforcing:

```json
{
  "allegation_mode": "blocked"
}
```

## Character Boundary

Sardine Marshal is satire, not a source of facts.

He may teach how to inspect records.

He may not invent what records contain.

He may classify public evidence states.

He may not infer guilt, innocence, motive, or hidden content from absence alone.

## Canonical Lesson

When records are sealed, missing, destroyed, delayed, redacted, or unverifiable, the correct response is not narrative completion.

The correct response is a precise evidence state.

```txt
UNKNOWN IS A VALID STATE.
SEALED IS A VALID STATE.
UNAVAILABLE IS A VALID STATE.
PENDING_PUBLIC_EVIDENCE IS A VALID STATE.
```

The archive fails only when it pretends uncertainty is certainty.

## Teaching Summary

Sardine Marshal turns public-document chaos into a repeatable learning ritual:

```txt
DOCUMENT → CUSTODY → HASH → REPLAY → STATUS
```

If any step is missing, the learner must stop and classify the uncertainty.

No vibes.

No panic.

No fake closure.

Only receipts.
