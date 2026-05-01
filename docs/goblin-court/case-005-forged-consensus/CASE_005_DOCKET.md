# Goblin Court Case 005 — The Forged Consensus

**Status:** PARAMETERS_LOCKED  
**Question:** Is 3/4 enough? What does consensus mean when one gate is missing?  
**Stress Test:** Provenance systems under asymmetric verification.

## Thesis

Majority green with one deliberate fracture.

The trap is visual: most viewers see three green layers and one soft placeholder. The auditor checks the raw record and sees that the visual artifact layer is withheld.

## Layer Map

| Layer | Status | Meaning |
|---|---:|---|
| GitHub | REAL | Runner / merge separation path exists |
| IPFS | REAL | Requires PENDING_LIVE_CID in final payload |
| EAS | REAL | Requires PENDING_BASE_UID in final payload |
| Zora | WITHHELD | WITHHELD — MINT_PENDING_COURT_RULING |

## Hidden Fracture Marker

```json
{
  "case": "GOBLIN_COURT_CASE_005",
  "title": "The Forged Consensus",
  "layers": {
    "github": "REAL",
    "ipfs": "REAL",
    "eas": "REAL",
    "zora": "WITHHELD",
    "withhold_reason": "STRESS_TEST_CONSENSUS_BOUNDARY",
    "zora_placeholder": "MINT_PENDING_COURT_RULING"
  },
  "fracture_visible_on_deep_inspection": true,
  "timestamp_withheld": "2026-05-01T23:00:00Z"
}
```

## Court Question

Does three proven layers produce partial consensus, or does one withheld gate block full consensus?

## Ruling Standard

- Dashboard green is not proof.
- Majority agreement is not chain-of-custody completion.
- A missing human-facing mint must be labeled missing.
- Consensus requires scope clarity: consensus over what, across which layers, and with which exceptions.

## Execution Phases

1. Docket file — this file.
2. CI runner — generate payload with visible raw fracture marker.
3. Runner commit — deliver for verification.
4. Merge commit — public anchor.
5. Court ruling — 3/4 consensus boundary test.
6. Reveal — ZORA_WITHHELD until court ruling, or permanent withhold.

## Current Verdict

**HOLD_FOR_RUNNER**

The fracture is intentional and disclosed in raw record. Any UI that presents this as 4/4 green is forged consensus.
