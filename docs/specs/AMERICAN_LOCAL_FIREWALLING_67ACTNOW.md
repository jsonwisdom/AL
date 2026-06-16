# American Local Firewalling — 67ACTNOW

Status: DRAFT_CANON
Operator: Jay Wisdom
Identity: jaywisdom.eth / jaywisdom.base / jaywisdom.base.eth

## Core thesis

American local communities need edge verification networks: political nodes that speak local vernacular, collect public claims, and route them into ALMS receipts before narratives harden into policy reality.

67ACTNOW is the Minnesota-first vernacular civic layer.

---

## Model

```json
{
  "system": "American Local Firewalling",
  "lane": "67ACTNOW",
  "state": "Minnesota",
  "district_count": 67,
  "node_type": "political_edge_node",
  "verification_engine": "ALMS",
  "distribution": ["community", "Zora", "social", "weekly audits"],
  "tone": ["local", "funny", "democratic", "receipt-backed"]
}
```

---

## Edge networks

An edge network is a local claim-capture surface.

Inputs:

- district claim
- budget claim
- agency claim
- local quote
- public meeting note
- citizen question
- meme / vernacular framing

Output:

```json
{
  "edge_node": "MN-SD-01",
  "claim": "string",
  "source_required": true,
  "vernacular": "local plain-language explanation",
  "alms_status": "DRAFT | PASS | FAIL | INDETERMINATE | TAINTED"
}
```

---

## Political nodes

Political nodes are not party machines. They are civic verification routers.

Each node asks:

1. What is being claimed?
2. Who pays?
3. Who benefits?
4. Which public record proves it?
5. Which ALMS receipt tracks it?
6. What should local people vote on today?

---

## Local firewall rule

```text
No claim enters the local narrative layer as VERIFIED until ALMS receipts support it.
```

Allowed labels:

```json
["DRAFT", "NEEDS_RECEIPT", "PASS", "FAIL", "INDETERMINATE", "TAINTED"]
```

---

## Vernacular layer

The system must translate policy language into local speech without breaking the receipt.

Example:

```json
{
  "official_claim": "The February forecast estimates a structural balance change.",
  "vernacular": "The state says the money math changed. Show us the receipt.",
  "receipt_required": true
}
```

---

## 67ACTNOW daily loop

```text
Claim -> Plain language -> Receipt check -> Citizen vote -> Daily update -> Weekly audit
```

Machine form:

```json
{
  "daily_loop": [
    "claim_intake",
    "vernacular_translation",
    "source_check",
    "alms_receipt",
    "citizen_vote",
    "zora_or_social_card",
    "weekly_audit_rollup"
  ]
}
```

---

## Public caption

```text
67ACTNOW

67 districts. 67 receipts. One local firewall.

If they claim it, they can show it.
If they spend it, we can count it.
If they dodge it, the node turns yellow.
```

---

## Guardrails

1. No doxxing.
2. No private personal data.
3. No unverified accusations.
4. No party-owned truth labels.
5. Humor is allowed; fake verification is not.
6. Local language must preserve source links and verdict labels.
7. ALMS receipts override vibes.

---

## Relationship to Taxed by Prompt

```json
{
  "Taxed_by_Prompt": "idea/accounting factory",
  "ALMS": "verification and receipt layer",
  "67ACTNOW": "local vernacular distribution layer",
  "Zora_Factory": "public artifact and flywheel layer"
}
```

---

## First lane

```json
{
  "lane": "MN Budget for Fun",
  "seed": "C0001",
  "topic": "Minnesota budget forecast",
  "status": "WAITING_FOR_REPLAY_PASSED",
  "next": "daily citizen budget claim card"
}
```
