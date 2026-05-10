# AGENCY IMPLEMENTATION CHECKLIST

## Status

AGENCY_IMPLEMENTATION_CHECKLIST_V1  
BRIDGE_BETWEEN_ALMS_AND_MODEL_GOVERNANCE_CHALLENGE  
OPERATIONAL_WORKFLOW_SPEC  
NO_TRIAGE_AS_DISPOSITION

## Purpose

This checklist turns ALMS and MODEL_GOVERNANCE_CHALLENGE into an agency-scale workflow.

It is designed for the hard case: an agency receives 10,000 plain-language objections in one week.

The answer must be neither chaos nor denial-by-backlog.

The system must auto-attach evidence, generate replayable explanations, surface governance patterns, and preserve human review.

## Core Workflow

```txt
citizen objection
→ auto-attach manifest
→ staff review mapped record
→ generate replayable explanation
→ sustain or escalate to governance review
→ public dashboard update
→ ungovernability review if pattern threshold met
```

Each step must be individually auditable.

No step may require the citizen to do more than state, in ordinary language, that the decision seems wrong.

## Section 1. Intake Standard

A valid challenge may begin with:

```txt
The computer said no and I think that is wrong.
```

The intake surface must not require:

- model name
- vendor name
- legal theory
- policy hash
- technical diagnosis
- statistical proof
- source code access
- knowledge of ALMS

The agency bears the burden of translating the objection into the correct review path.

## Section 2. Automatic Evidence Attachment

At intake, the system must automatically attach the ALMS evidence packet before staff review.

Minimum evidence packet:

```json
{
  "challenge_id": "REPLACE_WITH_CHALLENGE_ID",
  "decision_id": "REPLACE_WITH_DECISION_ID",
  "manifest_hash": "sha256:REPLACE_WITH_MANIFEST_HASH",
  "manifest_uri": "REPLACE_WITH_URI",
  "output_receipt_hash": "sha256:REPLACE_WITH_OUTPUT_HASH",
  "policy_hash": "sha256:REPLACE_WITH_POLICY_HASH",
  "model_identifier": "REPLACE_WITH_MODEL_ID",
  "decision_timestamp": "REPLACE_WITH_TIMESTAMP",
  "audit_log_ref": "REPLACE_WITH_REF",
  "drift_events": [],
  "replay_status": "verified|review_required|suspended|invalid|unknown",
  "governance_record_ref": "REPLACE_WITH_REF"
}
```

No staff member should hunt logs manually.

No citizen should be asked to locate technical records the agency already controls.

## Section 3. Triage Automation That Preserves Human Review

Triage may classify.

Triage may not adjudicate.

Allowed triage outputs:

```txt
EXECUTION_FIDELITY_REVIEW
MODEL_GOVERNANCE_REVIEW
BOTH_TRACKS_REQUIRED
URGENT_HUMAN_REVIEW
INCOMPLETE_RECORD_REVIEW
PATTERN_SIGNAL_DETECTED
```

Forbidden triage outputs:

```txt
AUTO_DENIED
AUTO_DISMISSED
AUTO_VALIDATED_WITHOUT_HUMAN
AUTO_ESCALATED_TO_PENALTY
AUTO_CLOSED_AS_DUPLICATE_WITHOUT_REVIEW
```

The classification is procedural.

It is not a disposition.

If triage becomes disposition, the intake layer has become the new black box.

## Section 4. Staff Review Mapped Record

Staff must see the citizen objection mapped onto the evidence packet.

Review view must show:

- citizen statement
- affected decision
- manifest hash
- replay status
- drift status
- policy hash
- deliberation record status
- plain-language explanation status
- prior similar challenges
- urgent harm flag
- recommended review track

Staff must record whether the challenge proceeds as:

```txt
EXECUTION_FIDELITY_CHALLENGE
MODEL_GOVERNANCE_CHALLENGE
BOTH_TRACKS_REQUIRED
```

A routing decision must be logged with a reason.

## Section 5. Replayable Explanation Generator

When an affected person asks why, the system must generate a plain-language explanation tied to a specific model version, policy hash, and manifest hash.

The explanation must itself be replayable.

Meaning:

- it references the same manifest hash as the decision
- it references the same policy hash
- it identifies the model or rule version
- it describes the governing logic in plain language
- it can be regenerated from the same decision record
- it does not drift silently across versions

Minimum explanation record:

```json
{
  "type": "REPLAYABLE_EXPLANATION_RECORD",
  "challenge_id": "REPLACE_WITH_CHALLENGE_ID",
  "decision_id": "REPLACE_WITH_DECISION_ID",
  "manifest_hash": "sha256:REPLACE_WITH_MANIFEST_HASH",
  "policy_hash": "sha256:REPLACE_WITH_POLICY_HASH",
  "model_identifier": "REPLACE_WITH_MODEL_ID",
  "plain_language_explanation": "REPLACE_WITH_EXPLANATION",
  "decisive_information_categories": [],
  "threshold_or_condition_applied": "REPLACE_WITH_THRESHOLD",
  "what_can_be_contested": [],
  "what_evidence_could_change_result": [],
  "generated_at": "REPLACE_WITH_TIMESTAMP",
  "explanation_hash": "sha256:REPLACE_WITH_EXPLANATION_HASH"
}
```

