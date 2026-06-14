# Base DOJ Batch Flywheel V0.1

**Repo:** jsonwisdom/AL  
**Lane:** Base Batches x DOJ Batches x Zora Flywheel  
**Anchor State:** YELLOW_READY  
**NO_FAKE_GREEN:** ACTIVE  
**Purpose:** define how Docker, Render, Zora Arena, ALMS replay, and public-record DOJ batches are assessed at the metadata level before any live proof or public claim is promoted.

---

## 1. Ruling

Docker, Render, and Zora Arena objects inside the Zora Flywheel are **metadata-assessed objects** until independently proven by receipt.

They may support public proof, education, publication, and replay, but they do not become GREEN merely because they exist.

**GREEN requires:**

1. source object path or endpoint,
2. reproducible metadata extract,
3. replay output,
4. hash receipt,
5. committed repo evidence,
6. optional external/on-chain witness.

---

## 2. Batch Families

### 2.1 Base Batches

Base batches are settlement, attestation, identity, or public-proof objects tied to Base infrastructure.

Examples:

- EAS UID batches,
- schema batches,
- resolver event batches,
- Zora object batches,
- Base name / identity batches,
- public-proof content batches.

### 2.2 DOJ Batches

DOJ batches are public-record or evidentiary-reference objects.

They are not assertions of guilt, wrongdoing, or official DOJ action unless directly supported by a public source receipt.

Examples:

- public filings,
- press releases,
- court docket references,
- FOIA / public-record request receipts,
- enforcement-policy documents,
- agency guidance,
- batch comparisons against ALMS provenance rules.

### 2.3 Join Rule

A Base batch may reference a DOJ batch only when the join key is explicit:

```text
join_key = public_record_id | docket_id | receipt_hash | uid | url_hash | artifact_hash
```

No loose narrative join is allowed.

---

## 3. Metadata Assessment Layer

Every object entering the flywheel receives a metadata envelope.

```json
{
  "object_id": "stable local or remote identifier",
  "object_family": "docker|render|zora|base_eas|doj_public_record|alms_receipt",
  "source_uri": "path, endpoint, tx, uid, or public URL",
  "capture_time_utc": "ISO-8601",
  "metadata_hash": "sha256 of normalized metadata",
  "content_hash": "sha256 when content is captured",
  "authority_level": "LOCAL|PUBLIC_HTTP|GITHUB|ONCHAIN|AGENCY_PUBLIC_RECORD",
  "truth_state": "RED|YELLOW_READY|GREEN",
  "replay_status": "PENDING|PASS|FAIL",
  "rollback_status": "AVAILABLE|NOT_AVAILABLE|NOT_REQUIRED",
  "notes": "bounded operator note"
}
```

---

## 4. Docker / Render / Zora Arena Roles

### Docker

Docker is the reproducibility container.

Required metadata:

- image name,
- image digest,
- Dockerfile hash,
- build args hash,
- environment variable names only, never secrets,
- run command,
- healthcheck result.

### Render

Render is the hosted execution surface.

Required metadata:

- service name,
- endpoint,
- deployment id when available,
- commit SHA deployed,
- env var names only,
- healthcheck response hash,
- GraphQL or HTTP probe hash.

### Zora Arena

Zora Arena is the public presentation and retail/attention surface.

Required metadata:

- collection / coin / post / object id,
- creator identity,
- content URI,
- media hash when available,
- description hash,
- linked receipt hash,
- revenue / retail status if applicable.

---

## 5. Purpose, Wit, Wisdom Applied

### Purpose

Every batch must answer: **what public function does this serve?**

Allowed functions:

- replay,
- provenance,
- education,
- evidence indexing,
- civic transparency,
- family archive,
- identity continuity,
- retail/publication.

### Wit

Every batch must include a human-readable explanation.

If a normal person cannot understand what the batch proves, it is not ready for public promotion.

### Wisdom

Every batch must include a boundary statement.

The boundary statement must say what the batch does **not** prove.

---

## 6. Replay / Repurpose / Rollback / Retail

### Replay

Can the object be re-run or re-queried and produce equivalent evidence?

Required status:

```text
replay_status = PENDING | PASS | FAIL
```

### Repurpose

Can the object be safely used in another lane?

Examples:

- DOJ public-record batch -> Computer Wisdom explainer,
- EAS UID batch -> JOY witness receipt,
- Render probe -> Grafana evidence panel,
- Zora object -> retail/public education surface.

Repurpose requires a new metadata envelope and a new boundary statement.

### Rollback

Can the object be reverted without corrupting truth state?

Rollback rules:

- never delete receipts,
- supersede bad metadata with correction receipts,
- mark invalid joins as RED or YELLOW,
- preserve old hashes for audit.

### Retail

Retail/publication is allowed only after the object has a public explanation and a receipt boundary.

No product, post, Zora object, or paid surface may imply DOJ endorsement, agency confirmation, court finding, or official validation unless such proof is directly present.

---

## 7. Base Batch x DOJ Batch Gate

A joined Base/DOJ batch may advance only if:

```text
source_public_record_present = true
base_receipt_present = true
join_key_present = true
metadata_hash_present = true
boundary_statement_present = true
no_fake_green = true
```

If any item is false:

```text
truth_state = YELLOW_READY or RED
```

---

## 8. ALMS Integration

ALMS treats every batch as a replayable evidence object.

Minimum ALMS receipt fields:

```json
{
  "batch_id": null,
  "batch_family": "base_doj_join",
  "inputs": [],
  "normalized_metadata_hash": null,
  "replay_command": null,
  "replay_output_hash": null,
  "truth_state": "YELLOW_READY",
  "no_fake_green": true
}
```

---

## 9. Current Status

**Status:** DESIGN_CONTROL_COMMITTED  
**Truth State:** YELLOW_READY  
**Live DOJ Proof:** NOT PRESENT  
**Live Base Batch Join:** NOT PRESENT  
**Live Render Probe:** NOT PRESENT  
**Retail Promotion:** BLOCKED UNTIL RECEIPT  

---

## 10. Next Clean Move

Create the first batch receipt:

```text
_truth/base-doj-batches/receipts/BASE_DOJ_BATCH_001_METADATA_RECEIPT.json
```

The receipt must include one real Base object, one real public-record object, one explicit join key, and a SHA256SUMS file before any GREEN claim.
