# RISKS.md — jaywisdom.base.eth Receipt Machine

## System Status

This repository treats jaywisdom.base.eth as a public identity root, receipt catalog, and onchain store staging layer.

Current anchor rule:

- Git first
- SHA256 second
- IPFS third
- EAS/Base witness fourth

No artifact is considered ANCHORED unless the receipt contains a real git commit, SHA256 hash, IPFS CID, EAS UID, and Base transaction hash.

## Verification Decay Risks

### 1. Ghost Anchoring

Risk: A file is described as anchored before there is a real tx hash, EAS UID, CID, or verifier output.

Control: Use PENDING until evidence exists.

### 2. IPFS Availability Decay

Risk: A CID exists, but no active pin/provider keeps the content reachable.

Control: Record CID as archive proof, not availability proof. Use multiple pins when possible.

### 3. Manifest Drift

Risk: MANIFEST.sha256 no longer matches the file contents.

Control: Re-run sha256sum before every status transition.

### 4. EAS Misbinding

Risk: An attestation references the wrong CID, wrong hash, wrong operator, or wrong repo state.

Control: EAS payload must include receipt_id, sha256, git_commit, operator, and claim.

### 5. ENS Overclaim

Risk: jaywisdom.base.eth is presented as fully configured before visible text-record evidence exists.

Control: ENS is identity convenience unless text-record proof is visible.

### 6. Private/Public Boundary Leak

Risk: Private family, wallet, financial, or personal data enters the public all-onchain store.

Control: Public receipts must be reviewed before archival. No private assets enter public receipts by default.

## Canon Rule

Receipt first.  
Anchor second.  
Profit third.
