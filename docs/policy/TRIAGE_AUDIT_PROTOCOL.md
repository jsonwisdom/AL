# TRIAGE AUDIT PROTOCOL

## Status

TRIAGE_AUDIT_PROTOCOL_V1  
COVERED_SYSTEM_FOR_ALMS  
NO_TRIAGE_AS_DISPOSITION  
DELAY_AS_DECISION_RECOGNIZED

## Constitutional Principle

```txt
A DELAY THAT FUNCTIONS AS A DENIAL IS A DECISION.
A DECISION REQUIRES DUE PROCESS.
```

Triage determines whether and when a human sees a challenge. Therefore, triage is materially consequential and must itself be replayable, audited, explained, and publicly measured.

## 1. Triage Is a Covered System

Any automated or semi-automated classifier that routes citizen objections must publish an ALMS manifest.

Minimum triage manifest fields:

```json
{
  "type": "TRIAGE_ROUTING_MANIFEST",
  "challenge_id": "REPLACE_WITH_CHALLENGE_ID",
  "triage_model_id": "REPLACE_WITH_MODEL_ID",
  "triage_policy_hash": "sha256:REPLACE_WITH_POLICY_HASH",
  "triage_version": "REPLACE_WITH_VERSION",
  "routing_output": "URGENT_HUMAN_REVIEW|STANDARD_HUMAN_QUEUE|EXECUTION_FIDELITY_REVIEW|MODEL_GOVERNANCE_REVIEW|BOTH_TRACKS_REQUIRED|INCOMPLETE_RECORD_REVIEW",
  "confidence": "REPLACE_WITH_CONFIDENCE_OR_NULL",
  "queue_id": "REPLACE_WITH_QUEUE_ID",
  "manifest_hash": "sha256:REPLACE_WITH_MANIFEST_HASH",
  "operator_permission_required_for_verification": false
}
```

## 2. Routing Outcomes Must Replay

A citizen must be able to verify:

```txt
my challenge was classified as X
with confidence Y
by triage version Z
under policy hash P
and routed to queue Q
```

Replay must show whether routing was consistent with the published policy for that triage version.

If triage replay fails, the challenge defaults to:

```txt
STANDARD_HUMAN_QUEUE
```

or:

```txt
URGENT_HUMAN_REVIEW
```

when harm is imminent.

## 3. Classification Is Not Disposition

Triage may route.

Triage may not decide.

Forbidden outputs:

```txt
AUTO_DENIED
AUTO_DISMISSED
AUTO_CLOSED_BY_PRIORITY
AUTO_DELAYED_WITHOUT_REVIEW_DATE
AUTO_DUPLICATE_WITHOUT_HUMAN_CONFIRMATION
```

A queue assignment that produces no meaningful review is treated as a de facto decision and becomes reviewable.

## 4. Queue Latency Must Be Public

Agencies must publish queue latency by routing class.

Minimum public metrics:

```txt
queue_id
routing_class
open_cases
median_time_to_human_review
p90_time_to_human_review
p99_time_to_human_review
oldest_unreviewed_case_age
urgent_cases_pending
cases_exceeding_due_process_window
```

If LOW_PRIORITY or equivalent classes have extreme delay, the public can see that triage is functioning as denial-by-delay.

## 5. Delay Thresholds

Each routing class must publish a maximum time-to-human-review.

If the threshold is exceeded, the system must emit:

```txt
DELAY_FUNCTIONS_AS_DENIAL
```

Required consequence:

```txt
HUMAN_REVIEW_REQUIRED
QUEUE_REBALANCING_REQUIRED
PUBLIC_DASHBOARD_UPDATE_REQUIRED
```

Repeated threshold breach triggers MODEL_GOVERNANCE_REVIEW of the triage system.

## 6. Triage Explanation Requirement

The affected person must receive a plain-language explanation of why the challenge was routed to a particular queue.

The explanation must identify:

- routing class assigned
- queue assigned
- urgency factors considered
- missing evidence, if any
- harm flags considered
- expected time to human review
- how to contest routing

The explanation must not rely on feature weights, jargon, or hidden priority labels.

## 7. Ungovernable Triage Failure

If triage cannot explain in plain language why a case was routed to a queue, it enters:

```txt
UNGOVERNABLE_EXPLANATION_FAILURE
```

Consequence:

```txt
AUTOMATED_ROUTING_AUTHORITY_SUSPENDED
DEFAULT_TO_STANDARD_HUMAN_QUEUE
```

If imminent harm exists, default is:

```txt
URGENT_HUMAN_REVIEW
```

## 8. Public Anti-Backlog Rule

Backlog cannot be used to quietly extinguish rights.

When queue delay exceeds published thresholds, the agency must:

- publish delay breach
- preserve all challenges
- stop using low-priority routing as a shield
- allocate human review capacity
- suspend automated adverse action where review delay creates irreparable harm

## 9. Audit Events

Every triage action must emit audit entries:

```txt
TRIAGE_MANIFEST_CREATED
ROUTING_CLASS_ASSIGNED
QUEUE_ASSIGNED
TRIAGE_EXPLANATION_GENERATED
TRIAGE_REPLAY_VERIFIED
TRIAGE_REPLAY_FAILED
DELAY_THRESHOLD_BREACHED
DELAY_FUNCTIONS_AS_DENIAL
HUMAN_REVIEW_OPENED
ROUTING_CONTESTED
AUTOMATED_ROUTING_SUSPENDED
```

## Closing Doctrine

```txt
TRIAGE IS A COVERED SYSTEM.
ROUTING MUST REPLAY.
QUEUE DELAY MUST BE PUBLIC.
EXPLANATION FAILURE SUSPENDS AUTOMATED ROUTING.
```

The intake layer may never become the new black box.