The explanation does not justify the policy.

It describes what the system considered and how the decision logic operated.

Policy justification belongs in MODEL_GOVERNANCE_CHALLENGE.

## Section 6. Ungovernable Explanation Failure

If a plain-language explanation cannot be generated, the system must enter:

```txt
UNGOVERNABLE_EXPLANATION_FAILURE
```

If the explanation cannot be tied to the decision manifest and policy hash, the system must enter:

```txt
EXPLANATION_REPLAY_FAILURE
```

Either condition triggers MODEL_GOVERNANCE_REVIEW.

Repeated explanation failure triggers ungovernability review.

## Section 7. Public Governance Outcomes Dashboard

Agencies must publish a public dashboard showing governance challenge patterns.

The dashboard is not a naming-and-shaming surface.

It is a structural early-warning system.

Dashboard fields:

- covered system ID
- decision domain
- total challenges
- challenge rate per 1,000 decisions
- execution fidelity challenges
- model governance challenges
- both-track challenges
- urgent human reviews
- replay failures
- explanation failures
- governance challenges upheld
- governance challenges denied
- pending reviews
- average time to human review
- pattern threshold status
- ungovernability review status

The dashboard must not disclose private personal data.

The dashboard must show patterns before harm reaches class-action scale.

## Section 8. Pattern Thresholds

A covered system must enter PATTERN_REVIEW when one or more conditions are met:

```txt
explanation_failure_rate exceeds threshold
replay_failure_rate exceeds threshold
governance_challenge_rate exceeds threshold
urgent_human_review_rate exceeds threshold
upheld_challenge_rate exceeds threshold
same policy hash generates repeated successful challenges
same feature category appears in repeated successful challenges
same population reports repeated adverse outcomes
```

Pattern thresholds must be published before deployment.

Thresholds may not be secretly raised to avoid review.

Threshold changes must be logged as policy changes.

## Section 9. Ungovernability Review

A system enters UNGOVERNABILITY_REVIEW when:

- plain-language explanations repeatedly fail
- deliberation record is missing
- policy logic cannot be described to affected persons
- governance challenges are repeatedly upheld
- drift threshold is repeatedly challenged and unsupported
- feature governance record is missing or defective
- human review routinely reverses automated outcomes

Possible outcomes:

```txt
CONTINUE_WITH_MONITORING
REQUIRE_POLICY_REVISION
REQUIRE_THRESHOLD_REVISION
REQUIRE_FEATURE_REVIEW
REQUIRE_NEW_DELIBERATION_RECORD
SUSPEND_AUTOMATED_AUTHORITY
SUNSET_UNGOVERNABLE_MODEL
```

## Section 10. Operational Queue Discipline

High volume does not suspend rights.

When challenge volume exceeds staffing capacity, the agency must:

- preserve all incoming challenges
- auto-attach ALMS evidence packets
- prioritize urgent harm cases
- publish backlog metrics
- request emergency review staffing
- pause automated adverse execution when backlog threatens meaningful review

Backlog is not a defense to due process failure.

## Section 11. Audit Requirements

Each step must emit an audit entry:

```txt
CHALLENGE_RECEIVED
MANIFEST_ATTACHED
TRIAGE_CLASSIFIED
STAFF_ROUTE_RECORDED
EXPLANATION_GENERATED
EXPLANATION_FAILED
HUMAN_REVIEW_OPENED
GOVERNANCE_REVIEW_OPENED
PATTERN_SIGNAL_DETECTED
UNGOVERNABILITY_REVIEW_OPENED
CASE_RESOLVED
DASHBOARD_UPDATED
```

Audit entries must include timestamp, actor or system component, challenge ID, decision ID, manifest hash, and resulting state.

## Section 12. Prohibited Agency Practices

Agencies may not:

- deny challenges because the citizen lacks technical vocabulary
- require citizens to locate manifests
- use triage classification as final disposition
- hide governance challenge patterns
- regenerate explanations untethered from manifest hashes
- raise pattern thresholds after deployment without public notice
- treat replay success as proof of justice
- close cases solely because many similar cases exist
- replace human review with explanation generation

## Section 13. Closing Doctrine

```txt
TRIAGE MAY CLASSIFY.
TRIAGE MAY NOT DECIDE.

EXPLANATION MUST REPLAY.
EXPLANATION MAY NOT JUSTIFY WHAT GOVERNANCE HAS NOT DEFENDED.

PATTERNS MUST SURFACE BEFORE HARM BECOMES A CLASS ACTION.
```

This checklist couples ALMS and MODEL_GOVERNANCE_CHALLENGE without collapsing them into each other.

Execution fidelity remains about whether the machine did what it said.

Model governance remains about whether the machine was allowed to do that at all.
