# ALMS RUN RECEIPT — 001

**Date:** 2026-05-04  
**Operator:** Jay Wisdom  
**Verifier:** `scripts/verify/alms_pdf_text_drift_verifier.py`  
**Canonical root:** `e1fbf116972f368c13fab67ef479e0b839b080ff`  
**Seal commit:** `afbbd791e66bc78d27e0fc4a329eb2e8bf54780a`

## Source Document

- **Name:** DOJ/NSD April 5, 2024 Joint Letter — Section 702 Reauthorization
- **Source URL:** https://www.justice.gov/nsd/media/1346981/dl?inline
- **Local PDF path expected for replay:** `_truth/receipts/fisa702.pdf`
- **Local extracted text path expected for replay:** `_truth/receipts/fisa702_extracted.txt`

## Extraction Method

- **Tool:** `pdftotext` / Poppler-style extraction
- **Command:**

```bash
pdftotext -layout _truth/receipts/fisa702.pdf _truth/receipts/fisa702_extracted.txt
```

## Verification Command

```bash
python3 scripts/verify/alms_pdf_text_drift_verifier.py \
  --pdf _truth/receipts/fisa702.pdf \
  --text _truth/receipts/fisa702_extracted.txt
```

## Reported Verification Output

```text
ALMS PDF/TEXT DRIFT VERIFIER
PDF: fisa702.pdf -> [stable byte hash]
Extracted: fisa702_extracted.txt -> [different text hash]
VERDICT: HASH_MISMATCH
STATUS: Byte drift confirmed — different artifacts.
```

## Diff Summary

| Location | PDF Source | Extracted Text |
|---|---|---|
| Page 1 | `refonns` | `reforms` or vice versa |
| Page 1 | `ce1iifications` | `certifications` |
| Page 1 | `FI SC-approved` | `FISC-approved` |
| Page 2 | `infonnation` | `information` |

Full diff expected at `_truth/receipts/fisa702_diff.txt` when the local artifacts are committed.

## Claim Boundary

**HASH_MISMATCH proves byte/artifact drift only.**  
Intent, narrative tampering, and malice require independent evidence outside this verifier.

## Doctrine

**Proof > vibes. Run the receipt.**

## Replay Notes

This receipt records the reported Run 001 summary and the replay command. The PDF bytes and extracted text artifact should be committed separately before this run is treated as fully self-contained inside the repository.

## Signature

- **Observer:** `jsonwisdom/observer_mode`
- **Seal:** `afbbd791e66bc78d27e0fc4a329eb2e8bf54780a`
- **Timestamp:** `2026-05-05T04:55:00Z`
