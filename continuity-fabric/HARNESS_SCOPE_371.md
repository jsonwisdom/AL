# Continuity Fabric Harness Scope — Issue #371

Status: implementation branch scaffold.

This branch implements the test harness required by Issue #371 and blocks release Issue #372 until green.

## Branch

`implement-continuity-fabric-harness-371`

## Scope

Minimum scope only:

```text
schemas/
  WALEntry.v1.json
  QuorumReceipt.v1.json
  SettlementRecord.v1.json
  PolicyDecisionLog.v1.json
  AlertEvent.v1.json
  ConfigUpdate.v1.json

test/harness/
  valid_policy_reload.spec.ts
  unknown_issuer.spec.ts
  emergency_kill_switch.spec.ts
```

## Required Fixture Chain

```text
ConfigUpdate -> WALEntry -> QuorumReceipt[] -> SettlementRecord -> PolicyDecisionLog -> AlertEvent -> ActivationRecord
```

## Merge Gate

- All 3 harness vectors pass.
- Schemas validate against vectors.
- Coverage target: 95% for P1, P2, P3, P4, PolicyEngine, Alerting.
- No `REVERT` in types.
- No unsigned decisions.
- No fake green paths.

## Forbidden In This Branch

- No `git tag`.
- No release notes.
- No deploy code.
- No main branch deployment.
- No code touching user funds.

## Doctrine

Law exists in Issues #371 and #372. This branch is enforcement only.

No silent mutation.  
No fake green.  
No unaudited policy.  
No replay without quorum.  
No global halt from one poisoned actor.
