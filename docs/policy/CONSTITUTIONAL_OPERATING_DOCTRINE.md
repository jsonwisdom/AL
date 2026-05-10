# CONSTITUTIONAL OPERATING DOCTRINE

## Status

CONSTITUTIONAL_OPERATING_DOCTRINE_V1  
UNIFIED_FRAMEWORK_FOR_MACHINE_MEDIATED_PUBLIC_POWER  
AI_CLARITY_ACT_EXTENSION  
ALMS_MODEL_GOVERNANCE_TRIAGE_BRIDGE

## 0. Unified Preamble

When government uses automated systems to determine or materially influence liberty, property, benefits, eligibility, enforcement, or access to public opportunity, due process requires more than after-the-fact explanation. The state may not delegate public power to uninspectable processes. If the state acts at machine speed, the affected person must be able to trigger verification at machine speed. Replayable execution proves only what the machine did; it does not prove that the rule was lawful, fair, or constitutional. And when delay functions as denial, queue design itself becomes adjudication. Machine-mediated public power is constitutionally valid only when its decisions are replayable, its governance record is challengeable, and its review path remains meaningful to the person affected.

## 1. Incorporated Protocols

This doctrine binds five protocols into one operating framework:

1. `alms_citizen_relay_system.md`
2. `MODEL_GOVERNANCE_CHALLENGE.md`
3. `AGENCY_IMPLEMENTATION_CHECKLIST.md`
4. `TRIAGE_AUDIT_PROTOCOL.md`
5. `ai_clarity_act_executive_order_draft.md`

Together they define constitutional due process for machine-mediated state power.

This is not AI ethics.

This is not responsible innovation branding.

This is constitutional procedure adapted to systems that decide, route, score, explain, and enforce at machine speed.

## 2. Definitions

| Term | Definition | Primary Protocol |
|---|---|---|
| `ALMS` | Audit Ledger Manifest Store; the triple-write, content-addressed civic record system for replay manifests and verification results. | ALMS Citizen Relay System |
| `ALMS_DECISION_REPLAY_MANIFEST` | Machine-readable record of a covered automated decision, including model identifier, policy hash, transformation chain hash, output receipt hash, and replay requirements. | ALMS Citizen Relay System |
| `APPEND_ONLY_AUDIT` | A record structure where new events may be added but prior events may not be silently rewritten or deleted. | ALMS / Agency Checklist |
| `AUTOMATED_ROUTING_AUTHORITY_SUSPENDED` | State entered when a triage system loses authority to route cases automatically due to replay or explanation failure. | Triage Audit Protocol |
| `BOTH_TRACKS_REQUIRED` | Routing state where a challenge must proceed through both execution fidelity review and model governance review. | Agency Checklist |
| `CITIZEN_REPLAY_RIGHT` | The right of an affected person or independent agent to retrieve and inspect replay surfaces without operator permission. | ALMS Citizen Relay System |
| `COVERED_SYSTEM` | Any automated or semi-automated system that determines or materially influences public outcomes or protected interests. | AI Clarity Act / ALMS |
| `DELAY_FUNCTIONS_AS_DENIAL` | State triggered when queue latency makes review functionally unavailable or meaningless. | Triage Audit Protocol |
| `EXECUTION_FIDELITY_CHALLENGE` | Challenge asking whether the system did what the manifest says it did. | ALMS / Implementation Memo |
| `GOVERNANCE_AUTHORITY_SUSPENDED` | State entered when a system lacks required governance records or plain-language explainability. | Model Governance Challenge |
| `HIGH_IMPACT_SYSTEM` | Covered system affecting benefits, housing, employment, credit, eligibility, legal recommendation, safety-critical access, education, medical access, immigration, or enforcement prioritization. | AI Clarity Act / Model Governance |
| `HUMAN_REVIEW_REQUIRED` | State requiring a qualified human official to review the decision, record, or challenge before adverse automated authority continues. | ALMS / Agency Checklist / Triage |
| `LEGACY_REVIEW_REQUIRED` | Migration state for pre-ALMS systems that remain active or relied upon but lack full replay surfaces. | ALMS Implementation Memo |
| `MATERIALLY CONSEQUENTIAL` | Capable of affecting liberty, property, benefits, eligibility, housing, credit, employment, legal exposure, public safety access, medical access, education opportunity, or public-sector prioritization. | AI Clarity Act |
| `MODEL_GOVERNANCE_CHALLENGE` | Challenge asking whether the system was allowed to do what it did, even if execution replay succeeds. | Model Governance Challenge |
| `NO_OPERATOR_PERMISSION` | Verification must not require the system operator's approval, credential, API key, or private dashboard access. | ALMS Citizen Relay System |
| `PATTERN_REVIEW` | Review triggered when repeated challenges, explanation failures, replay failures, or upheld complaints indicate systemic risk. | Agency Checklist |
| `PLAIN_LANGUAGE_EXPLANATION` | Explanation understandable to the affected person, identifying the rule applied, decisive information, threshold, contestable points, and evidence that could change the result. | Model Governance / Agency Checklist |
| `REPLAY_FAILURE` | Failure to reproduce or verify the relevant manifest, output, routing classification, explanation, or audit chain. | ALMS / Triage |
| `REPLAYABLE_EXPLANATION_RECORD` | Plain-language explanation tied to a decision ID, manifest hash, policy hash, model version, and explanation hash. | Agency Checklist |
| `STANDARD_HUMAN_QUEUE` | Default non-urgent human review queue used when automated triage replay fails or routing authority is suspended. | Triage Audit Protocol |
| `SUSPENDED` | State where automated authority pauses pending human review, replay repair, or governance review. | ALMS Citizen Relay System |
| `TRIAGE_ROUTING_MANIFEST` | ALMS-covered manifest for routing decisions, including triage model ID, policy hash, routing output, confidence, queue ID, and manifest hash. | Triage Audit Protocol |
| `UNGOVERNABLE_EXPLANATION_FAILURE` | State entered when a model or triage system cannot explain in plain language why a decision or route occurred. | Model Governance / Triage |
| `UNGOVERNABLE_MODEL_SUNSET` | Remedy removing automated authority from a model whose public logic cannot be explained to affected persons. | Model Governance Challenge |
| `VOID_AB_INITIO` | Legal consequence for unreplayable punitive or adverse legal outputs: the output is treated as invalid from inception and may not be cited or used downstream. | ALMS Citizen Relay System |

