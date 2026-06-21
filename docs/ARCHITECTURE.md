# jaywisdom.base.eth Receipt Machine Architecture

## Purpose

jaywisdom.base.eth is the public identity root for Jay Wisdom's onchain store, receipt catalog, and verification system.

This repository is the constitutional staging layer. It prepares claims locally before any public witness is created.

## Verification Order

1. Git commit
2. SHA256 manifest
3. IPFS CID
4. EAS attestation on Base
5. Final receipt update

No artifact is ANCHORED until all required witness fields are real and recorded.

## Core Directories

| Directory | Purpose |
|---|---|
| receipts/ | Root receipts and forensic proof objects |
| schemas/ | EAS and verification schemas |
| attestations/ | Draft and finalized witness payloads |
| docs/ | Human-readable architecture and replay guide |
| ledger/ | Public operational accounting, when added |
| hooks/ | Zora/Base economic logic, when added |
| store/ | Public sellable artifacts, when added |

## Current Root Receipt

Receipt: IDENTITY_ROOT_RECEIPT_001

Claim: jaywisdom.base.eth is the public identity root for Jay Wisdom's onchain store and verification catalog.

Current status: LOCAL_CANON_PENDING_ANCHOR

## Canon

Receipt first.  
Anchor second.  
Profit third.

---

# Inside-Out Zero-Trust Verification System (ZTVS)

## The Canonical System Rules

1. **Official source is origin, not authority.**
2. **Replay loop is proof, not presentation.**
3. **Public explorer is access, not validation.**
4. **REVIEW RECEIPT = only bridge from drift back to green.**

## Canonical Patch Rule

> **No Fake Green means a clean state must actively prove why it became clean.**

## State Transition Integrity

To transition the ledger from a state of structural anomaly back to a clean state, the pipeline must ingest and record an explicit human-in-the-loop review signature.

```text
┌─────────────────┐
│ DRIFT_DETECTED  │
└────────┬────────┘
         │
         │  [ Signed Review Receipt Needed ]
         ▼
┌─────────────────┐
│ REVIEW_PENDING  │
└────────┬────────┘
         │
         │  [ Map Receipt SHA-256 ]
         ▼
┌─────────────────┐
│    VERIFIED     │
└─────────────────┘
```

* **Direct Bypass Prohibited:** `DRIFT_DETECTED` → `VERIFIED` transitions trigger an immediate build failure unless the generating Evidence Card records a non-null `review_receipt_hash`.
* **State Drift Permanence:** If an active change occurs in the origin document, the local verification node locks down. A stale or detached file inside the workspace will not satisfy the condition; the hash of the active review receipt is permanently woven into the chronological record of the evidence artifact.

## Final Verification Topology

```ini
OFFICIAL        = Origin Ingestion Base
GITHUB_LOOP     = Automated Proof Preservation Engine
PUBLIC_EXPLORER = Frictionless Evidence Access Layer
REVIEW_RECEIPT  = Cryptographic Bridge from Drift back to Green State
```

The loop is closed. The pipeline is hardened against passive bypass via stale workspace files.
