# ALMS Production Receipts

`_truth/receipts/` is the Meme Court Flywheel production genesis.

Rule:
- One claim per JSON file.
- Receipt files are append-only.
- Do not edit old receipts to correct them.
- If a claim must be reversed, add a new receipt with `verdict: "VOID"` and `voids_claim_id` pointing to the original claim.
- Filenames should match `CLAIM_YYYYMMDD_HHMMSSZ_nonce.json`.

Required fields:
- `claim_id`
- `timestamp_utc`
- `actor`
- `nonce`
- `inputs`
- `outputs`
- `verdict`

Pipeline:

```txt
receipt -> raw-byte sha256 -> daily inventory -> chained audit manifest -> IPFS witness -> EAS anchor
```

Doctrine:

```txt
Receipts first.
Anchors second.
No claim graduates without evidence.
```
