# ALMS Citizen Relay System

## Status

AUDIT_LEDGER_MANIFEST_STORE_V1_DRAFT  
CITIZEN_REPLAY_RIGHT  
OPERATOR_PERMISSION_NOT_REQUIRED  
ALLEGATION_MODE_BLOCKED

## Purpose

The Audit Ledger Manifest Store (ALMS) turns machine-speed verification into civic infrastructure.

It ensures that materially consequential automated decisions publish a replayable manifest at the time of decision, persisted across independent stores, and retrievable without operator permission.

## Core Invariant

```txt
operator_permission_required_for_verification: false
```

The state may execute automated systems at machine speed only if citizens, auditors, journalists, counsel, and independent agents can verify at machine speed without asking the system operator.

## Section 1. Manifest Persistence

Immutability shall not depend on the agency or vendor that benefits from mutability.

Each covered automated output MUST publish its manifest to three independent stores at time of decision:

1. Agency operational system
2. National Archives or equivalent public records custodian
3. Public content-addressable network

Each manifest is content-addressed by SHA-256.

The manifest hash is the receipt.

Any manifest missing from one or more required stores enters `REVIEW_REQUIRED` status.

Any manifest with mismatched hashes across stores creates a presumption of invalidity.

## Section 2. Hourly Merkle Anchoring

Every hour, ALMS SHALL publish a Merkle root of all newly accepted manifests.

The hourly root SHALL be published to:

- Federal Register or equivalent public notice surface
- one judicial or court-adjacent timestamp authority
- one academic or independent research timestamp authority

A valid hourly anchor includes:

```json
{
  "type": "ALMS_HOURLY_MERKLE_ANCHOR",
  "window_start": "REPLACE_WITH_TIMESTAMP",
  "window_end": "REPLACE_WITH_TIMESTAMP",
  "manifest_count": 0,
  "merkle_root": "sha256:REPLACE_WITH_ROOT",
  "federal_register_ref": "REPLACE_WITH_REF",
  "judicial_timestamp_ref": "REPLACE_WITH_REF",
  "academic_timestamp_ref": "REPLACE_WITH_REF"
}
```

## Section 3. Manifest Schema

Minimum manifest shape:

```json
{
  "type": "ALMS_DECISION_REPLAY_MANIFEST",
  "manifest_version": "ALMS_V1",
  "decision_id": "REPLACE_WITH_DECISION_ID",
  "covered_system_id": "REPLACE_WITH_SYSTEM_ID",
  "agency_or_operator": "REPLACE_WITH_OPERATOR",
  "decision_timestamp": "REPLACE_WITH_TIMESTAMP",
  "decision_domain": "benefits|housing|employment|credit|eligibility|legal_recommendation|safety_critical|other",
  "model_identifier": "REPLACE_WITH_MODEL_ID",
  "policy_hash": "sha256:REPLACE_WITH_POLICY_HASH",
  "input_provenance_classification": "public|private|sealed|confidential|mixed",
  "transformation_chain_hash": "sha256:REPLACE_WITH_TRANSFORM_HASH",
  "output_receipt_hash": "sha256:REPLACE_WITH_OUTPUT_HASH",
  "replay_required": true,
  "operator_permission_required_for_verification": false,
  "append_only_audit": true,
  "human_review_required_on_failure": true,
  "allegation_mode": "blocked"
}
```

## Section 4. Reference Verifier Behavior

The ALMS verifier SHALL:

1. Fetch manifest by `decision_id` or manifest hash.
2. Retrieve all three store copies.
3. Compute SHA-256 over canonical manifest bytes.
4. Confirm all stores match the same hash.
5. Confirm the manifest hash appears in the correct hourly Merkle root.
6. Confirm the hourly root is anchored to required public timestamp surfaces.
7. Confirm replay path exists and does not require operator permission.
8. Emit a machine-readable verification result.

Verifier output:

```json
{
  "type": "ALMS_VERIFICATION_RESULT",
  "decision_id": "REPLACE_WITH_DECISION_ID",
  "manifest_hash": "sha256:REPLACE_WITH_HASH",
  "triple_write_valid": true,
  "merkle_anchor_valid": true,
  "operator_permission_required_for_verification": false,
  "replay_surface_present": true,
  "verification_status": "verified|review_required|suspended|invalid",
  "allegation_mode": "blocked"
}
```

## Section 5. Observer Independence

Observers are qualified by reproducible verification, not appointment.

Any person or institution that runs the open-source ALMS verifier and publishes replay results may act as an observer.

The official diversity pool SHOULD include at least five observers across at least three institutional types:

- press
- university lab
- civil society organization
- private auditor
- foreign academic partner
- public defender or legal aid entity

Observer independence is the property that verification still works even if no official observer is trusted.

## Section 6. Replay Failure Consequences

### Missing manifest, failed replay, or drift detected

The decision enters:

```txt
SUSPENDED
```

The system may not execute further automated actions on that case until review.

### Benefits, housing, employment, credit, or eligibility

Suspension triggers mandatory human review within 72 hours.

A rebuttable presumption favors the citizen.

The burden shifts to the agency or operator to reproduce valid replay.

### Punitive or adverse legal recommendation systems

Replay failure renders the output:

```txt
VOID_AB_INITIO
```

It may not be cited, scored, transferred, or used downstream.

### Safety-critical systems

Replay failure triggers fail-closed human operator mode and a public ALMS incident report within 24 hours.

## Section 7. Prohibited Substitutes

The following do not satisfy ALMS:

- dashboard screenshots
- vendor attestations without replay
- logs controlled only by the operator
- summaries without manifest hash
- black-box confidence scores
- API keys required for public verification
- trade-secret claims that eliminate replayability for covered outputs

## Section 8. Closing Doctrine

```txt
NO MANIFEST, NO AUTHORITY.
NO REPLAY, NO AUTOMATED POWER.
NO OPERATOR PERMISSION, NO BLACK BOX.
```

ALMS exists so executive automation leaves a byte-by-byte receipt that any citizen or independent agent can inspect.
