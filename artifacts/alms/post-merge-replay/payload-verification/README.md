# ALMS Payload Verification

Directories-first workspace for verifying the unsigned ALMS payload replay.

## Bedrock binding

`59448d850d355854956cb5834ebef17f7f14c7dc`

## Boundaries

- No GREEN verdict is assumed.
- No workflow dispatch is performed by this scaffold.
- No payload is evidence until downloaded, hashed, and schema-validated.
- No signer operates in this layer.
- No signed CRO is produced here.

## Layout

- `run-metadata/` — workflow run and job metadata
- `artifacts/` — downloaded unsigned payload
- `logs/` — workflow and verification logs
- `hashes/` — SHA-256 bindings
- `receipts/` — local verification receipts
