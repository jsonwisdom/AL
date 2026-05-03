# AL Source Candidate — Act 2025-251

## Status

`SOURCE_CANDIDATE_ACCEPTED_FOR_FREEZE`

This document records the first official Alabama source candidate for the AL PASS gate.

## Source

- Jurisdiction: `AL`
- Document: `FY26 General Fund Appropriation Bill — Act 2025-251 (Signed)`
- Source URL: `https://budget.alabama.gov/wp-content/uploads/2026/01/FY26-General-Fund-Appropriation-Bill-Act-2025-251-Signed.pdf`
- Domain: `budget.alabama.gov`
- Format: `PDF`
- Candidate frozen path: `fixtures/al/sources/al_budget_act_2025_251.pdf`

## Classification

| Check | Result |
|---|---|
| Official Alabama domain | `PASS` |
| Signed appropriations act | `PASS` |
| Byte-freezable artifact | `PASS` |
| Suitable for AL PASS gate | `YES_AFTER_FREEZE_AND_HASH` |

## Boundary

This candidate does not flip AL to `PASS` by itself.

AL can only move to `PASS` after the exact PDF bytes are committed under:

```text
fixtures/al/sources/al_budget_act_2025_251.pdf
```

and the AL claim hash is updated to match those committed bytes.

## Required Operator Steps

```bash
mkdir -p fixtures/al/sources
curl -L \
  "https://budget.alabama.gov/wp-content/uploads/2026/01/FY26-General-Fund-Appropriation-Bill-Act-2025-251-Signed.pdf" \
  -o fixtures/al/sources/al_budget_act_2025_251.pdf

bash scripts/hash_source.sh fixtures/al/sources/al_budget_act_2025_251.pdf
```

Then update only the allowed AL claim fields:

- `claim_text`
- `source.description`
- `source.source_url`
- `frozen_artifact.reference`
- `hash`

Do not change engine rules.
Do not mark AL as `PASS` manually.
Do not update audit log until replay confirms.

## Principle

Official source first. Freeze bytes second. Hash third. Replay decides.

**Hashable ≠ verified. Receipts > vibes.**
