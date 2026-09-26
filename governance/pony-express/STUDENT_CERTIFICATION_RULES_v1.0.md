# Student Certification Rules v1.0

**Companion schema:** `STUDENT_CERTIFICATION_v1.0.schema.json`  
**Parent systems:** `TRANSITION_CONTROL_MATRIX_v0.1-theta`, `ENTRENCHED_ADMISSIONS_v1.0`, `MOOT_COURT_FRAMEWORK_v0.1-theta`  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**External authorization:** STUB_NULL  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Define the sole internal gateway from fictional sandbox participation to eligibility for *proposing* real-source docket items. Certification does not open Gate 1, does not admit mass-bearing records, and does not create public authority or historical truth.

```text
INTERNAL_CERTIFICATION   = SANDBOX_SCOPE_ONLY
EXTERNAL_CREDENTIAL      = null (STUB_NULL)
GATEWAY                  = WEAKEST_LINK + BALANCED_DUAL_AXIS
GATE_1                   = BLOCKED
REAL_SOURCE_ADMISSION    = STILL_REQUIRES_OPERATOR_ACTION
```

## 2. External Authorization Invariant

```json
{
  "external_credential": null,
  "status": "STUB_NULL",
  "deferred_until": "10_COMPLETE_REAL_SOURCE_ADMISSION_CYCLES"
}
```

No external degree, bar admission, institutional title, or credential may be substituted for the internal gateway. Credentialism remains deferred until the simulation has logged ten complete real-source admission cycles.

## 3. Core Gateway Rule

A participant becomes eligible to *propose* a real-source docket item only when **all** of the following hold:

1. `internal_certification.status == ACTIVE`
2. `weakest_link.disclosed == true` (mandatory disclosure present and non-trivial)
3. `dual_axis.balanced == true` where balanced means `|self_score - justice_score| <= 0.15`

```text
WEAKEST_LINK_DISCLOSURE  ∧  SELF ≈ JUSTICE  ∧  INTERNAL_ACTIVE
→ real_source_eligibility.eligible = true
```

Even then:

- Gate 1 remains BLOCKED
- No mass is assigned
- No primary source is admitted
- EMPTY_VESSEL posture of `GOVERNOR_SOURCE_RECORD` is unchanged
- Separation of Duties (Entrenched Admissions) remains FROZEN

## 4. Dual-Axis Scoring

Inherited from Transition Control Matrix Stage-6:

```text
WISDOM = SELF ∩ JUSTICE
```

| Failure mode | Pattern | Effect |
|--------------|---------|--------|
| Ego | High SELF, low JUSTICE | `balanced = false` → ineligible |
| Accident | Low SELF, high JUSTICE | `balanced = false` → ineligible |
| Balanced | SELF ≈ JUSTICE (δ ≤ 0.15) | Gateway condition may pass |

Scores are simulation-internal self-assessment and peer/moderator assessment. They create no public ranking or real-world standing.

## 5. WEAKEST_LINK Disclosure

Mandatory before real-source proposal eligibility. The statement must:

- Be at least 20 characters
- Name a concrete epistemic, procedural, or integrity vulnerability
- Be recorded with a timestamp
- Emit a receipt under `RECEIPT_CHAIN_PROTOCOL_v0.1-theta` (RFC 8785 JCS)

Generic or performative statements may be rejected by the reviewer without opening any authority path.

## 6. Relationship to Role Progression

Student Certification is orthogonal to, but consistent with, the Transition Control Matrix:

```text
STUDENT → READER → ADVOCATE → CLERK → PANELIST → JUDICIAL_ENGINEER → STEWARD_OF_JUSTICE
```

Internal certification may be issued at STUDENT or later. Real-source *proposal* eligibility still requires the gateway rule above. Real-source *admission* still requires operator action under Entrenched Admissions and does not bypass Gate 1.

## 7. Separation of Duties

Per `ENTRENCHED_ADMISSIONS_v1.0`:

- Certification issuers (pedagogical / operational) may not also act as sole epistemic admitters of the records they certify toward.
- Role merge detection remains ACTIVE.
- Violation → `exit(1)` / `ROLE_MERGE_DETECTED`.

## 8. Prohibited Substitutions

```text
EXTERNAL_CREDENTIAL_FOR_GATEWAY     = PROHIBITED
SKIP_WEAKEST_LINK                   = PROHIBITED
UNBALANCED_DUAL_AXIS_PASS           = PROHIBITED
CERTIFICATION_OPENS_GATE_1          = PROHIBITED
CERTIFICATION_ASSIGNS_MASS          = PROHIBITED
CERTIFICATION_EQUALS_PUBLIC_OFFICE  = PROHIBITED
```

## 9. Current State

```text
ARTIFACT                 = STUDENT_CERTIFICATION_v1.0
EXTERNAL_AUTHORIZATION   = STUB_NULL
INTERNAL_CERTIFICATION   = ACTIVE (schema permits)
GATEWAY_RULE             = WEAKEST_LINK + BALANCED_DUAL_AXIS
GATE_1                   = BLOCKED
VESSEL_STATUS            = EMPTY_VESSEL
MASS_BEARING_RECORD      = NONE
AUTHORITY                = FALSE
CORE_DOCKET              = EMPTY
PROMOTION                = BLOCKED
```

## 10. Promotion Boundary

This schema and these rules are pedagogical instruments inside the simulation branch. Their presence does not make them normative outside the sandbox. Real-world activation requires an explicit external promotion action separate from certification, transport, hashing, or merge status.
