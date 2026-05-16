# Witness v0.4 Runtime

Isolated operational project surface for the Witness court pilot inside `jsonwisdom/AL`.

## Purpose

Witness v0.4 exposes a minimal FastAPI runtime for append-only court event replay, Merkle convergence, inclusion proofs, and fork proposals.

This project is intentionally isolated under:

```text
projects/witness-v0.4-runtime/
```

It is not the AL constitutional root. It is the disposable runtime surface.

## Runtime endpoints

```text
GET  /health
GET  /summarize
GET  /replay
GET  /proof/{index}
POST /governance/fork
GET  /convergence-receipt
```

## Render deployment

Render should target:

```text
Branch: project/witness-v0.4-runtime
Root Directory: projects/witness-v0.4-runtime
Build Command: pip install -r requirements.txt
Start Command: mkdir -p /tmp/witness-data && uvicorn witness_court_pilot_v4:app --host 0.0.0.0 --port $PORT
```

Free-tier mode uses:

```text
DATA_DIR=/tmp/witness-data
```

This is ephemeral demo mode. It proves runtime convergence, not persistent continuity.

## Canonicality

Visible in Git is not canonical.

This runtime becomes receipt-relevant only when endpoint bytes are captured, independently recomputed, and bound into the AL receipt/canonical item registry.

## Deletion policy

Nothing is deleted from AL unless it passes three consecutive audits.

Extraction does not imply deletion.