## 3. Citizen Challenge Flow

Readable architecture for the person whose rights are affected:

```txt
PERSON SAYS:
  "The computer said no and I think that is wrong."

        ↓

INTAKE ACCEPTS CHALLENGE
  Governed by: MODEL_GOVERNANCE_CHALLENGE + AGENCY_IMPLEMENTATION_CHECKLIST
  Rule: no technical vocabulary required

        ↓

ALMS EVIDENCE AUTO-ATTACHED
  Governed by: ALMS_CITIZEN_RELAY_SYSTEM
  Attached: manifest hash, policy hash, model ID, output receipt, audit log, replay status

        ↓

TRIAGE CLASSIFIES ROUTE
  Governed by: TRIAGE_AUDIT_PROTOCOL
  Rule: triage may classify; triage may not decide
  Output: EXECUTION_FIDELITY_CHALLENGE / MODEL_GOVERNANCE_CHALLENGE / BOTH_TRACKS_REQUIRED / URGENT_HUMAN_REVIEW

        ↓

TRIAGE ROUTING REPLAYS
  Governed by: TRIAGE_AUDIT_PROTOCOL
  Citizen can verify: classified as X, version Y, policy hash Z, queue Q
  Failure: default to STANDARD_HUMAN_QUEUE or URGENT_HUMAN_REVIEW

        ↓

REPLAYABLE EXPLANATION GENERATED
  Governed by: AGENCY_IMPLEMENTATION_CHECKLIST + MODEL_GOVERNANCE_CHALLENGE
  Rule: explanation tied to manifest hash and policy hash
  Failure: UNGOVERNABLE_EXPLANATION_FAILURE

        ↓

TRACK 1: EXECUTION FIDELITY REVIEW
  Governed by: ALMS
  Question: did the system do what the record says?
  Failure: SUSPENDED or VOID_AB_INITIO for punitive/legal outputs

        ↓

TRACK 2: MODEL GOVERNANCE REVIEW
  Governed by: MODEL_GOVERNANCE_CHALLENGE
  Question: was the system allowed to do that at all?
  Failure: policy revision, threshold review, model withdrawal, or UNGOVERNABLE_MODEL_SUNSET

        ↓

PUBLIC DASHBOARD UPDATES
  Governed by: AGENCY_IMPLEMENTATION_CHECKLIST + TRIAGE_AUDIT_PROTOCOL
  Shows: challenge rates, latency, explanation failures, upheld challenges, pattern signals

        ↓

REMEDY
  Possible: human review, corrected decision, suspended authority, void output, policy revision, public rulemaking, model sunset, court review
```

## 4. Agency Obligations Table

