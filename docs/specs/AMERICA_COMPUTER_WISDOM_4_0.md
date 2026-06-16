# America Computer Wisdom 4.0

Status: DRAFT_CANON
Operator: Jay Wisdom
Primary identity: jaywisdom.base
ENS identity: jaywisdom.eth

## Core thesis

America Computer Wisdom 4.0 is the machine-reasoning layer above Based America 3.0.

Based America 3.0 makes public verification local, funny, onchain-ready, and community-distributed.

Computer Wisdom 4.0 makes the same system reason over receipts, detect contradictions, route claims to the correct state lane, compute roots, and surface what changed without requiring humans to manually chase every workflow.

---

## System identity

```json
{
  "system": "America Computer Wisdom 4.0",
  "operator": "Jay Wisdom",
  "primary_identity": "jaywisdom.base",
  "ens_identity": "jaywisdom.eth",
  "engine": "Computer Wisdom",
  "verification_core": "ALMS",
  "public_layer": "Based America 3.0",
  "principle": "machines may assist reasoning, but receipts decide truth"
}
```

---

## Relationship to prior layers

```json
{
  "America_2_0": "civic verification infrastructure",
  "Based_America_3_0": "public Base-native distribution and participation layer",
  "America_Computer_Wisdom_4_0": "machine-speed reasoning, routing, contradiction detection, and root-aware state intelligence"
}
```

---

## Architecture

```text
Citizen Claim
  -> Local Vernacular Parser
  -> State Lane Router
  -> Source Requirement Engine
  -> ALMS Receipt Builder
  -> Replay Verifier
  -> Dependency + Version Gates
  -> Merkle Root Engine
  -> Computer Wisdom Contradiction Scanner
  -> Public Explanation Card
  -> Base / Zora / Community Distribution
```

---

## Core modules

### 1. Vernacular parser

Translates local language into structured civic claims without losing tone.

```json
{
  "input": "They say the budget math changed again, show the receipt.",
  "claim_type": "budget_forecast",
  "state": "MN",
  "required_source": true,
  "tone": "local_plain_language"
}
```

---

### 2. State lane router

Routes claims to the proper state ledger.

```json
{
  "state_code": "AL | MN | DC | ...",
  "lane_id": "67ACTNOWAL | 67ACTNOW | STATE_ALMS",
  "route_status": "ROUTED | NEEDS_STATE | BLOCKED"
}
```

---

### 3. Source requirement engine

Decides what evidence is required before a claim can be verified.

```json
{
  "claim_id": "CW4-0001",
  "required_evidence": [
    "public_source_url_or_repo_path",
    "frozen_bytes_or_text",
    "hash",
    "replay_result"
  ],
  "default_verdict": "INDETERMINATE"
}
```

---

### 4. Contradiction scanner

Finds conflicts across receipts and roots.

```json
{
  "scanner": "CW_CONTRADICTION_SCANNER_V1",
  "checks": [
    "same_claim_different_hash",
    "same_source_different_verdict",
    "verified_label_without_receipt",
    "state_root_includes_blocked_claim",
    "public_caption_claims_more_than receipt proves"
  ]
}
```

---

### 5. Public explanation card

Turns machine results into human-readable updates.

```json
{
  "title": "Budget Goblin Detected",
  "claim": "string",
  "verdict": "PASS | FAIL | INDETERMINATE | TAINTED",
  "why": "plain language explanation",
  "receipt": "repo path or URL",
  "root": "sha256:<64-hex>"
}
```

---

## Truth rule

Computer Wisdom may classify, route, summarize, and explain.

Computer Wisdom must not invent truth.

Only ALMS receipts, replay outputs, version registry state, dependency gates, and Merkle roots may promote a claim to VERIFIED.

---

## Machine-speed loop

```text
ingest -> classify -> route -> require source -> build receipt -> replay -> root -> scan contradictions -> publish explanation -> collect feedback
```

Machine-readable loop:

```json
{
  "loop": [
    "claim_ingest",
    "vernacular_parse",
    "state_route",
    "source_requirement",
    "receipt_build",
    "replay_verify",
    "version_gate",
    "dependency_gate",
    "merkle_root",
    "contradiction_scan",
    "public_card"
  ]
}
```

---

## Guardrails

1. No claim may be labeled VERIFIED without ALMS PASS.
2. No public card may omit verdict.
3. No machine summary may hide INDETERMINATE.
4. No state root may include a BLOCKED claim as clean.
5. No contradiction may be auto-resolved without a new receipt.
6. No Base / ENS anchor may be claimed without wallet receipt, tx hash, EAS UID, or signed proof.
7. Humor is allowed; fake verification is forbidden.

---

## First deployment lanes

```json
{
  "AL": {
    "lane": "67ACTNOWAL",
    "role": "speed lead",
    "computer_wisdom_task": "fast claim routing + source requirement"
  },
  "MN": {
    "lane": "67ACTNOW",
    "role": "budget proof lane",
    "computer_wisdom_task": "budget claim parsing + receipt explanation"
  }
}
```

---

## Public slogan

```text
America Computer Wisdom 4.0

Machines can reason.
Receipts decide.
jaywisdom.base
```

---

## Next build step

```json
{
  "next": "create claim_intake_schema.json",
  "then": "create contradiction_scanner_spec",
  "then_after": "wire first MN budget explanation card"
}
```
