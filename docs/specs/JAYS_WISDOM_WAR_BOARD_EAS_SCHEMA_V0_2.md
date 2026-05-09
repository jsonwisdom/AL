# Jay’s Wisdom War Board — EAS Schema v0.2

**Spec ID:** `JAYS_WISDOM_WAR_BOARD_EAS_SCHEMA_V0_2`  
**War Board ID:** `JAYS_WISDOM_WAR_BOARD_V0_2`  
**Spec Path:** `docs/specs/JAYS_WISDOM_WAR_BOARD_V0_2.md`  
**Identity:** `jaywisdom.base.eth`  
**Mode:** Minimal receipts-first EAS witness schema  
**Status:** REGISTRATION_CANDIDATE — NOT YET ONCHAIN REGISTERED

## Purpose

This schema witnesses the War Board public record without pretending to store the full dashboard state onchain.

GitHub is replay.
EAS is witness.
ENS is discovery.

## Proposed EAS Schema

```text
string projectId,string specId,string repoUrl,string commitHash,string specPath,bytes32 specHash,string statusJson
```

## Field Semantics

| Field | Meaning |
|---|---|
| `projectId` | Stable project identifier, e.g. `MEME_METAVERSE_WAR_BOARD` |
| `specId` | `JAYS_WISDOM_WAR_BOARD_V0_2` |
| `repoUrl` | Public GitHub URL for the repo or spec |
| `commitHash` | Git commit anchoring the spec state |
| `specPath` | Repo path to the canonical spec file |
| `specHash` | bytes32 hash of the canonical spec bytes |
| `statusJson` | Compact JSON status payload including status taxonomy |

## Required Status Taxonomy

```json
{
  "CANDIDATE": "submitted but not reviewed",
  "LOCAL_ATTESTED": "supported by local source",
  "MULTI_TERRITORY": "same seam appears in multiple places",
  "ORIGIN_DISPUTED": "origin claim contested",
  "JOINT_ORIGIN": "synchronous independent emergence inside temporal window with no causal link shown",
  "USAGE_SHARED": "phrase is valid in multiple territories",
  "CORRECTED": "prior claim updated",
  "REVOKED": "claim withdrawn but visible"
}
```

## JOINT_ORIGIN Rule

`JOINT_ORIGIN` is valid only when the collision inspector records:

```json
{
  "temporal_window_check": "PASS",
  "independence_proof": "PASS",
  "local_context_preservation": "PASS"
}
```

## Registration Rule

Registration must be performed with browser wallet signing only.

Terminal scripts may generate payloads or verify chain state, but must not handle private keys.

## Non-Claims

This document does not claim that the schema is already registered onchain.

A schema UID becomes canonical only after direct Base mainnet verification succeeds.
