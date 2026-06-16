# AL PASS Gate

## Current Status

`INDETERMINATE` — locked.

## Why AL Is Not PASS

The current Alabama source artifact in `fixtures/al/sources/` self-declares that it is not eligible for verified status.

Current blocking constraints:

- `OFFICIAL_SOURCE_PENDING`
- Not an official source capture
- Not a verified Alabama budget claim
- Not eligible for `VERIFIED` status

Hashing this placeholder would only prove the placeholder bytes exist. It would not prove an official Alabama budget source claim.

## Gate Condition for PASS

Alabama can only move to `PASS` after:

1. Official Alabama source bytes are captured.
2. Source bytes are frozen as an immutable repo artifact.
3. SHA-256 is computed from the official bytes.
4. The AL claim is updated with the expected `sha256:<hex>` hash.
5. Replay confirms the source hash match.
6. The verifier reports AL as `PASS` without changing engine rules.

## Prohibited Actions

- Hashing the placeholder file to force `PASS`
- Flipping AL to `PASS` based on placeholder bytes
- Updating the audit log with false verification
- Making public claims of AL verification before official source replay
- Changing engine logic to relax the gate

## Principle

**Hashable does not mean verified.**

The machine must respect source constraints, not override them for convenience.

## Canonical Decision

```json
{
  "verdict": "AL_PASS_ATTEMPT_REJECTED",
  "reason": "Source artifact self-declares non-verified / official source pending",
  "action": "Preserve INDETERMINATE",
  "state": "AL"
}
```

**Receipts > vibes.**
