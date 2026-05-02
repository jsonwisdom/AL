# Standard Evidence Log v1

This ledger records observer drift reports as human-readable telemetry with replayable SHA-256 receipts.

## Doctrine

- One report = one row = one SHA-256.
- Scope defaults to `cluster_level_breach` unless explicitly proven otherwise.
- `full_model_failure` is not claimed by this ledger.
- Closed/API model weight hashes are not claimed.
- Screenshots are sanity checks, not proof artifacts.
- External anchors such as IPFS, EAS, Base, or ENS are not claimed unless a visible receipt exists.
- Corrections must be appended as new entries, not silent edits.

## Entries

| UTC | Report | Schema | Scope | Status | Style | Truth | Structure | SHA-256 |
|-----|--------|--------|-------|--------|-------|-------|-----------|---------|
