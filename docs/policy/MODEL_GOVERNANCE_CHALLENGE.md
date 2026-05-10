# MODEL GOVERNANCE CHALLENGE

## Status

MODEL_GOVERNANCE_CHALLENGE_V1  
COMPANION_TO_ALMS_IMPLEMENTATION_MEMO  
JUSTICE_REVIEW_PATHWAY  
NOT_EXECUTION_FIDELITY_ONLY

## Purpose

This protocol defines how a person may challenge the design, policy logic, threshold, feature use, or public legitimacy of an automated system even when execution replay succeeds.

Replay proves execution.

It does not prove justice.

A perfectly replayable system may still be unlawful, arbitrary, discriminatory, incomprehensible, or unfit for public power.

## Core Firewall

```txt
REPLAY PROVES EXECUTION.
IT DOES NOT PROVE JUSTICE.
```

The MODEL_GOVERNANCE_CHALLENGE pathway prevents ALMS from becoming a perfect machine for replaying injustice at scale.

## Section 1. Scope

A MODEL_GOVERNANCE_CHALLENGE may be filed against any covered automated system that materially affects:

- benefits
- housing
- employment
- credit
- public eligibility
- legal recommendation
- safety-critical access
- education opportunity
- medical triage or access
- immigration or border processing
- public-sector prioritization or enforcement

A challenge may address system design even if the manifest, audit log, and replay surface are valid.

## Section 2. Zero-Barrier Challenge Initiation

A challenge must be openable by an affected person without technical knowledge.

The following statement is sufficient to initiate a valid challenge:

```txt
The computer said no and I think that is wrong.
```

The person does not need to know:

- what a model is
- what features were used
- what threshold was applied
- what policy hash means
- how replay works
- how to classify the error

The system bears the burden of translation.

Agencies and operators must convert plain-language grievances into the appropriate challenge track:

```txt
EXECUTION_FIDELITY_CHALLENGE
MODEL_GOVERNANCE_CHALLENGE
BOTH_TRACKS_REQUIRED
```

Failure to route the challenge correctly is itself a review defect.

## Section 3. Plain-Language Intake Requirements

The intake form must ask plain questions:

```txt
What happened?
What did the system decide?
Why do you think it was wrong?
What harm did it cause or threaten?
What outcome are you asking for?
Do you need urgent human review?
```

The intake form must not require the citizen to provide:

- model name
- vendor name
- algorithm type
- legal theory
- statistical proof
- source code access
- technical diagnosis

## Section 4. Pre-Deployment Deliberation Requirement

Agencies may not deploy first and deliberate later.

Before any covered automated system may exercise public authority, the agency must publish a deliberation record sufficient for future governance challenges.

No deliberation record means no automated authority.

Minimum deliberation record:

- covered system purpose
- legal authority for use
- affected population
- protected interests at stake
- model or rule family description
- plain-language explanation of decision logic
- feature governance record
- prohibited proxy assessment
- threshold policy
- drift tolerance policy
- validation evidence
- disparate impact assessment
- appeal pathway
- human review policy
- public comment or equivalent deliberation record
- sunset or renewal date

## Section 5. Deliberation Record Hash

The deliberation record must be content-addressed.

Every covered system manifest must reference:

```json
{
  "deliberation_record_hash": "sha256:REPLACE_WITH_HASH",
  "deliberation_record_uri": "REPLACE_WITH_PUBLIC_URI",
  "plain_language_logic_uri": "REPLACE_WITH_PUBLIC_URI"
}
```

If the deliberation record cannot be produced, the system enters:

```txt
GOVERNANCE_AUTHORITY_SUSPENDED
```

## Section 6. Ungovernable Model Sunset

A model whose policy logic cannot be explained in plain language to the affected person loses automated authority.

The explanation must be understandable to the person affected, not merely to:

- a judge
- a vendor
- a technical auditor
- a regulator
- an expert witness

Replay perfection is irrelevant if the system cannot explain the governing logic of the decision in plain language.

```txt
INCOMPREHENSIBLE_PUBLIC_POWER IS UNGOVERNABLE PUBLIC POWER.
```

## Section 7. Plain-Language Explanation Standard

The explanation must identify:

- what rule or policy was applied
- what information mattered most
- what threshold or condition was not met
- what the person can contest
- what evidence could change the result
- whether a human can override or revise the result

The explanation may not rely on:

- confidence scores alone
- proprietary secrecy alone
- vague risk categories
- unexplained feature weights
- generic model-card summaries
- inaccessible technical jargon

## Section 8. Challenge Grounds

A MODEL_GOVERNANCE_CHALLENGE may allege that the system:

- applies an unlawful policy
- applies an arbitrary threshold
- uses prohibited proxies
- produces disparate impact without sufficient justification
- lacks meaningful human review
- lacks a public deliberation record
- lacks plain-language explainability
- permits unjust drift tolerance
- changes policy without notice
- relies on unavailable or unverifiable inputs
- converts score into verdict
- denies appeal by design

## Section 9. Burden Allocation

The citizen bears only the burden of opening the challenge and describing the harm or suspected wrong in ordinary language.

The operator bears the burden to produce:

- deliberation record
- plain-language explanation
- policy hash
- threshold record
- feature governance record
- validation record
- disparate impact record
- drift policy
- human review pathway

If the operator cannot produce these records, automated authority is suspended.

## Section 10. Remedies

Available remedies include:

```txt
HUMAN_REVIEW_REQUIRED
THRESHOLD_REVIEW_REQUIRED
POLICY_RECORD_REQUIRED
FEATURE_REVIEW_REQUIRED
DISPARATE_IMPACT_REVIEW_REQUIRED
MODEL_WITHDRAWAL_REQUIRED
GOVERNANCE_AUTHORITY_SUSPENDED
UNGOVERNABLE_MODEL_SUNSET
PUBLIC_RULEMAKING_REQUIRED
COURT_REVIEW_AVAILABLE
```

## Section 11. Emergency Relief

If the automated decision threatens imminent loss of housing, benefits, employment, liberty, medical access, safety access, or legal status, the challenge triggers urgent human review.

The automated decision may not execute irreparable adverse consequences while governance review is pending unless a human official issues a written emergency justification.

## Section 12. Trade Secret Boundary

Trade-secret claims may protect implementation details.

They may not eliminate constitutional review.

At minimum, the affected person must receive a plain-language explanation of:

- the governing policy
- the decisive information categories
- the threshold or condition applied
- the appeal route
- what evidence could change the result

A system that cannot provide this minimum explanation is ungovernable for public authority.

## Section 13. Separation From Execution Fidelity

Execution fidelity asks:

```txt
Did the system do what the manifest says it did?
```

Model governance asks:

```txt
Was the system allowed to do that at all?
```

A system may pass execution replay and fail governance review.

A valid hash does not cure an invalid rule.

A stable model does not cure an unjust threshold.

A replayable denial does not become lawful merely because it replayed perfectly.

## Section 14. Closing Doctrine

```txt
NO DELIBERATION RECORD, NO AUTOMATED AUTHORITY.
NO PLAIN-LANGUAGE EXPLANATION, NO AUTOMATED AUTHORITY.
NO MODEL GOVERNANCE PATHWAY, NO PUBLIC POWER.
```

ALMS preserves the record.

MODEL_GOVERNANCE_CHALLENGE preserves the right to contest the rule behind the record.
