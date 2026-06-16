# AL_REPLAY_MODULE_V1

## STATUS
INITIALIZING

## PURPOSE
Bridge the static `FEDERAL_AI_TESTING_ROOT_LANE_V1` evidence docket into the dynamic ALMS replay runtime without converting narrative claims into authority.

This module treats the federal AI root receipt as the initial replay target for an Audit Lineage Management System (ALMS) lane. It does not claim that an EAS attestation has been created. It only defines how a committed docket, verifier, receipt, and future attestation packet are replayed.

## GENESIS RECEIPT

```text
0xbabd724ec57a5eda9268596d3be7a437f7d5e6bb0a9ae9e4a6e6b699798e03f0
```

## CURRENT ANCHOR STATE

```yaml
docket_id: FEDERAL_AI_TESTING_ROOT_LANE_V1
schema_uid: 0x70e30c2294cc91f178886ef547db67bd3b3a6575af971328d42a8d5e2ad1fb88
schema_tx: 0x2f02d4a4a3fd1687a9dcf5ee6999f6a01e802842378d64b466c1733160bde628
attestation_uid: null
anchor_state: YELLOW_READY
no_fake_green: true
```

## 1. REPLAY_INVARIANT

Any system state derived from this module MUST be replayable from the raw docket entries `FED-AI-001` through `FED-AI-006` using:

```text
scripts/verify_federal_ai_root_lane.py
```

A replay result is valid only if it can reconstruct the docket hash, verifier hash, receipt hash, and attestation packet fields from committed bytes.

## 2. EXECUTION_GATES

### GATE_01 — Receipt Binding
The replay module MUST verify the receipt object against the ALMS registry or committed receipt path.

Failure state:

```text
RECEIPT_BINDING_MISSING
```

### GATE_02 — NO_FAKE_GREEN Enforcement
The replay module MUST confirm:

```text
no_fake_green == true
```

Failure state:

```text
NO_FAKE_GREEN_BREACH
```

### GATE_03 — CRO Requirement
Any execution payload lacking a valid JSON Canonical Receipt Object (CRO) MUST be rejected.

Failure state:

```text
MISSING_CANONICAL_RECEIPT_OBJECT
```

### GATE_04 — Attestation Boundary
The replay module MUST NOT mark the lane `GREEN_ANCHORED` unless an EAS attestation UID exists and is bound to the registered schema UID.

Failure state:

```text
FAKE_ANCHOR_GREEN_DETECTED
```

## 3. EVIDENCE_BINDING

The AL runtime is restricted to the committed federal AI root docket bytes. Any variance in document content, verifier content, or receipt content MUST trigger a replay halt.

Failure state:

```text
AUTHENTICITY_BREACH
```

## 4. GENESIS EVENT MODEL

```yaml
genesis_event:
  event_type: FEDERAL_AI_ROOT_RECEIPT_INGESTED
  docket_id: FEDERAL_AI_TESTING_ROOT_LANE_V1
  verifier: scripts/verify_federal_ai_root_lane.py
  receipt: fed_ai_root_receipt
  anchor_state: YELLOW_READY
  attestation_required_for_green: true
```

## 5. REPLAY WITNESS CONTRACT STUB

A future `Replay_Witness_Contract` MAY observe updates to the federal AI root lane, but it MUST enforce these boundaries:

```yaml
witness_contract:
  may_observe:
    - docket_hash
    - verifier_hash
    - receipt_hash
    - attestation_packet
    - eas_schema_uid
    - eas_attestation_uid
  may_not_assert:
    - attestation_created_without_uid
    - primary_source_verified_without_receipt
    - green_anchor_without_onchain_uid
    - narrative_claim_as_authority
```

## 6. STATE TRANSITIONS

```yaml
states:
  YELLOW_READY:
    meaning: schema exists and packet may be prepared, but attestation UID is missing
    allowed_next:
      - GREEN_ANCHORED
      - YELLOW_PACKET_REFRESHED
      - RED_AUTHENTICITY_BREACH
  GREEN_ANCHORED:
    required:
      - eas_schema_uid
      - eas_attestation_uid
      - docket_sha256
      - verifier_sha256
      - receipt_sha256
      - receipt_uri
      - no_fake_green: true
  RED_AUTHENTICITY_BREACH:
    trigger:
      - hash_mismatch
      - missing_receipt
      - false_green_attempt
```

## 7. CANONICAL RULE

```text
No docket state may enter ALMS runtime authority unless it is replayable from committed bytes and bounded by an explicit receipt.
```

## 8. ENCODED LESSON

```text
Proof over narrative means the replay path must survive the operator session.
```
