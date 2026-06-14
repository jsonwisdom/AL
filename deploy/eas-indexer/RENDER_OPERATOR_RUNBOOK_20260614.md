# EAS Indexer Render Operator Runbook — Issue #328

**Date:** 2026-06-14  
**Repo:** `jsonwisdom/AL`  
**Issue:** #328  
**Lane:** EAS Indexer Integration for ALMS  
**Anchor State:** `YELLOW_READY`  
**NO_FAKE_GREEN:** `ACTIVE`

---

## 1. Ruling

This runbook advances the EAS Indexer Integration lane from scaffolded receipt to live endpoint proof.

The lane remains `YELLOW_READY` until all five gates are proven from repo history:

```text
live_graphql_endpoint: false
uid_query_output: false
resolver_event_status: false
replay_receipt_hash: false
committed_receipt: true
```

A Render service being created is not enough for GREEN. A GraphQL endpoint must answer the ALMS UID replay query, the response must be committed, and the receipt hash must be recorded.

---

## 2. Existing committed artifacts

```text
deploy/eas-indexer/render.yaml.template
graphql/eas-indexer/ALMS_UID_REPLAY.graphql
scripts/eas-indexer/alms_uid_replay_probe.sh
_truth/eas-indexer/receipts/ISSUE_328_UID_REPLAY_20260614.json
```

---

## 3. Render service setup

Use Render Blueprint or manual Web Service creation.

### Service type

```text
Web Service / Docker-backed service
```

### Repo

```text
jsonwisdom/AL
```

### Blueprint template

```text
deploy/eas-indexer/render.yaml.template
```

Copy or adapt this template into the Render dashboard / deploy pipeline. Do not commit secrets.

---

## 4. Required environment variables

Set these in Render, not in git:

```text
ALCHEMY_BASE_API_KEY=<secret>
DATABASE_URL=<Render Postgres internal connection string>
CHAIN_ID=8453
EAS_CONTRACT_ADDRESS=0x4200000000000000000000000000000000000021
SCHEMA_REGISTRY_ADDRESS=0x4200000000000000000000000000000000000020
```

Optional operator label:

```text
ALMS_LANE=ISSUE_328_EAS_INDEXER
NO_FAKE_GREEN=true
```

---

## 5. Live endpoint target

Expected shape:

```text
https://<render-service-name>.onrender.com/graphql
```

Do not mark `live_graphql_endpoint` true until the endpoint responds to a GraphQL POST.

---

## 6. UID replay probe

After Render exposes `/graphql`, run from the repo root:

```bash
cd ~/AL 2>/dev/null || cd ~/COMPUTERWISDOM/AL
export EAS_GRAPHQL_ENDPOINT="https://YOUR-RENDER-SERVICE.onrender.com/graphql"
bash scripts/eas-indexer/alms_uid_replay_probe.sh
```

Expected output path:

```text
_truth/eas-indexer/live-probes/<UTC>/
```

Expected files:

```text
payload.json
query.graphql
variables.json
response.json
receipt.json
SHA256SUMS
```

---

## 7. Commit live probe receipt

After reviewing `response.json`, commit the probe artifacts:

```bash
git status --short
git add _truth/eas-indexer/live-probes/
git commit -m "receipt: record Issue 328 EAS UID replay probe"
git push
```

Then update Issue #328 with:

```text
live_graphql_endpoint=<endpoint>
probe_dir=_truth/eas-indexer/live-probes/<UTC>/
receipt_sha256=<sha256 of receipt.json from SHA256SUMS>
response_sha256=<sha256 of response.json from SHA256SUMS>
commit=<commit sha>
```

---

## 8. GREEN gate interpretation

### Gate 1 — live_graphql_endpoint

GREEN only when endpoint returns a valid GraphQL response.

### Gate 2 — uid_query_output

GREEN only when the ALMS UIDs are queried and `response.json` is committed.

Target UIDs:

```text
0x4d6a7df50cba18e1086820732c158274b51adf9f17722c40d55fd3f73b5d6874
0xcc3e5448328c3ca29282e05bacbc4dc96d4cd533f7144d0a437a6f39cceec1f1
```

### Gate 3 — resolver_event_status

GREEN only when resolver event state is either:

```text
INDEXED
NOT_PRESENT_FOR_TARGET_UIDS_WITH_EXPLANATION
```

Do not fake event success if the current query returns attestations but not custom resolver logs.

### Gate 4 — replay_receipt_hash

GREEN only when `receipt.json` hash is present in `SHA256SUMS` and included in the Issue #328 comment.

### Gate 5 — committed_receipt

Already true for scaffold receipt. Final GREEN requires the live probe receipt commit as well.

---

## 9. Post-probe Issue #328 comment template

```markdown
## ISSUE #328 LIVE UID REPLAY PROBE

**ANCHOR_STATE:** YELLOW_READY -> [candidate update]  
**NO_FAKE_GREEN:** ACTIVE

### Endpoint
`<live_graphql_endpoint>`

### Probe directory
`_truth/eas-indexer/live-probes/<UTC>/`

### Hashes
- `response.json`: `<sha256>`
- `receipt.json`: `<sha256>`
- `SHA256SUMS`: `<sha256>`

### UID replay result
- Original UID: `<FOUND | NOT_FOUND | ERROR>`
- Correction UID: `<FOUND | NOT_FOUND | ERROR>`

### Resolver events
`<INDEXED | PENDING | NOT_PRESENT_FOR_TARGET_UIDS_WITH_EXPLANATION>`

### Commit
`<commit_sha>`

### Ruling
`<YELLOW_READY | GREEN_CANDIDATE | GREEN>`
```

---

## 10. Hard stop rule

If the endpoint fails, returns HTML, returns auth errors, or returns empty data for both target UIDs, record the failure honestly as a YELLOW/RED probe receipt.

Failure receipts are still useful. Fake GREEN is not.
