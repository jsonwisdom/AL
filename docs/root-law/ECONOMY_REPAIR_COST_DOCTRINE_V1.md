# Economy Repair Cost Doctrine v1

Status: DRAFT_ROOT_LAW_EXTENSION
Root identity: jaywisdom.base
Applies to: relayer repair, correction receipts, economic penalties, role restoration, donor-funded infrastructure, and worker bee operations.

## Verdict

Repair should require Proof of Repair, not pure Proof of Work or pure Proof of Stake.

Effort alone can be performative.
Stake alone can be plutocratic.
Verified repair must be replayable.

## Core Rule

```text
The cost of repair is the cost of making the system safer and the record clearer.
```

## Repair Cost Model

Use three layers:

```text
1. PROOF_OF_REPAIR
   mandatory
   evidence that the failure was understood and corrected

2. PROOF_OF_REPLAY
   mandatory
   independent verification that the repaired path now passes

3. REFUNDABLE_STAKE_OR_BOND
   optional
   used only when the failure creates external review, compute, or operational cost
```

## Why Not Pure Proof of Work

Proof of Work can show effort, but effort does not prove correction.

A relayer could spend time, generate logs, or perform busywork without fixing the underlying violation.

## Why Not Pure Proof of Stake

Proof of Stake can show financial seriousness, but money must not buy trust.

A rich actor should not be able to purchase rapid rehabilitation while a smaller contributor is excluded from repair.

## Required Repair Receipt

A valid RepairReceipt should include:

```json
{
  "type": "RepairReceipt",
  "root_identity": "jaywisdom.base",
  "source_witness_hash": "bytes32",
  "reject_code": "bytes32",
  "relayer": "address",
  "failure_receipt_hash": "bytes32",
  "root_cause_hash": "bytes32",
  "patch_hash": "bytes32",
  "replay_result_hash": "bytes32",
  "reviewer_receipt_hash": "bytes32",
  "stake_bond_hash": "bytes32_or_zero",
  "repair_state": "REPAIR_SUBMITTED",
  "challenge_window_ends_at": "timestamp"
}
```

## Repair States

```text
REPAIR_SUBMITTED
- relayer admits or addresses the issue
- neutral pending review

REPAIR_REPLAYED
- repaired path passes deterministic replay
- positive transparency signal may begin

REPAIR_CHALLENGED
- unresolved
- no restoration until settlement

REPAIR_VERIFIED
- role capability may be restored
- reputation update remains receipt-bound

REPAIR_REJECTED
- role cooldown continues
- rejection must include a reason receipt

CONCEALMENT_CONFIRMED
- escalation
- repair grace does not apply until concealment is separately settled
```

## Economic Rules

Allowed:

- refundable bond for review/compute costs
- fee escrow for third-party auditors
- capped challenge bond to prevent spam
- reward for verified repair work
- donor-funded subsidies for legitimate small contributors

Forbidden:

- buying confidence
- buying role restoration without replay
- permanent economic caste
- donor override of settlement
- hidden reputation scoring
- punishment for honest correction alone

## Role Restoration Rule

```text
No role restoration without Proof of Replay.
No economic payment can replace Proof of Replay.
```

## Cost Assignment

| Situation | Cost Type | Reason |
| --- | --- | --- |
| honest first correction | no penalty; only repair evidence | becoming is protected |
| integrity mismatch repeated | repair receipt + replay proof | process reliability must improve |
| external reviewer needed | refundable review bond | covers real audit cost |
| frivolous challenge | challenge bond may be forfeited | protects commons bandwidth |
| confirmed concealment | escalation receipt + longer cooldown | deception attacks the commons |
| promotion attempt | no economic shortcut | confidence inflation is protocol attack |

## Worker Bee Boundary

AI employees may:

- prepare repair diffs
- compute replay reports
- estimate external review costs
- draft RepairReceipts
- surface unresolved repair challenges

AI employees may not:

- sell restoration
- accept payment as proof
- settle repair without replay
- hide failed replays
- convert repair history into a global identity score

## Donor Boundary

Donors may fund repair infrastructure, reviewers, compute, education, and accessibility.

Donors may not purchase truth, erase challenge windows, or override replay results.

## Constitutional Line

```text
Work shows effort.
Stake shows exposure.
Replay shows repair.
```

## Audit Verdict

ECONOMY_REPAIR_COST_DOCTRINE_V1_APPLIED

Repair is not a tax.
Repair is not a bribe.
Repair is a replayable restoration path.
