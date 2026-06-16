# Taxed by Prompt — Zora Factory & Flywheel

Status: DRAFT_CANON
Operator: Jay Wisdom
Identity: jaywisdom.eth / jaywisdom.base / jaywisdom.base.eth

## Core thesis

If a prompt can generate a policy idea, budget claim, public narrative, or institutional action, it should also generate a receipt, an accounting surface, and a public research trail.

If the prompt spends public money, the prompt owes the public a receipt.

---

## System merge

```json
{
  "project": "Taxed by Prompt",
  "subsystem": "Congressional Idea Factory",
  "distribution_layer": "Zora Factory",
  "economic_loop": "Receipt Flywheel",
  "verification_layer": "ALMS",
  "operator": "Jay Wisdom",
  "identity": ["jaywisdom.eth", "jaywisdom.base", "jaywisdom.base.eth"]
}
```

---

## Three-layer model

### 1. Idea Factory

Turns public policy prompts into structured proposals.

Inputs:

- policy idea
- sponsor / committee / agency target
- claimed benefit
- claimed cost
- public record sources
- unknowns

Output:

```json
{
  "idea_id": "TBP-0001",
  "claim": "string",
  "affected_budget_surface": "string",
  "agency_or_committee": "string",
  "evidence_required": true,
  "status": "DRAFT"
}
```

---

### 2. ALMS Receipt Layer

Turns the idea into an auditable object.

Required surfaces:

- source paths
- cost assumptions
- research citations
- replay status
- version registry state
- Merkle inclusion root

Output:

```json
{
  "receipt_id": "TBP-0001-R001",
  "idea_id": "TBP-0001",
  "artifact_paths": [],
  "hashes": [],
  "verdict": "PASS | FAIL | INDETERMINATE | TAINTED",
  "merkle_root": "sha256:<64-hex>"
}
```

---

### 3. Zora Factory

Turns verified receipts into public-facing drops.

Zora artifacts may include:

- visual artwork
- short public caption
- audit card
- receipt link
- Merkle root
- repo link
- wallet / identity anchor

Zora does not create truth. Zora distributes truth objects.

---

## Flywheel

```text
Prompt -> Idea -> Research -> Receipt -> Merkle Root -> Zora Drop -> Public Feedback -> New Prompt
```

Machine-readable version:

```json
{
  "flywheel": [
    "prompt_intake",
    "idea_structuring",
    "accounting_surface",
    "evidence_collection",
    "alms_receipt",
    "merkle_root",
    "zora_publication",
    "feedback_ingestion",
    "next_prompt"
  ]
}
```

---

## Zora drop template

```json
{
  "title": "Taxed by Prompt: <idea>",
  "subtitle": "Congressional Idea Factory Receipt",
  "creator": "Jay Wisdom",
  "identity": "jaywisdom.base",
  "receipt_id": "TBP-0001-R001",
  "verdict": "PASS | FAIL | INDETERMINATE | TAINTED",
  "merkle_root": "sha256:<64-hex>",
  "repo_url": "https://github.com/jsonwisdom/AL",
  "caption": "If the prompt spends public money, the prompt owes the public a receipt."
}
```

---

## Guardrails

1. No Zora drop may claim VERIFIED unless ALMS receipt is PASS.
2. INDETERMINATE drops must be labeled as research-in-progress.
3. TAINTED drops must be labeled as boundary violation / rejected evidence.
4. Zora contract address must not be claimed until confirmed by chain receipt.
5. Receipt hash is not a deed. Transaction hash is not a contract.
6. Public narrative must point back to evidence.

---

## Accounting & Research prompt

Use this prompt for external model review:

```text
Audit this policy idea as a Taxed by Prompt receipt.
Return JSON only.

Input:
- policy idea:
- claimed benefit:
- claimed cost:
- affected agency / committee:
- sources:

Check:
1. What claim is being made?
2. What public money or public authority is implicated?
3. What evidence is required before publication?
4. What is the minimum accounting surface?
5. What ALMS receipt fields are missing?
6. Can this be published to Zora as PASS, INDETERMINATE, FAIL, or TAINTED?

Hard rules:
- Do not invent citations.
- Do not invent costs.
- Do not mark VERIFIED without receipt.
- If evidence is missing, return INDETERMINATE.
```

---

## First production lane

```json
{
  "lane": "Minnesota Budget Receipts",
  "seed": "C0001",
  "source": "_truth/sources/mmb-feb-2026-forecast.txt",
  "zora_series": "Taxed by Prompt: State Budget Receipts",
  "status": "WAITING_FOR_REPLAY_PASSED"
}
```
