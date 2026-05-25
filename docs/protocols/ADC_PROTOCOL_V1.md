---
schemaVersion: adc_protocol_v1
protocolId: ADC_PROTOCOL_V1
title: Automatic Drift Correction Protocol V1
repositoryOfRecord: jsonwisdom/AL
methodologyChamber: true
externalEvidenceChamber: jsonwisdom/base
baselineReceipt: TRACK_WATCHDOG_02_DAY0_SWEEP
baselineCommit: 2eb95aa4042826cf10c4148cf20df61a3e6d4072
postMergeFinalizationCommit: 2fa4060e5002b2e66830eef4ee714226f3771737
mergeCommitSha: dde076ff55aed22c5428c1ee5e7baa435a08e288
previousMasterRoot: daea0d74e2cea96f211cc5a9434f01099e435448f4da625d0eabdc8c3f1fe16f
currentMasterRoot: 1f17fd0a61c43e411d3792335a935cc1517267f9caf443d6c594efc95610c3b7
rootStatus: ROOT_SEALED
classification: METHODOLOGY_REFINEMENT
mode: APPEND_ONLY_REPAIR_GEOMETRY
canonicalInvariants:
  - REPAIR_APPENDS
  - REPAIR_NEVER_REWRITES
  - DRIFT_MUST_BE_RECEIPT_BEARING
  - NO_SILENT_CORRECTION
  - NO_HISTORY_REWRITE
  - HUMAN_READABLE_AFTER_REPLAY
status: ACTIVE_DRAFT_FOR_DAY7_SWEEP
---

# ADC_PROTOCOL_V1 — Automatic Drift Correction Protocol

## 1. Purpose

ADC_PROTOCOL_V1 defines the lawful response geometry for drift detected by watchdog sweeps.

It does not auto-mutate source history. It does not rewrite receipts. It does not erase prior state.

It converts drift into a bounded, receipt-bearing repair path.

Core invariant:

```txt
REPAIR_APPENDS
REPAIR_NEVER_REWRITES
```

---

## 2. Scope

ADC applies after a watchdog sweep returns any verdict other than `CLEAN`.

Valid input verdicts:

```txt
DRIFT_DETECTED
INDETERMINATE
TAINTED
MISSING_WITNESS
```

ADC does not run on `CLEAN` except to record no-op readiness.

---

## 3. Drift Classification

```txt
CLASS_0_OBSERVATION_ONLY
  Non-mutating discrepancy. Requires note, no repair.

CLASS_1_DOCUMENTATION_DRIFT
  Receipt/docs mismatch. Requires append-only correction receipt.

CLASS_2_LINEAGE_DRIFT
  Commit, branch, root, or receipt lineage mismatch. Requires halt and reconciliation receipt.

CLASS_3_CROSS_LAYER_CONTAMINATION
  Evidence leaks into methodology or methodology mutates evidence. Requires fork-or-quarantine decision.

CLASS_4_AUTHORITY_ESCALATION
  Unsupported official/on-chain/ENS/IPFS/mainnet claim. Requires immediate boundary receipt and public correction.
```

---

## 4. Evidence Admissibility

Admissible evidence:

```txt
Git commit SHA
Git blob SHA
Git tree SHA
Pull request metadata
Changed-file list
Canonical root payload
Receipt file contents
Verified operator-provided hash
```

Inadmissible evidence:

```txt
Memory-only claim
Placeholder hash
Uncommitted local file
Screenshot without repo confirmation
ENS/IPFS/on-chain assertion without receipt
Speculation about protocol intent
```

---

## 5. Required ADC Receipt Fields

Every correction must create a new receipt with:

```json
{
  "adc_receipt_id": "ADC_RECEIPT_<N>",
  "triggering_watchdog_track": "TRACK_WATCHDOG_<N>",
  "drift_class": "CLASS_<N>",
  "observed_fault": "string",
  "admissible_evidence": [],
  "forbidden_action_avoided": [],
  "repair_action": "APPEND_ONLY_RECEIPT",
  "source_rewrite": false,
  "history_rewrite": false,
  "new_root_required": true,
  "status": "PENDING_RESEAL"
}
```

---

## 6. Repair Procedure

```txt
1. HALT_EXPANSION
2. CLASSIFY_DRIFT
3. COLLECT_ADMISSIBLE_EVIDENCE
4. WRITE_ADC_RECEIPT
5. APPEND_CORRECTION_ONLY
6. RECOMPUTE_MASTER_ROOT
7. SEAL_NEW_ROOT
8. RESUME_ONLY_AFTER_ROOT_SEALED
```

No step may be skipped.

---

## 7. Forbidden Repair Actions

```txt
DELETE_PRIOR_RECEIPT
REWRITE_HISTORY
FORCE_PUSH_OVER_CANON
SILENTLY_EDIT_EVIDENCE
RETROACTIVE_OFFICIAL_CLAIM
PLACEHOLDER_ROOT_FINALIZATION
MERGE_BEFORE_RESEAL
EXPAND_SCOPE_DURING_DRIFT
```

---

## 8. Re-Seal Rule

Any ADC correction that changes repository-visible state requires a new root transition.

```txt
previousMasterRoot = current sealed root
newMasterRoot = SHA256(canonical ADC payload)
```

The correction is not complete until `ROOT_SEALED` is recorded.

---

## 9. Day 7 Integration

TRACK_WATCHDOG_02 Day 7 sweep must call ADC when the verdict is not `CLEAN`.

```txt
IF verdict == CLEAN:
  record watchdog receipt only

IF verdict != CLEAN:
  invoke ADC_PROTOCOL_V1
  halt merge/scope expansion
  append ADC receipt
  reseal root before resuming
```

---

## 10. Final State

```json
{
  "protocol_id": "ADC_PROTOCOL_V1",
  "repository_of_record": "jsonwisdom/AL",
  "current_master_root": "1f17fd0a61c43e411d3792335a935cc1517267f9caf443d6c594efc95610c3b7",
  "mode": "APPEND_ONLY_REPAIR_GEOMETRY",
  "repair_appends": true,
  "repair_never_rewrites": true,
  "status": "ACTIVE_DRAFT_FOR_DAY7_SWEEP"
}
```

Proof over narrative. Repair appends. Repair never rewrites. ⚙️🧾
