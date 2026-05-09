# AL — Audit Ledger / ALMS Verification Machine

![PORTABLE_TRUTH_LIVE](https://img.shields.io/badge/PORTABLE_TRUTH-LIVE-black?style=for-the-badge)
![VERIFY_OVER_NARRATIVE](https://img.shields.io/badge/VERIFY-%3E%20NARRATIVE-blue?style=for-the-badge)

**Public Proof:** https://jsonwisdom.github.io/AL/computer-wisdom-public-proof.html

**Status:** active research repository for deterministic receipts, civic verification, public proof pages, and bounded data pipelines.

---

## Purpose

AL is a zero-trust civic verification repository.

Its job is to turn claims, datasets, documents, and public-facing proof pages into replayable artifacts that can be checked by humans, courts, agents, and machines without relying on narrative authority.

The repository is not one single app. It is a chain-of-custody workspace for:

- deterministic receipt generation
- public proof surfaces
- data pipeline verification
- legal / civic doctrine
- observer and agent workflows
- contract and attestation experiments
- studio-facing explanations for public adoption

Core principle:

> **Truth should be testable, replayable, and bounded by receipts.**

---

## Current Public Module

### NY ALMS Climate-Economic Stack

A deterministic, auditable data pipeline that currently produces:

- median household income for all 62 NY counties using ACS 5-year data
- climate observations for counties with GSOD station coverage
- temperature trend and extreme-event metrics for covered station counties
- explicit guardrails preventing statewide overclaim

### Current Claim Boundary

The NY module is **sparse climate coverage + full income coverage**.

It does **not** claim statewide climate validation, hazard mapping, attribution, causality, or interpolation to uncovered counties.

---

## Repository Map

| Path | Purpose |
|---|---|
| `.github/workflows/` | CI gates, safety checks, automated verification |
| `_truth/` | truth receipts, security reports, anchor records |
| `agents/` | agent-facing workflows and operating patterns |
| `claims/` | claim records and structured assertion material |
| `contracts/` | protocol / attestation / on-chain experiment layer |
| `data/` | source and derived data artifacts |
| `docs/` | technical, civic, legal, and operational doctrine |
| `experiments/` | research prototypes and bounded experiments |
| `frames/` | visual / state framing artifacts |
| `law/` | legal and governance-oriented materials |
| `normalize/` | normalization and canonicalization support |
| `observers/` | independent observer / verifier surfaces |
| `qubo/` | optimization / modeling experiments |
| `receipts/` | replayable receipt chain outputs |
| `script/` / `scripts/` | execution, verification, and build scripts |
| `site/` | public web surfaces |
| `sources/` | source-specific intake material |
| `src/` | implementation code |
| `studio/` | public education, publishing, and adoption layer |
| `tools/` | utility tooling |
| `validators/` | signature / validation implementations |
| `watchers/` | monitoring and watcher experiments |

---

## Receipt Chain: NY Module

| Receipt | What | Coverage |
|---|---|---|
| NY-001 | County FIPS | 62/62 |
| NY-003 | ACS income | 62/62 |
| NY-004 | GSOD 2024 climate | sparse station coverage |
| NY-007B | GSOD trends | station counties |
| NY-010 | Extreme events | station counties |
| NY-011S | Sparse validation | station counties |
| NY-012 | Methodology note | claim boundary |

---

## Guardrails

This repo should preserve these rules:

- no simulated data presented as observed data
- no statewide claim from sparse station coverage
- no receipt without reproducible inputs or declared limitations
- no secret material in receipts
- no narrative upgrade without machine-checkable proof
- no public proof page that overstates what the receipt chain proves

---

## Operating Doctrine

AL follows a simple verification loop:

1. **Intake** — collect source material.
2. **Normalize** — convert inputs into canonical, bounded structures.
3. **Generate** — produce receipt artifacts and public proof surfaces.
4. **Verify** — check hashes, coverage, limits, and replayability.
5. **Publish** — expose only what the receipt chain can support.

---

## What This Repo Is Not

- not a general dashboard repo
- not a vibes-based policy analysis folder
- not a finished statewide climate atlas
- not a replacement for source data providers
- not a claim of causality unless a receipt explicitly proves that scope

---

## Public Identity

Operator / research identity: **Jay Wisdom / JSONWisdom**

Working frame: **Jay's Wisdom of Zero Trust**

Guiding idea:

> **Build systems where truth can be tested, not just asserted.** ⚙️🧾

---

*Last updated: May 2026*
