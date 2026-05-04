# NY ALMS Climate-Economic Stack

![PORTABLE_TRUTH_LIVE](https://img.shields.io/badge/PORTABLE_TRUTH-LIVE-black?style=for-the-badge)

**Public Proof:** https://jsonwisdom.github.io/AL/computer-wisdom-public-proof.html

**Status:** Verified sparse climate + full income coverage for NY counties

## What This Is

A deterministic, auditable data pipeline that produces:
- Median household income for all 62 NY counties (ACS 5-year)
- Climate observations for 4 counties with GSOD stations (2020-2024)
- Temperature trends and extreme event metrics for station counties
- Explicit guardrails preventing overclaim

## Receipt Chain

| Receipt | What | Coverage |
|---------|------|----------|
| NY-001 | County FIPS | 62/62 |
| NY-003 | ACS income | 62/62 |
| NY-004 | GSOD 2024 climate | 6/62 |
| NY-007B | GSOD trends | 4/62 |
| NY-010 | Extreme events | 4/62 |
| NY-011S | Sparse validation | 4/62 |
| NY-012 | Methodology note | N/A |

## What This Does Not Claim

- No statewide climate validation
- No risk atlas or hazard map
- No attribution or causality
- No interpolation to uncovered counties

## Guardrails

- $0 / BigQuery-only
- Deterministic receipts with hashes
- No simulated data
- Honest sparsity documented

## Data Gaps (If Expanding)

- PRISM external download (FTP 404)
- ERA5 unavailable in public BigQuery
- Additional station mapping needed

---

*Receipts verified on GitHub*
*Last updated: May 2026*
