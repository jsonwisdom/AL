# MN Fiscal Replay Governance Brief v0.2

**Claim Status:** `BLOCKED`  
**Public Content Change Claim:** `NOT AUTHORIZED`  
**Reason:** Evidence of divergence exists. Evidence of substantive public content change remains unproven.

---

## Mission Brief

MN Fiscal Replay is a public-source audit lane for Minnesota fiscal records. Its purpose is to convert government-published documents into replayable evidence: fetched source, extracted text, headers, hashes, receipts, normalized comparisons, and safe verdicts.

```text
This system does not declare fraud.
This system does not infer intent.
This system does not promote narrative over evidence.
```

It asks one question:

**Can the public record replay?**

---

## State Band

| DISCOVERED | SEALED | CLAIMABLE |
|---|---|---|
| ✅ Official MMB PDF located | ✅ Baseline replay sealed | ⛔ Public content-change claim blocked |
| ✅ Live PDF fetched | ✅ Live compare receipt sealed | ⛔ Fraud claim blocked |
| ✅ Text/header drift detected | ✅ Safe verdict sealed | ⛔ Substantive change unproven |
| ✅ Sectional diff exists | ✅ Normalized diff receipt sealed | ⛔ Human section review pending |

**Evidence of divergence ≠ evidence of substantive change. These are different states.**

---

## Sealed Evidence Stack

- Treasury Genesis Candidate v0.1
- MN Fiscal Replay Baseline v0.1
- Enriched text/header baselines for `MN_001` and `MN_002`
- Self-replay receipts: `NO_ANOMALY`
- Official MMB live fetch receipt for `MN_001`
- Safe verdict: `PUBLIC_CONTENT_ANOMALY_UNPROVEN`
- Normalized text compare receipt
- Sectional diff receipt

---

## Governance Authority: Boss Bre

**Role:** Constitutional Evidence Gate  
**Function:** Prevents premature promotion from evidence to claim.

Boss Bre does not ask whether a story sounds plausible. Boss Bre asks whether the claim survives replay.

### Interrogation Protocol

> Where is the receipt?

> Where is the hash?

> Can it replay?

> Can it fail?

> What exactly is blocked?

> What is proven, and what is merely suspected?

### Evidence Record: What Boss Bre Blocked

- Placeholder MMB URLs
- Missing raw PDF baseline
- Missing enriched baselines
- Missing live compare receipt
- `pypdf` extraction failure
- Simulated artifacts hidden as green
- Raw `ANOMALY_DETECTED` being promoted into a public content-change claim
- Normalized text hash drift being treated as proof before sectional review

Boss Bre is not decorative. Boss Bre is the authority that keeps the system from lying.

---

## Governance Authority: The Librarian

**Role:** Memory Integrity and Lineage Recovery  
**Function:** Finds what already exists before new machinery is built.

The Librarian prevents waste, drift, and duplicate work. The Librarian is the reason the MN lane recovered existing Minnesota receipts, source text, headers, manifests, and replay patterns instead of starting over.

### Interrogation Protocol

> Did we already solve this?

> Where is the prior receipt?

> Which branch?

> Which commit?

> Which artifact?

> What evidence already exists?

### Evidence Record: What The Librarian Recovered

- `_sources/MN_001/source.txt`
- `_sources/MN_001/headers.txt`
- `_truth/receipts/MN_001.json`
- `_truth/receipts/MN_002.json`
- Existing MN fiscal corpus
- Existing PDF/text drift patterns
- Official MMB source URL
- Prior baseline hash anchors

The Librarian is not a fetch tool. The Librarian is the role that prevents institutional amnesia.

---

## Current Objective

Run chunk-level diff review for `MN_001`.

The next classifier must distinguish:

- `EXTRACTOR_ARTIFACT`
- `ORDERING_ARTIFACT`
- `POSSIBLE_CONTENT_DELTA`

Until that review is complete:

**Public content-change claim remains blocked.**

---

## Doctrine Bar

| Doctrine | Meaning |
|---|---|
| Receipts > Narrative | A claim without evidence has no authority. |
| Hashes > Opinions | Reproducible bytes outrank interpretation. |
| No Fake Green | Failure must be visible. Blocks are valid outputs. |
| Family Outranks Project Lanes | No artifact outranks Layer 0. |