| Protocol | Agency Obligation | Responsible Actor | Noncompliance Trigger | Required Remedy |
|---|---|---|---|---|
| AI Clarity Act | Identify covered and high-impact systems. | Agency head / CIO / program owner | Undisclosed automated system affecting protected interests | Inventory publication and REVIEW_REQUIRED |
| AI Clarity Act | Preserve replay surfaces for materially consequential outputs. | Program owner / system operator | Missing model ID, policy hash, timestamp, input provenance, transformation chain, or output hash | SUSPENDED until manifest is produced |
| ALMS | Publish decision manifest at time of decision. | System operator | Missing manifest after cutover | SUSPENDED; punitive/legal output VOID_AB_INITIO |
| ALMS | Triple-write manifest to agency, public records custodian, and content-addressable network. | Records officer / system operator | Missing store copy or hash mismatch | REVIEW_REQUIRED; presumption of invalidity |
| ALMS | Publish hourly Merkle anchor. | ALMS operator / records custodian | Missing root or timestamp authority | REVIEW_REQUIRED; anchor repair required |
| ALMS | Permit verification without operator permission. | System operator / vendor | API key, credential, dashboard-only access, or operator gatekeeping required | NO_OPERATOR_PERMISSION violation; SUSPENDED |
| Model Governance | Publish pre-deployment deliberation record. | Agency policy owner | No deliberation record | GOVERNANCE_AUTHORITY_SUSPENDED |
| Model Governance | Provide plain-language explanation to affected person. | Program owner / explanation service | Incomprehensible or missing explanation | UNGOVERNABLE_EXPLANATION_FAILURE |
| Model Governance | Maintain feature, threshold, validation, disparate impact, and drift policy records. | Model governance board / program owner | Missing or defective governance record | MODEL_GOVERNANCE_REVIEW |
| Agency Checklist | Auto-attach ALMS evidence packet at intake. | Challenge intake system | Staff or citizen required to hunt logs | INCOMPLETE_RECORD_REVIEW |
| Agency Checklist | Ensure triage classification is not disposition. | Intake owner / review supervisor | Auto-denial, auto-dismissal, auto-closure | HUMAN_REVIEW_REQUIRED; audit breach |
| Agency Checklist | Publish governance outcomes dashboard. | Agency transparency officer | Challenge patterns hidden or unavailable | PUBLIC_DASHBOARD_UPDATE_REQUIRED |
| Agency Checklist | Trigger pattern review when thresholds are crossed. | Governance board | Repeated failures ignored | PATTERN_REVIEW / UNGOVERNABILITY_REVIEW |
| Triage Audit | Treat triage as a covered system. | Intake owner / triage operator | Routing model lacks manifest | AUTOMATED_ROUTING_AUTHORITY_SUSPENDED |
| Triage Audit | Make routing outcomes replayable. | Triage operator | Routing cannot be reproduced from version and policy hash | Default to STANDARD_HUMAN_QUEUE or URGENT_HUMAN_REVIEW |
| Triage Audit | Publish queue latency by routing class. | Agency operations lead | Latency hidden or not broken out by class | DELAY_FUNCTIONS_AS_DENIAL review |
| Triage Audit | Explain routing in plain language. | Triage operator | Cannot explain why routed to queue | UNGOVERNABLE_EXPLANATION_FAILURE; suspend automated routing |

## 5. Two-Track Doctrine

### Track 1: Execution Fidelity

Execution fidelity asks:

```txt
Did the system do what the manifest says it did?
```

It is governed by ALMS.

Evidence includes:

- decision replay manifest
- manifest hash
- output receipt hash
- model identifier
- policy hash
- transformation chain hash
- triple-write persistence
- Merkle anchor
- audit log
- replay result

Execution failure may trigger:

```txt
SUSPENDED
REVIEW_REQUIRED
VOID_AB_INITIO
HUMAN_REVIEW_REQUIRED
```

### Track 2: Substantive Legitimacy

Substantive legitimacy asks:

```txt
Was the system allowed to do that at all?
```

It is governed by MODEL_GOVERNANCE_CHALLENGE.

Evidence includes:

- deliberation record
- legal authority
- plain-language logic
- feature governance
- threshold policy
- drift tolerance policy
- validation record
- disparate impact analysis
- public comment record
- human review pathway

Governance failure may trigger:

```txt
MODEL_GOVERNANCE_REVIEW
POLICY_REVISION_REQUIRED
THRESHOLD_REVIEW_REQUIRED
FEATURE_REVIEW_REQUIRED
GOVERNANCE_AUTHORITY_SUSPENDED
UNGOVERNABLE_MODEL_SUNSET
PUBLIC_RULEMAKING_REQUIRED
COURT_REVIEW_AVAILABLE
```

### The Firewall

```txt
REPLAY PROVES EXECUTION.
IT DOES NOT PROVE JUSTICE.
```

A valid hash does not cure an invalid rule.

A perfect replay does not cure an unlawful threshold.

A stable model does not cure an ungovernable explanation.

A timely queue does not cure a routing classifier that cannot be replayed.

### The Reunification at Remedy

The tracks separate diagnosis but reunify at remedy.

A single challenge may require:

- execution correction
- human review
- governance review
- public dashboard update
- pattern review
- court review
- suspension of automated authority

The citizen does not need to choose the correct legal or technical track.

The institution must route the challenge correctly and preserve review.

## 6. Closing Doctrine

```txt
NO MANIFEST, NO AUTHORITY.
NO REPLAY, NO AUTOMATED POWER.
NO DELIBERATION RECORD, NO AUTOMATED AUTHORITY.
NO PLAIN-LANGUAGE EXPLANATION, NO AUTOMATED AUTHORITY.
TRIAGE MAY CLASSIFY; TRIAGE MAY NOT DECIDE.
A DELAY THAT FUNCTIONS AS A DENIAL IS A DECISION.
A SCORE IS NOT A VERDICT.
CONSENSUS IS NOT CONVERGENCE.
```

The technology may change.

The rights do not.

This doctrine exists so public power implemented by machines remains public, reviewable, challengeable, and bounded by constitutional due process.
