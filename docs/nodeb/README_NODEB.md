# Node B — Base Anchor Module (ALMS)

This module introduces the **Node B Sovereign Uptime Anchor** into AL.

## Components
- `contracts/nodeb/NodeBUptime.sol` → On-chain attestation contract
- (external) `nodeb_collector.py` → L0 telemetry
- (external) `l2_settler.py` → L2 settlement

## ALMS Rules
- No private keys in repo
- No claims without tx_hash
- Merkle root must be 32 bytes
- Monthly settlement only

## State
READY_FOR_DEPLOYMENT (pending real tx)
