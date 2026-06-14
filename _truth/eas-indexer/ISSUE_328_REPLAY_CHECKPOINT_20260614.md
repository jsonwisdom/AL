# ISSUE 328 REPLAY CHECKPOINT — EAS INDEXER / FEDERAL_AI / JOY

**Date:** 2026-06-14  
**Repo:** jsonwisdom/AL  
**Issue:** #328 — EAS Indexer Integration for ALMS  
**Checkpoint Comment ID:** 4703346670  
**Anchor State:** YELLOW_READY  
**NO_FAKE_GREEN:** ACTIVE

---

## 1. Ruling

The EAS Indexer integration lane is feasible and ready for deployment testing, but it is **not GREEN** until live infrastructure, query outputs, resolver event visibility, replay receipts, and committed evidence exist.

**Current state:** YELLOW_READY  
**Reason:** Architecture is formulated; live replay evidence is still pending.

---

## 2. Five Gates Required For GREEN

GREEN requires all five artifacts below:

1. `live_graphql_endpoint`
2. `uid_query_output`
3. `resolver_event_status`
4. `replay_receipt_hash`
5. `committed_receipt`

If any one is missing, the lane remains YELLOW_READY.

---

## 3. Lane Replay

### A. EAS / ALMS Indexer

**Goal:** Run a self-hosted EAS indexer for Base and expose ALMS attestations through GraphQL.

**Required config:**

- Chain ID: `8453`
- EAS: `0x4200000000000000000000000000000000000021`
- SchemaRegistry: `0x4200000000000000000000000000000000000020`
- Database: Postgres
- Deployment target: Render or equivalent managed service

**Replay target UIDs:**

- `0x4d6a7df50cba18e1086820732c158274b51adf9f17722c40d55fd3f73b5d6874`
- `0xcc3e5448328c3ca29282e05bacbc4dc96d4cd533f7144d0a437a6f39cceec1f1`

**GraphQL probe:**

```graphql
query ALMSReplay {
  attestations(where: { id_in: [
    "0x4d6a7df50cba18e1086820732c158274b51adf9f17722c40d55fd3f73b5d6874",
    "0xcc3e5448328c3ca29282e05bacbc4dc96d4cd533f7144d0a437a6f39cceec1f1"
  ] }) {
    uid
    attester
    recipient
    schemaId
    decodedData { name value }
    time
    revocationTime
  }
}
```

**Status:** YELLOW_READY until query output is captured and committed.

---

### B. Whitehouse / Federal AI Lane

**Goal:** Convert public AI governance claims into replayable docket entries.

**Integration use:** EAS indexer becomes the query membrane for public attestations related to FEDERAL_AI_ROOT_LANE.

**Required evidence:**

- Source document URL or archived copy
- Hash of source artifact
- ALMS docket entry
- EAS UID or pending attestation record
- Replay result showing claim -> source -> receipt continuity

**Status:** YELLOW_READY. No authority claim without receipt.

---

### C. DOJ Public-Record Lane

**Goal:** Track DOJ public records, enforcement statements, AI procurement signals, and evidence-policy artifacts without narrative drift.

**Required evidence:**

- Public source artifact
- Capture timestamp
- Hash
- Docket classification
- Replay check result

**Status:** YELLOW_READY. Public-record capture required before GREEN.

---

### D. Computer Wisdom Lane

**Goal:** Translate the EAS/ALMS indexer into public-facing explanation: what was claimed, what was proven, what remains pending.

**Output targets:**

- Plain-language explainer
- GitHub Pages or docs page
- GraphQL query example
- NO_FAKE_GREEN explanation

**Status:** YELLOW_READY. Explainer must reference committed receipts, not aspirations.

---

### E. JOY / Family Approvals Lane

**Goal:** Keep Family Approvals separate from technical overclaiming while allowing JOY to display human-readable replay outcomes.

**Boundaries:**

- JOY may display status summaries.
- JOY must not claim GREEN unless ALMS receipt is GREEN.
- Family approval artifacts are emotional/human records, not substitutes for infrastructure proof.

**Status:** YELLOW_READY.

---

## 4. Next Executable Step

Deploy or update the EAS indexer service with Base configuration, then run the UID probe and commit the first query output receipt.

Recommended receipt path:

```text
_truth/eas-indexer/receipts/ISSUE_328_UID_REPLAY_20260614.json
```

Recommended hash path:

```text
_truth/eas-indexer/receipts/SHA256SUMS
```

---

## 5. Final Check

**NO_FAKE_GREEN invariant:** ACTIVE  
**Current anchor:** YELLOW_READY  
**Promotion condition:** all five GREEN gates present and replayable from repo history.
