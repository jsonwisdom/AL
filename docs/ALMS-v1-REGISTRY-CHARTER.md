# ALMS-v1-REGISTRY-CHARTER.md

## Autonomous Ledger for Machine & Institutional Sovereignty — Registry Charter

```text
DOCUMENT TYPE:    constitutional_surface
EPOCH:            ALMS-v1
EPOCH_OBJECT:     ALMS-v1-EPOCH-0001
PARENT_SURFACE:   ALMS-v1-TREATIES.md
EXTENSION_RULE:   EXTEND_ONLY
V0_MUTATION:      false
STATUS:           CANONICAL
DEPENDS_ON:       Treaty IV.1, IV.2, IV.3, IV.4
```

## Preamble

This Charter defines the complete legal order governing registries under ALMS v1.
It implements and extends Treaty IV (Registry Law) without modifying it.

A Registry is the identity and standing layer of ALMS. It does not evaluate truth.
It does not override courts. It does not replay claims. It does one thing:

> A Registry establishes, maintains, and publishes the verified identities and standing records of operators authorized to produce admissible claims — and it does so under a replayable, tamper-evident authorization chain that descends without break from the epoch seed.

All registry operations are claims under ALMS law. All registry claims are subject to provenance completeness, non-repudiation, and replay supremacy.

A registry that cannot prove its own authorization chain is not a registry. It is an impersonator.

## Part I — Authorization Model

### Charter I.1 — Model Declaration

ALMS v1 uses the Peer Authorization with Epoch Seed model:

```text
AUTHORIZATION_MODEL:  PEER_AUTHORIZATION_WITH_EPOCH_SEED
SEED_AUTHORITY:       ALMS-v1-EPOCH-0001
EXPANSION_RULE:       authorized_registries_may_authorize_new_registries by_quorum_attestation
CHAIN_REQUIREMENT:    every_authorization_edge_must_be_replayable
FAILURE_MODE:         broken_chain_makes_downstream_claims_inadmissible
SELF_AUTHORIZATION:   prohibited
SCOPE_DEFAULT:        namespace_scoped_not_universal
```

### Charter I.2 — Authorization Chain Law

A registry R is authorized if and only if:

1. R's authorization chain descends from the epoch seed registry without break.
2. Every authorization edge E in the chain satisfies all four edge validity tests:
   - Quorum: the authorizing registry set met the quorum threshold at time of authorization.
   - Scope: R's namespace is a subset of the authorizing registries' combined namespace grants.
   - Timestamp: the authorization timestamp is within the valid window and does not precede the authorizing registries' own authorization timestamps.
   - Revocation: no registry in the chain was in REVOKED or SUSPENDED status at the time it performed the authorization act.
3. The authorization chain is itself published as an immutable record and is independently replayable.

If any edge in the authorization chain fails any of the four tests, R is unauthorized. All operator identities issued by R are inadmissible. All claims published by those operators are inadmissible.

This rule applies recursively.

### Charter I.3 — Self-Authorization Prohibition

No registry may authorize itself. No registry may be a member of the quorum that authorizes it. No registry may authorize a registry that, through any chain of delegations, would grant authority back to the original registry.

Circular authorization graphs are tainted by definition. Detection of a circular authorization graph triggers immediate TAINTED classification for all registries in the cycle and all downstream registries.

### Charter I.4 — Authorization Chain Replayability Requirement

Every authorization act must produce a replayable authorization record.

```json
{
  "authorization_record": {
    "record_type": "registry_authorization",
    "epoch": "ALMS-v1",
    "authorized_registry": "<registry_id>",
    "authorizing_set": ["<registry_id_1>", "<registry_id_2>"],
    "quorum_threshold": "<N of M>",
    "quorum_attestations": ["<signed_attestation_1>", "<signed_attestation_2>"],
    "namespace_grant": "<namespace_scope>",
    "timestamp_utc": "<unix_timestamp>",
    "authorization_hash": "<JCS_hash_of_this_record>",
    "parent_chain_hash": "<hash_of_authorizing_registries_chain_records>"
  }
}
```

The authorization_hash field is computed over the canonicalized record using JCS before the field is populated. It constitutes the edge identity in the authorization chain graph.

## Part II — Epoch Seed Registry

### Charter II.1 — Seed Registry Declaration

```text
SEED_REGISTRY_ID:         ALMS-v1-SEED-REGISTRY-0001
AUTHORIZED_BY:            ALMS-v1-EPOCH-0001
AUTHORIZATION_TYPE:       epoch_declaration
NAMESPACE:                * (universal, seed only)
CHAIN_DEPTH:              0
SELF_AUTHORIZATION:       n/a (epoch-declared, not peer-authorized)
STATUS:                   ACTIVE
```

