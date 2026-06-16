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
