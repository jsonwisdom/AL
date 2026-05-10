# Wiring Diagram — Family Approved Receipts Machine

**Audit Branch:** `root-law-machine-audit-v1`  
**Constitutional Version:** 1.0.0  
**Last Updated:** 2026-05-09

---

## Data Flow

```text
[Learning Lab / Witness Stream UI] -> [IndexedDB Receipt Log]
                                     ↓
                         [Agent Oracle V2 — 5 Bees]
                                     ↓
                         [Human Accept / Challenge]
                                     ↓
                         [MigrationGuard.submitMigration()]
                                     ↓
              ┌──────────────────────┴──────────────────────┐
              ↓                                             ↓
[PASS] -> Event: MigrationReceiptWritten     [FAIL] -> Event: MigrationFailClosed
              ↓                                             ↓
      [EAS Attestation]                 [ReputationOracle.ingestFailClosed()]
```

---

## Component Responsibilities

| Component | Responsibility | Constitutional Rule |
|-----------|----------------|---------------------|
| **Learning Lab** | Capture witness observations | Receipt-first |
| **Witness Stream UI** | Human input surface | No silent authority |
| **IndexedDB Receipt Log** | Local-first immutable store | Replayable memory |
| **Agent Oracle V2 (5 Bees)** | Coordinate, route, plan, link receipts | Cannot define truth |
| **Human Accept / Challenge** | Settlement gate | Human before settlement |
| **MigrationGuard** | Pre-storage integrity guard | No confidence upgrade |
| **ReputationOracle** | Slashable fault ingestion | Neutral start + repair path |
| **EAS Attestation** | On-chain receipt anchor | Constitutional root bound |

---

## Environment Variables (Testnet)

```env
VITE_CONSTITUTIONAL_ROOT_UID=0x3c220510fd03e3daf8e19abc02eafb58e6991d2d
VITE_MIGRATION_GUARD_ADDRESS=0x0000000000000000000000000000000000000000
VITE_REPUTATION_ORACLE_ADDRESS=0x0000000000000000000000000000000000000000
VITE_EAS_ADDRESS=0x4200000000000000000000000000000000000021
VITE_CHAIN_ID=84532
```

Note: Guard and oracle addresses are placeholders until testnet deployment receipts exist.

---

## Prohibited Flows (Constitutional Block)

| Flow | Why Blocked |
| --- | --- |
| Tokenization | No economic weighting of truth |
| Trust scores | No permanent authority labels |
| Silent confidence upgrade | Target cannot exceed source |
| Autonomous settlement | Human before settlement |
| Leaderboards | No engagement scoring |

---

## Required Flows (Constitutional Mandate)

| Flow | Requirement |
| --- | --- |
| Receipt before synthesis | Every output emits a receipt |
| Replay before authority | Verification requires replay |
| Human accept/challenge | Settlement requires human gate |
| Degradation log | Every change logged, even empty |

---

## Repair Path (Correction Doctrine)

1. Relayer submits failure -> `MigrationFailClosed` event
2. Oracle records violation as a receipt-bound event
3. Relayer submits repair proof -> `submitRepair()`
4. Relayer submits replay proof -> required before verification
5. Audit committee verifies -> `verifyRepair()`
6. Relayer reactivated only after replay-verified repair, unless concealment is confirmed

Promotion remains a protocol attack. It cannot be repaired by payment.

---

## Bound Projects Status

| Project | Status | Wiring Verified |
| --- | --- | --- |
| Cross-Chain Migration Guard | Audited | Yes |
| Agent Oracle V2 (Spec) | Locked | Yes |
| Witness Stream UI | To build | Pending |
| IndexedDB Receipt Log | To build | Pending |
| Replay Verifier | To build | Pending |

---

## The Invariant

```text
Confidence may be preserved. Confidence may not be manufactured.
No output without a receipt. No synthesis without replay. No settlement without human acceptance.
```

---

This wiring diagram is the authoritative reference for all constitutional integrations.
Changes require audit review and a new commit on `root-law-machine-audit-v1`.