The seed registry holds universal namespace for the sole purpose of authorizing the first generation of operational registries. It does not issue operator identities directly.

The seed registry may not be used to authorize operators.

### Charter II.2 — Seed Registry Constraints

- It may authorize operational registries but not operators.
- It may not be revoked by any peer registry, only by epoch succession.
- It may not expand its own namespace beyond universal seed scope.
- It may not authorize a registry with universal namespace.
- Its authorization record is the genesis record of the authorization chain and has no parent chain hash.

### Charter II.3 — First-Generation Authorization Quorum

```text
QUORUM_TYPE:       seed_declaration
QUORUM_THRESHOLD:  1 of 1
MINIMUM_SIGNERS:   1
```

### Charter II.4 — Standard Peer Quorum Requirements

```text
QUORUM_THRESHOLD:       ceil(2/3) of authorizing registry set
MINIMUM_AUTHORIZERS:    2
MAXIMUM_AUTHORIZERS:    no limit
ATTESTATION_FORMAT:     signed_authorization_record
TIMESTAMP_WINDOW:       all attestations must fall within 72 hours of each other
ATTESTATION_BINDING:    each attestation must commit to the full authorization record hash
```

## Part III — Namespace Scope

### Charter III.1 — Namespace Definition

```text
namespace      ::= domain ("/" subdomain)*
domain         ::= [a-z0-9] ([a-z0-9-]* [a-z0-9])?
subdomain      ::= [a-z0-9] ([a-z0-9-]* [a-z0-9])?
universal      ::= "*" (seed registry only)
```

### Charter III.2 — Namespace Inheritance Law

A registry may only grant namespaces that are subsets of its own namespace.

### Charter III.3 — Namespace Conflicts

Two registries hold a namespace conflict when their namespaces overlap and neither is a subset of the other. Namespace conflicts are reported to courts of competent jurisdiction as structural disputes.

### Charter III.4 — Namespace Expansion

Namespace expansion requires a new authorization record, quorum of the registry's authorizing set, and a namespace still within the authorizing set's combined grants.

### Charter III.5 — Universal Namespace Prohibition

No operational registry may hold universal namespace. Universal namespace is permanently reserved for the seed registry.

## Part IV — Operator Identity Lifecycle

### Charter IV.1 — Operator Registration

```json
{
  "operator_registration": {
    "operator_id": "<proposed_operator_id>",
    "registry_id": "<issuing_registry_id>",
    "identity_proof": "<cryptographic_identity_commitment>",
    "namespace": "<claimed_operating_namespace>",
    "claim_types": ["M", "I"],
    "timestamp_utc": "<unix_timestamp>",
    "registration_hash": "<JCS_hash_of_this_record>"
  }
}
```

### Charter IV.2 — Standing Record

```json
{
  "standing_record": {
    "operator_id": "<operator_id>",
    "registry_id": "<issuing_registry_id>",
    "status": "ACTIVE | SUSPENDED | REVOKED | EXPIRED",
    "namespace": "<authorized_namespace>",
    "claim_types": ["M", "I"],
    "valid_from": "<unix_timestamp>",
    "valid_until": "<unix_timestamp | null>",
    "status_reason": "<refusal_code | null>",
    "standing_hash": "<JCS_hash_of_this_record>",
    "previous_hash": "<hash_of_prior_standing_record | null>"
  }
}
```

Standing records form an immutable linked list per operator.

### Charter IV.3 — Status Transitions

```text
ACTIVE    -> SUSPENDED
ACTIVE    -> REVOKED
ACTIVE    -> EXPIRED
SUSPENDED -> ACTIVE
SUSPENDED -> REVOKED
EXPIRED   -> ACTIVE
REVOKED   -> none
```

### Charter IV.4 — Revocation Non-Retroactivity

Revocation of operator standing is prospective only. Claims published while an operator held ACTIVE status remain admissible regardless of subsequent revocation.

## Part V — Revocation Propagation

### Charter V.1 — Registry Revocation

A registry may be revoked by a quorum of its authorizing registries.

### Charter V.2 — Downstream Propagation Rule

New claims by operators issued by a revoked registry are held inadmissible until propagation review concludes.

Prior claims published before the revocation timestamp by operators with ACTIVE status at publication time retain admissibility.

Downstream registries authorized by the revoked registry are placed in SUSPENDED status.

### Charter V.3 — Downstream Standing Restoration

A downstream registry may petition for standing restoration by proving valid authorization at issuance, non-participation in the revoked conduct, and re-authorization from an alternate registry whose chain does not pass through the revoked registry.

### Charter V.4 — Suspension vs. Revocation Propagation Distinction

