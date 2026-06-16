# Merkle-Rooted State-Level ALMS — 51 States

Status: DRAFT_CANON
Operator: Jay Wisdom
Identity: jaywisdom.eth / jaywisdom.base / jaywisdom.base.eth
Lead lane: Alabama
Activation lane: 67ACTNOWAL

## Core thesis

Apply ALMS as a state-level civic verification layer across all 50 states plus DC.

Each state runs as a local proof lane with its own receipts, local vernacular, public claim intake, and Merkle-rooted state ledger.

Alabama takes the lead on speed.

---

## System model

```json
{
  "system": "Merkle-Rooted State-Level ALMS",
  "scope": "50 states + DC",
  "state_count": 51,
  "lead_state": "Alabama",
  "lead_lane": "67ACTNOWAL",
  "verification_layer": "ALMS",
  "root_rule": "state_root -> national_root",
  "principle": "local claims, local receipts, global verifiability"
}
```

---

## Root hierarchy

```text
Local Claim Receipt
  -> District / County Root
  -> State Root
  -> National 51-State Root
  -> Optional Base / ENS Anchor
```

Machine-readable form:

```json
{
  "root_hierarchy": [
    "claim_receipt",
    "local_root",
    "state_root",
    "national_51_state_root",
    "base_or_ens_anchor"
  ]
}
```

---

## State lane object

Each state lane must expose:

```json
{
  "state_code": "AL",
  "state_name": "Alabama",
  "lane_id": "67ACTNOWAL",
  "status": "DRAFT | ACTIVE | REPLAY_REQUIRED | REPLAY_PASSED | BLOCKED",
  "state_root": "sha256:<64-hex> | UNSET",
  "receipt_count": 0,
  "lead_topics": ["budget", "grants", "agency claims", "local infrastructure"],
  "vernacular_profile": "local plain-language civic style"
}
```

---

## 51-state registry

Canonical path:

```text
alms/states/state_registry.json
```

Required fields:

```json
{
  "registry_id": "ALMS_51_STATE_REGISTRY",
  "registry_version": "1.0.0",
  "states": []
}
```

---

## Alabama lead rule

Alabama may move fastest, but it cannot bypass evidence.

```json
{
  "lead_state": "AL",
  "speed_rule": "fast intake, strict receipts",
  "promotion_rule": "no state_root without replayable receipts",
  "public_lane": "67ACTNOWAL"
}
```

---

## 67ACTNOWAL

67ACTNOWAL is the Alabama lead adaptation of the 67ACTNOW civic firewall concept.

It means:

```text
67ACTNOWAL = local political edge network + ALMS receipts + public updates + state root
```

Core public line:

```text
Alabama takes the lead on speed.
Receipts before narratives.
Local claims. State roots. Public proof.
```

---

## Guardrails

1. No state lane may claim VERIFIED without ALMS receipts.
2. No state root may be promoted from DRAFT without replay.
3. No national root may include a state marked BLOCKED unless explicitly labeled.
4. Vernacular translation must preserve source links and verdict labels.
5. Political nodes are civic verification routers, not party-owned truth machines.
6. Humor is allowed. Fake verification is not.

---

## First build sequence

```json
{
  "step_1": "create alms/states/state_registry.json",
  "step_2": "initialize Alabama as ACTIVE lead lane",
  "step_3": "initialize Minnesota as ACTIVE budget proof lane",
  "step_4": "compute state roots after receipts exist",
  "step_5": "fold state roots into national_51_state_root"
}
```
