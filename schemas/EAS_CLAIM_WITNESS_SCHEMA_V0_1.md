# EAS Claim Witness Schema V0.1

Status: CLAIM_WITNESS_ONLY
Authority: false
Membrane: HOLDS

## Purpose

Define how EAS may witness claims within the replay spine.

EAS records what was claimed, when it was claimed, and who made the claim. EAS does not make claims true.

## Allowed Witness Events

- Receipt hash observed.
- Replay index updated.
- Emergency context declared.
- Public route schema published.
- Public state transition claimed.

## Forbidden Witness Events

- Universal truth declarations.
- Legal authority declarations.
- Medical authority declarations.
- Custody declarations.
- Official government authority declarations.

## Schema

```json
{
  "claim_id": "STRING",
  "claimed_by": "STRING",
  "claimed_at": "TIMESTAMP",
  "claim_text": "STRING",
  "receipt_hash": "OPTIONAL",
  "authority": false,
  "membrane": "HOLDS"
}
```

## Replay Rule

Witnessing a claim is not equivalent to proving a claim.

## Final Line

EAS witnesses. Replay evaluates. Authority remains false.
