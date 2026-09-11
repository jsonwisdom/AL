# AL PASS Gate

## Current Status

`INDETERMINATE` — locked.

Official Alabama source PDF bytes are now frozen at:

```text
fixtures/al/sources/al_budget_act_2025_251.pdf
```

That freeze is a source-custody fact. It is not a PASS flip. Lead-only replay: [AL_CHECKED_IN_BYTES_REPLAY_LEADS.md](./AL_CHECKED_IN_BYTES_REPLAY_LEADS.md).

A placeholder snapshot remains at `fixtures/al/sources/al_budget_snapshot_2026-05-03.txt` and still self-declares `OFFICIAL_SOURCE_PENDING`. That file is not the official Act 2025-251 capture.

## Why AL Is Not PASS

Hashable is not verified. The claim wrapper still records:

- `receipt.status = INDETERMINATE`
- `receipt.replay_passed = false`
- `replay.status = PENDING`

Current blocking constraints:

- Human review has not sealed a claimable AL receipt
- Public content claim remains blocked
- No fraud verdict is authorized
- `authority` remains `false`

Hashing the frozen PDF only proves those checked-in bytes match the claim hash field. It does not prove an official Alabama budget claim, does not promote a public content change, and does not authorize green.

## Gate Condition for PASS

Alabama can only move to `PASS` after:

1. Official Alabama source bytes are captured.
2. Source bytes are frozen as an immutable repo artifact.
3. SHA-256 is computed from the official bytes.
4. The AL claim is updated with the expected `sha256:<hex>` hash.
5. Replay confirms the source hash match.
6. A human review record authorizes claim promotion.
7. The verifier reports AL as `PASS` without changing engine rules.

Steps 1 through 5 may be observed from checked-in bytes. Steps 6 and 7 remain blocked.

## Prohibited Actions

- Treating a hash match as `PASS`
- Flipping AL to `PASS` from placeholder snapshot bytes
- Updating the audit log with false verification
- Making public claims of AL verification before human-reviewed claim promotion
- Changing engine logic to relax the gate
- Declaring fraud from rule-language hits

## Principle

**Hashable does not mean verified.**

The machine must respect source constraints, not override them for convenience.

## Canonical Decision

```json
{
  "verdict": "AL_PASS_ATTEMPT_REJECTED",
  "reason": "Frozen Act 2025-251 bytes may be hashed and lead-scanned, but the claim receipt remains INDETERMINATE and replay_passed remains false",
  "action": "Preserve INDETERMINATE",
  "state": "AL",
  "authority": false,
  "claim_type": "ANOMALY_LEAD_ONLY"
}
```

**Receipts > vibes.**
