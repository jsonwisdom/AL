# BASE_AGENTIC_BATCH_HIRING_REPLAY_V1

Status: canonical draft
Class: agentic hiring replay surface
Boundary: evaluation assistance only; no autonomous employment decision authority

## Purpose

Replay an agentic batch hiring pipeline as a constitutional workflow where every scoring, ranking, escalation, and rejection event is auditable, bounded, and contestable.

This system does not grant agents authority to hire, reject, discriminate, or make final employment decisions. It creates replayable evidence for human review.

## Core invariant

> No hiring outcome without replayable evidence, human review, and contestable rationale.

## Batch lifecycle

```text
B0_BATCH_INTAKE
  -> B1_ELIGIBILITY_NORMALIZATION
  -> B2_AGENTIC_SCREENING_ASSIST
  -> B3_BIAS_AND_POLICY_GATE
  -> B4_HUMAN_REVIEW_REQUIRED
  -> B5_DECISION_RECEIPT_GENERATED
  -> B6_APPEAL_OR_CONTEST_WINDOW
  -> B7_ARCHIVE_AND_REPLAY_SEAL
```

## B0_BATCH_INTAKE

Required inputs:

- batch_id
- role_id
- role_description_hash
- candidate_record_hashes[]
- intake_timestamp
- consent_or_lawful_basis_record
- evaluator_policy_hash

Invariant:

```text
candidate_raw_data must not be mutated after intake_hash is sealed
```

Failure:

```text
INTAKE_MUTATION_DETECTED
```

## B1_ELIGIBILITY_NORMALIZATION

Purpose:
Normalize candidate records into comparable, privacy-bounded evaluation objects.

Required outputs:

- normalized_candidate_hash
- redaction_map_hash
- eligibility_criteria_hash
- normalization_agent_id
- normalization_receipt_hash

Invariant:

```text
normalization must be replayable from intake data and policy hash
```

Failure:

```text
NON_REPLAYABLE_NORMALIZATION
```

## B2_AGENTIC_SCREENING_ASSIST

Purpose:
Use agents to assist with structured evidence extraction, not final decisions.

Allowed outputs:

- evidence_match_summary
- uncertainty_flags
- missing_information_flags
- candidate_question_suggestions
- role_fit_assist_score

Forbidden outputs:

- final_hire_decision
- final_reject_decision
- protected_class_inference
- unreviewable_black_box_rank

Invariant:

```text
agentic_score.legitimacy_effect == advisory_only
```

Failure:

```text
AGENT_DECISION_AUTHORITY_BREACH
```

## B3_BIAS_AND_POLICY_GATE

Purpose:
Detect policy violations, unsupported inferences, protected-class leakage, and inconsistent scoring.

Required checks:

- protected_attribute_proxy_scan
- adverse_impact_signal_check
- score_reason_alignment_check
- evidence_source_trace_check
- comparable_candidate_consistency_check

Failure labels:

```text
PROTECTED_PROXY_RISK
UNSUPPORTED_INFERENCE
SCORE_REASON_MISMATCH
EVIDENCE_TRACE_MISSING
COMPARABLE_CANDIDATE_INCONSISTENCY
```

If any hard failure occurs:

```text
status = HUMAN_REVIEW_ESCALATED
```

## B4_HUMAN_REVIEW_REQUIRED

Purpose:
Ensure no candidate outcome is finalized by agentic output alone.

Required human review receipt:

- reviewer_id_hash
- review_timestamp
- evidence_reviewed_hashes[]
- rationale_hash
- override_or_accept_agent_assist
- reviewer_attestation_signature

Invariant:

```text
final_decision requires human_review_receipt
```

Failure:

```text
NO_HUMAN_REVIEW_FOR_HIRING_OUTCOME
```

## B5_DECISION_RECEIPT_GENERATED

Required fields:

- decision_receipt_id
- candidate_hash
- role_id
- decision_label
- evidence_refs[]
- human_review_receipt_hash
- policy_hash
- contest_window
- receipt_signature

Permitted decision labels:

```text
ADVANCE_TO_NEXT_STAGE
HOLD_FOR_MORE_INFO
NOT_ADVANCED_WITH_RATIONALE
WITHDRAWN_BY_CANDIDATE
INELIGIBLE_POLICY_DEFINED
```

Forbidden labels:

```text
AI_REJECTED
AI_HIRED
UNEXPLAINED_RANK_ELIMINATION
```

## B6_APPEAL_OR_CONTEST_WINDOW

Purpose:
Permit contestability before archival finality.

Required surfaces:

- candidate_accessible_reason_summary
- correction_submission_channel
- contest_deadline
- review_reopen_rule

Invariant:

```text
contest_window must be declared before archive seal
```

Failure:

```text
NO_CONTESTABILITY_WINDOW
```

## B7_ARCHIVE_AND_REPLAY_SEAL

Required archive fields:

- batch_archive_id
- decision_receipts[]
- policy_hashes[]
- model_or_agent_versions[]
- replay_environment_hash
- bias_gate_results[]
- human_review_receipts[]
- contest_records[]
- canonical_encoded_lesson

Archive rule:

```text
archive replay allowed for audit_only mode
archive replay forbidden for retroactive decision laundering
```

Failure:

```text
HIRING_DECISION_LAUNDERING_DETECTED
```

## Base anchoring boundary

Optional onchain anchoring may publish only:

- batch_archive_id
- Merkle root of decision receipts
- timestamp
- schema version

Forbidden onchain publication:

- candidate names
- resumes
- protected attributes
- private rationale text
- personal identifying information

## Replay verdicts

```text
BATCH_REPLAY_VALID
BATCH_REPLAY_VALID_WITH_WARNINGS
BATCH_REPLAY_INVALID
HUMAN_REVIEW_REQUIRED
CONTESTABILITY_REQUIRED
```

## Encoded lesson

> Agentic hiring may assist judgment, but legitimacy requires replayable evidence, human review, and contestable outcomes.
