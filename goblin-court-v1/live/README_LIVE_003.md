# LIVE_003 — x402 Network Settlement Pass

**Status:** LIVE SETTLEMENT PASS STARTED  
**Branch:** `gc-v1-live-003`  
**Canonical Demo:** `MN-STEARNS-003`  
**Builder Code:** `bc_j1200j64`

---

## Purpose

This pass attaches a real x402 middleware boundary in front of the already-merged paid Prompt Pack Unit gate.

Target flow:

```text
Receipt -> Replay -> Score 78 -> x402 Payment Required -> Gate -> Prompt Pack Unit
```

---

## What This Adds

```text
goblin-court-v1/live/
  README_LIVE_003.md
  package.json
  .env.example
  server.mjs
  lineage_live_003.test.mjs
```

The live server protects one route:

```text
GET /api/mn-stearns-003/prompt-pack
```

The route returns the paid `PROMPT_PACK_UNIT_V0_1` only after:

1. x402 middleware accepts payment for the protected route.
2. The existing `gate_003.js` lineage check passes.

---

## Boundaries Preserved

This pass does not add:

- DDL
- migrations
- database state
- subscriptions
- marketplace behavior
- generated images
- agents
- additional seed cases

---

## Default Safety Mode

The default `.env.example` uses Base Sepolia:

```text
GC_X402_NETWORK=eip155:84532
GC_X402_FACILITATOR_URL=https://x402.org/facilitator
```

For production Base mainnet, switch to:

```text
GC_X402_NETWORK=eip155:8453
GC_X402_FACILITATOR_URL=https://api.cdp.coinbase.com/platform/v2/x402
```

Production CDP facilitator usage requires CDP API keys and a real receiving wallet address. Do not test mainnet with large amounts.

---

## Local Test

```bash
cd goblin-court-v1/live
npm install
npm test
npm start
```

Expected test output:

```text
PASS live lineage fixture test
```

---

## Core Invariant

```text
Network settlement unlocks access.
Lineage gate still decides whether the paid artifact may be served.
```
