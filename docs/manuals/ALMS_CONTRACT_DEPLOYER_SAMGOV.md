# ALMS Contract Deployer — SAM.gov Integration

## Purpose

This module extends ALMS into a **contract deployment registry** that links:

- GitHub source (proof)
- Base contract deployment (anchor)
- External identity systems (SAM.gov)

## Core Principle

A contract is not recognized unless:

1. Deployment tx hash exists
2. Contract address is confirmed
3. Source hash is linked

## SAM.gov Layer

Domain: `sam.gov`

Fields:
- `externalId` = SAM.gov Entity ID
- `domain` = "sam.gov"

This allows mapping:

```json
{
  "entity": "SAM.gov",
  "entity_id": "...",
  "contract_address": "0x...",
  "chain": "base"
}
```

## Flow

1. GitHub commit → sourceHash
2. Base deploy → tx_hash + contract_address
3. Call `registerDeployment()`
4. Store SAM.gov identity reference

## ALMS Rule

- No registration without contract_address
- txKey = keccak(tx_hash)
- ENS remains pointer layer

## Status

PRE-DEPLOYMENT — waiting for real contract address confirmation
