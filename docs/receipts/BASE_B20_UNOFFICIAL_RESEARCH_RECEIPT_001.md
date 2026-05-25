# BASE B20 Unofficial Research Receipt 001

**Repository of record:** `jsonwisdom/AL`  
**External observed repository:** `jsonwisdom/base`  
**External draft PR:** `https://github.com/jsonwisdom/base/pull/1`  
**External observation branch:** `jay/b20-precompile-audit-001`  
**Classification:** `UNOFFICIAL_RESEARCH_RECEIPT`  
**Mode:** `OBSERVATION_ONLY_NO_CODE_MUTATION`  

---

## 1. Purpose

This AL receipt records the methodology boundary for the Base B20 precompile observation work.

The Base fork preserves repository-visible evidence. AL preserves the constitutional method: distinguish code evidence from official instruction, prevent unsupported escalation, and keep claims replayable.

---

## 2. Evidence Boundary

Allowed claim:

```txt
The copied Base repository contains repository-visible B20-related native precompile code paths and benchmark references at the observed commit lineage.
```

Forbidden claims without separate public evidence:

```txt
Base has published official B20 instructions.
Base has published a public B20 user manual.
B20 is live on Base mainnet.
B20 is supported for public production use.
Stablecoin or Security variants are launched products.
Benchmark presence proves roadmap intent.
A copied fork grants authority over Base protocol direction.
```

---

## 3. Code Evidence Is Not Instruction

```txt
CODE_PATH != OFFICIAL_DOCUMENTATION
BENCHMARK != PRODUCTION_STATUS
SYMBOL_NAME != ROADMAP_INTENT
FORK_COPY != PROTOCOL_AUTHORITY
```

---

## 4. Cross-Repo Structure

```txt
jsonwisdom/base
  -> preserves observed Base repository state and B20 receipt files

jsonwisdom/AL
  -> preserves the audit methodology and claim-boundary rule
```

This avoids copying Base source into AL while still preserving the research boundary in the AL constitutional archive.

---

## 5. AL Alignment

This receipt supports the Glass-Box Republic posture: contestability requires visible evidence, clear claim boundaries, and no authority cosplay.

Observed code can be reviewed. Official status must be separately proven.

---

## 6. Receipt State

```json
{
  "receipt_id": "BASE_B20_UNOFFICIAL_RESEARCH_RECEIPT_001",
  "repository_of_record": "jsonwisdom/AL",
  "external_observed_repository": "jsonwisdom/base",
  "external_pr": "https://github.com/jsonwisdom/base/pull/1",
  "classification": "UNOFFICIAL_RESEARCH_RECEIPT",
  "mode": "OBSERVATION_ONLY",
  "source_code_mutation": false,
  "official_base_documentation_claim": false,
  "official_base_manual_claim": false,
  "production_status_claim": false,
  "status": "SEALED_AS_METHOD_RECEIPT"
}
```

Proof over narrative. Code evidence is not an instruction manual. ⚙️🧾
