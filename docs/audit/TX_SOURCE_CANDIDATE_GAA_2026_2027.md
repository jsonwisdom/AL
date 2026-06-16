# TX Source Candidate — General Appropriations Act 2026–2027

## Status

`SOURCE_CANDIDATE_ACCEPTED_FOR_FREEZE`

This document records the first official Texas source candidate for the TX PASS gate.

## Source

- Jurisdiction: `TX`
- Document: `General Appropriations Act 2026–2027`
- Source URL: `https://www.lbb.texas.gov/Documents/GAA/General_Appropriations_Act_2026_2027.pdf`
- Domain: `lbb.texas.gov`
- Publisher: Texas Legislative Budget Board
- Format: `PDF`
- Candidate frozen path: `fixtures/tx/sources/tx_general_appropriations_act_2026_2027.pdf`

## Classification

| Check | Result |
|---|---|
| Official Texas government domain | `PASS` |
| Legislative Budget Board source | `PASS` |
| General Appropriations Act | `PASS` |
| Byte-freezable artifact | `PASS` |
| Suitable for TX PASS gate | `YES_AFTER_FREEZE_AND_HASH` |

## Boundary

This candidate does not flip TX to `PASS` by itself.

TX can only move to `PASS` after the exact PDF bytes are committed under:

```text
fixtures/tx/sources/tx_general_appropriations_act_2026_2027.pdf
```

and the TX claim hash is updated to match those committed bytes.

## Required Operator Steps

```bash
mkdir -p fixtures/tx/sources
curl -L \
  "https://www.lbb.texas.gov/Documents/GAA/General_Appropriations_Act_2026_2027.pdf" \
  -o fixtures/tx/sources/tx_general_appropriations_act_2026_2027.pdf

bash scripts/hash_source.sh fixtures/tx/sources/tx_general_appropriations_act_2026_2027.pdf
```

Then update only the allowed TX claim fields:

- `claim_text`
- `source.description`
- `source.source_url`
- `frozen_artifact.reference`
- `hash`

Do not change engine rules.
Do not mark TX as `PASS` manually.
Do not claim national `PASS` until replay confirms every state is `PASS`.
Do not claim Base/EAS, ENS, or on-chain anchoring from this step.

## Principle

Official source first. Freeze bytes second. Hash third. Replay decides.

**Hashable ≠ verified. Receipts > vibes.**
