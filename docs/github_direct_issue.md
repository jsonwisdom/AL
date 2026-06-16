# GitHub Direct Connector Issue

Status: ACTIVE
Authority: false

## Rule

Commit existence does not equal content validity.

After any GitHub direct write, fetch the file and verify content before promotion.

## Observed Failure

The connector returned commit SHAs while writing truncated JSON to `specs/divergence_proof_v1.json`.

Result: sealing blocked.

## Operational Response

If connector writes truncate content:

1. Stop connector writes for that file.
2. Restore minimal valid content.
3. Use GitHub web UI or terminal git push.
4.