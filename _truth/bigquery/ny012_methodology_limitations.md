# NY ALMS Climate-Economic Stack: Methodology & Limitations

## Receipt Chain (Locked)

| Receipt | Artifact | Coverage | Status |
|---------|----------|----------|--------|
| NY-001 | NY county FIPS spine | 62/62 | ✅ Locked |
| NY-003 | ACS 5-year median income | 62/62 | ✅ Locked |
| NY-004 | NOAA GSOD 2024 climate | 6/62 | ✅ Locked |
| NY-007B | GSOD 2020-2024 trends | 4/62 | ✅ Locked |
| NY-010 | GSOD 2024 extreme events | 4/62 | ✅ Locked |
| NY-011S | Sparse validation report | 4/62 | ✅ Locked |

## What Is Proven

- **Geographic spine:** All 62 NY counties have FIPS codes
- **Income data:** All 62 NY counties have ACS 5-year median income estimates
- **Station climate data:** 4 counties (Albany, Erie, Franklin, Suffolk) have reliable GSOD station data for 2020-2024
- **Climate trends:** These 4 counties show measurable temperature trends (mean +3.08°F/decade) over 2020-2024
- **Extreme events:** Heavy rain days and composite extreme scores calculated for station counties

## What Is Sparse

- **Climate coverage:** Only 4 of 62 counties have station-derived climate data
- **Validation:** Only these 4 counties have validation between annual and extreme metrics
- **Trend confidence:** 5-year window (2020-2024) is too short for climate normals

## What Is Intentionally Not Claimed

- No statewide climate validation
- No statewide risk atlas or hazard map
- No causality, health impact, disaster, or economic-loss attribution
- No interpolation to uncovered counties
- No PRISM or gridded climate comparison
- No ERA5 reanalysis (dataset unavailable in public BigQuery)

## Data Gaps

- **PRISM normals:** External download failed (FTP 404); requires updated source
- **ERA5 reanalysis:** Not available in public BigQuery
- **Additional stations:** Many mapped stations have no 2024 data

## Next Data Requirements (If Expanding)

1. Working PRISM FTP access or alternative gridded climate source
2. GHCN-D station ID mapping for NY stations
3. Multi-year GSOD query automation (union across tables)
4. Spatial interpolation methods (IDW, kriging) with uncertainty bounds

## Policy Guardrails

- **$0 / BigQuery-only** maintained (PRISM would be exception)
- **No vertex AI / compute engine**
- **Deterministic receipts only** (no simulated data)
- **Honest sparsity** (no claims beyond measured coverage)

---

*Last updated: May 2026*
*Receipt chain verified on GitHub*