Suspension affects only new authorization acts. It does not trigger downstream propagation.

## Part VI — Refusal Codes

```text
REG-001 CHAIN_BROKEN
REG-002 QUORUM_NOT_MET
REG-003 SCOPE_EXCEEDED
REG-004 SELF_AUTHORIZATION
REG-005 CIRCULAR_CHAIN
REG-006 TIMESTAMP_VIOLATION
REG-007 IDENTITY_PROOF_INVALID
REG-008 NAMESPACE_CONFLICT
REG-009 REVOKED_AUTHORIZER
REG-010 SUSPENDED_AUTHORIZER
REG-011 UNIVERSAL_NAMESPACE_PROHIBITED
REG-012 SEED_REGISTRY_OPERATOR_ISSUANCE
REG-013 INVALID_STANDING_RECORD
REG-014 INVALID_AUTHORIZATION_RECORD
REG-015 DOWNSTREAM_PROPAGATION_PENDING
```

### Charter VI.2 — Refusal Code Binding

A refusal code, once issued against a registry act, is an immutable record. A successful appeal supersedes the refusal code for the specific act but does not expunge it.

## Part VII — Cross-Registry Treaty Hooks

### Charter VII.1 — Registry Treaty Mechanism

Authorized registries may enter into cross-registry treaties defining mutual recognition, shared revocation notifications, joint quorum pools, dispute escalation, and shared claim-type equivalence classes.

### Charter VII.2 — Treaty Scope Limits

A cross-registry treaty may not grant namespace authority not already held, override ALMS-v1-TREATIES.md, bypass quorum requirements, replace replay verification, or bind non-participating registries without explicit attestation.

### Charter VII.3 — Treaty Conflict Resolution

Where a cross-registry treaty conflicts with this Charter, this Charter governs. Where it conflicts with ALMS-v1-TREATIES.md, the Treaties govern.

## Part VIII — Deterministic Refusal Procedure

A registry must refuse an authorization, registration, or standing act when any enumerated refusal condition is detected. Refusal is mandatory, not discretionary.

### Charter VIII.2 — Refusal Record

```json
{
  "refusal_record": {
    "record_type": "registry_refusal",
    "epoch": "ALMS-v1",
    "registry_id": "<refusing_registry_id>",
    "refused_act": "<description_of_refused_act>",
    "refused_actor": "<operator_id_or_registry_id>",
    "refusal_codes": ["REG-NNN", "REG-NNN"],
    "evidence_hashes": ["<hash_of_supporting_evidence>"],
    "timestamp_utc": "<unix_timestamp>",
    "refusal_hash": "<JCS_hash_of_this_record>"
  }
}
```

## Appendix A — Authorization Chain Validity Algorithm

```text
function is_authorized(R, epoch_seed):
  chain = build_chain(R, epoch_seed)
  if chain is null:
    return UNAUTHORIZED, REG-001

  for each edge E in chain:
    quorum_result = check_quorum(E)
    if quorum_result != PASS:
      return UNAUTHORIZED, REG-002

    scope_result = check_scope(E)
    if scope_result != PASS:
      return UNAUTHORIZED, REG-003

    timestamp_result = check_timestamps(E)
    if timestamp_result != PASS:
      return UNAUTHORIZED, REG-006

    revocation_result = check_revocation_status(E.authorizing_set, E.timestamp)
    if revocation_result == REVOKED:
      return UNAUTHORIZED, REG-009
    if revocation_result == SUSPENDED:
      return UNAUTHORIZED, REG-010

  cycle_result = check_cycles(chain)
  if cycle_result != PASS:
    return UNAUTHORIZED, REG-005

  return AUTHORIZED
```

## Appendix B — Registry Invariants

```text
REG-INV-001  A registry is authorized iff its chain descends from the epoch seed without break and every edge satisfies quorum, scope, timestamp, and revocation checks.
REG-INV-002  No registry may authorize itself or participate in the quorum that authorizes it.
REG-INV-003  Authorization chains must be replayable. An unreplayable chain is equivalent to a broken chain.
REG-INV-004  Universal namespace is permanently reserved for the epoch seed registry.
REG-INV-005  Revocation of operator standing is prospective only. Prior admissible claims are permanently preserved.
REG-INV-006  Revocation of a registry propagates to downstream registries for future claims only. Prior admissible claims are permanently preserved.
REG-INV-007  Refusal is mandatory when a refusal condition is detected.
REG-INV-008  A refusal record is immutable. It may be superseded by a court ruling but not expunged.
REG-INV-009  Cross-registry treaties extend Charter and Treaty law. They may not override it.
REG-INV-010  The seed registry issues no operator identities.
```

End of ALMS-v1-REGISTRY-CHARTER.md
