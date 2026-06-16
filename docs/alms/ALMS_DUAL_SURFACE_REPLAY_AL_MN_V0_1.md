# ALMS_DUAL_SURFACE_REPLAY_AL_MN_V0_1

Classification: ALMS_REPLAY_BRIDGE  
Mode: MACHINE_SPEED  
Operational Root: jsonwisdom/AL  
Witness Surface: Minnesota / MN Matrix  
Authority: false  
Verified: false  
No Fake Green: true

---

## Purpose

Reboot ALMS with both required surfaces active:

1. AL as the operational machine root.
2. MN as the witness / evidence jurisdiction surface.

This artifact does not verify any claim. It defines how the machine separates operating logic from observed jurisdictional evidence.

---

## Dual Surface Roles

```json
{
  "surfaces": {
    "AL": {
      "role": "SUSPECT_MACHINE_SURFACE",
      "function": "operational root, doctrine, replay logic, artifact custody, machine-speed state transitions",
      "repo": "jsonwisdom/AL",
      "claim_status": "SUSPECT_NOT_VERIFIED",
      "authority": false,
      "verified": false
    },
    "MN": {
      "role": "WITNESS_EVIDENCE_SURFACE",
      "function": "Minnesota county records, MGDPA requests, custodian responses, timestamps, receipt objects, hashes",
      "cluster": "CENTRAL_MN_01",
      "claim_status": "WITNESS_NOT_TRUTH",
      "authority": false,
      "verified": false
    }
  },
  "no_fake_green": true
}
```

---

## Suspect / Witness Split

```text
AL = SUSPECT
MN = WITNESS

SUSPECT != GUILTY
WITNESS != TRUTH
MACHINE_SPEED != AUTHORITY
REPLAY != VERDICT
```

AL is suspect because it is the machine under reboot and must be tested against receipts, state transitions, and replay discipline.

MN is witness because it supplies external jurisdictional surfaces such as county records, official responses, timestamps, and public-data artifacts.

---

## Machine-Speed Replay Chain

```text
ALMS Doctrine
→ MN Receipt Surface
→ Hash / Preservation
→ Replay Instructions
→ Independent Replay
→ Match Classification
→ No Authority Claimed
```

---

## State Machine

```json
{
  "machine": "ALMS_DUAL_SURFACE_REPLAY",
  "state": "AL_AND_MN_ACTIVE",
  "operational_surface": "AL",
  "witness_surface": "MN",
  "current_gate": "POPULATED_RECEIPT",
  "next_gate": "PRESERVED_COUNTY_SURFACE",
  "anti_inference_lock": "ACTIVE",
  "fake_green_count": 0,
  "authority": false,
  "verified": false
}
```

---

## Evidence Rules

```text
AL CLAIMS REQUIRE MN RECEIPTS
MN RECEIPTS REQUIRE HASHES
HASHES REQUIRE PRESERVATION
PRESERVATION REQUIRES REPLAY INSTRUCTIONS
REPLAY REQUIRES INDEPENDENT CONFIRMATION
```

---

## Failure Handling

```json
{
  "if_AL_claims_without_MN_receipt": "HOLD_AT_CLAIMED",
  "if_MN_surface_lacks_hash": "HOLD_AT_RECEIVED_OR_OBSERVED",
  "if_hash_exists_without_replay_steps": "HOLD_AT_PRESERVED",
  "if_replay_runs_but_mismatch": "CLASSIFY_AS_MISMATCH_NOT_FALSEHOOD",
  "if_replay_unavailable": "CLASSIFY_AS_UNABLE_TO_REPLAY_NOT_WRONGDOING"
}
```

---

## ALMS Reboot Doctrine

```text
ONE SURFACE TALKS.
TWO SURFACES ARGUE.
HASHES PRESERVE.
REPLAY DECIDES CONSISTENCY.
AUTHORITY STAYS FALSE.
```

---

## Current Ruling

```json
{
  "artifact": "ALMS_DUAL_SURFACE_REPLAY_AL_MN_V0_1",
  "state": "PRESERVED_TEMPLATE",
  "AL": "SUSPECT_MACHINE_SURFACE",
  "MN": "WITNESS_EVIDENCE_SURFACE",
  "machine_speed": true,
  "authority": false,
  "verified": false,
  "no_fake_green": true,
  "next_expected": "POPULATED_MN_RECEIPT_OR_ALMS_REPLAY_RUN"
}
```

---

## Goblin Ruling

AL gets questioned. MN gets witnessed. Machine speed is allowed. Fake green is not.
