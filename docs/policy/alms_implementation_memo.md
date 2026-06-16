# ALMS Implementation Memo

## Status

IMPLEMENTATION_MEMO_V1  
AI_CLARITY_ACT_EXTENSION  
AUDIT_LEDGER_MANIFEST_STORE  
CITIZEN_RELAY_SYSTEM

## Purpose

This memo answers three implementation questions for the Audit Ledger Manifest Store (ALMS):

1. How existing automated systems migrate into ALMS.
2. How independent observers are funded without capture.
3. How citizens challenge model design when replay succeeds but the system is still unjust.

## 1. Existing Systems and Migration

### Rule

ALMS shall not retroactively erase all pre-ALMS automated decisions.

But any pre-ALMS decision still under appeal, enforcement, renewal, review, downstream scoring, or legal reliance must become replayable or lose automated authority.

### Cutover Structure

Covered systems shall enter one of four migration states:

```txt
LEGACY_PENDING_INVENTORY
LEGACY_REPLAYABLE
LEGACY_REVIEW_REQUIRED
LEGACY_AUTHORITY_SUSPENDED
```

### Timeline

Within 90 days:

- agencies publish inventory of covered automated systems
- each system receives a replayability classification
- all active systems must declare whether manifests can be reconstructed

Within 180 days:

- new materially consequential outputs must write ALMS manifests at time of decision
- legacy systems unable to produce manifests enter REVIEW_REQUIRED

Within 365 days:

- covered systems without ALMS-compatible replay surfaces may not issue new automated adverse actions

### Retroactivity Rule

VOID_AB_INITIO applies immediately to post-cutover covered decisions that lack valid replay.

For pre-cutover decisions:

- if still under appeal or active enforcement, replay failure creates a rebuttable presumption in favor of the citizen
- if punitive or adverse legal use continues after cutover, unreplayable output becomes inadmissible
- if the decision is final and no longer relied upon, ALMS flags it as LEGACY_UNREPLAYABLE rather than voiding it automatically

## 2. Observer Economics and Anti-Capture Funding

### Principle

Do not license observers.

License the verifier.

Any person, newsroom, university lab, civil society group, public defender, auditor, or citizen agent that runs the open-source ALMS verifier and publishes results may act as an observer.

### Funding Mechanism

Covered systems shall pay a small audit fee into an ALMS Observer Independence Fund.

Funds shall be distributed by rule-based lottery, not agency discretion.

Eligible categories:

- press organizations
- university labs
- civil society organizations
- public defender or legal aid entities
- private auditors
- foreign academic partners
- local civic technology groups

### Anti-Capture Rules

No single agency may select its own observers.

No covered vendor may fund an observer directly for verification of its own system.

Observer grants must be public, rotating, and time-limited.

Observer results must be independently reproducible and published with:

- verifier version
- manifest hash
- replay timestamp
- verification result
- signature or public authentication proof

### Civic Observer Clause

Official observer pools are not exclusive.

A non-funded observer running the public verifier can still produce a legally cognizable replay failure if the result is reproducible.

Observer independence is a property of the protocol, not a credential of the institution.

## 3. Semantic and Model-Design Challenges

### Problem

Replay fidelity proves that the machine did what the manifest says it did.

It does not prove that the model design, policy threshold, feature selection, drift tolerance, or objective function is just.

Execution correctness is not substantive legitimacy.

### Two-Track Review

ALMS therefore separates challenges into two tracks:

```txt
EXECUTION_FIDELITY_CHALLENGE
MODEL_GOVERNANCE_CHALLENGE
```

### Execution Fidelity Challenge

Question:

```txt
Did the system execute as recorded?
```

Evidence:

- manifest hash
- replay path
- output receipt
- drift log
- audit chain

Remedy:

- suspend authority if replay fails
- correct manifest or output if mismatch is proven
- void punitive/legal output when unreplayable

### Model Governance Challenge

Question:

```txt
Was the system design lawful, fair, and constitutionally sufficient even if replay succeeds?
```

Evidence:

- model card
- policy hash
- threshold policy
- feature governance record
- validation studies
- disparate impact analysis
- public comment record
- expert review
- constitutional risk assessment

Remedy:

- human review
- threshold suspension
- policy revision
- model withdrawal
- public rulemaking
- court review

### Semantic Review Trigger

A citizen may trigger MODEL_GOVERNANCE_CHALLENGE when:

- replay succeeds but the citizen disputes the governing rule
- model threshold appears arbitrary or discriminatory
- feature selection encodes prohibited proxies
- drift threshold was set to tolerate unjust degradation
- policy hash changed without meaningful notice
- system passes execution replay but produces structurally suspect outcomes

### Burden Rule

For execution failure, burden shifts to the operator to prove replayability.

For model-governance challenges, the operator must disclose sufficient design record for meaningful review without exposing private individual data beyond lawful bounds.

Trade-secret claims may protect source details but may not eliminate constitutional review of covered systems.

## 4. Unified Consequence Matrix

| Failure Mode | State | Consequence |
|---|---|---|
| Missing manifest after cutover | SUSPENDED | no further automated action |
| Triple-write mismatch | REVIEW_REQUIRED | burden shifts to operator |
| Merkle anchor missing | REVIEW_REQUIRED | manifest presumed incomplete |
| Replay failure in benefits/housing/employment/credit/eligibility | SUSPENDED | human review within 72 hours |
| Replay failure in punitive/legal recommendation | VOID_AB_INITIO | output inadmissible downstream |
| Replay succeeds but design challenged | MODEL_GOVERNANCE_REVIEW | substantive review required |
| Drift threshold disputed | MODEL_GOVERNANCE_REVIEW | threshold record required |
| Observer disagreement | DIVERGENT | no automated upgrade |

## 5. Closing Rule

```txt
REPLAY PROVES EXECUTION.
IT DOES NOT PROVE JUSTICE.
```

ALMS preserves the record needed to challenge both.
