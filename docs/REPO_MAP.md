# REPO MAP

## Top-Level

- `/README.md` — operator overview
- `/docs/` — GitHub Pages source, architecture, doctrine, map, public proof surfaces
- `/docs/proof/` — public HTML proof viewers served by GitHub Pages
- `/_truth/receipts/` — canonical receipt index, manifest, changelog, and attestation receipts
- `/_truth/receipts/index.json` — canonical receipt index used by proof viewers
- `/data/` — canonical outputs where present
- `/scripts/` — deterministic transforms where present
- `/agents/` — observer, validator, and automation experiments where present

## Current Public Proof Surfaces

- `docs/proof/computer-wisdom-public-proof.html` — public proof page
- `docs/proof/index.html` — receipt index viewer

GitHub Pages serves these under:

- `https://jsonwisdom.github.io/AL/proof/computer-wisdom-public-proof.html`
- `https://jsonwisdom.github.io/AL/proof/`

## Canonical Truth Layer

The current receipt layer is attestation-based.

Primary index:

- `_truth/receipts/index.json`

Supporting truth files include:

- `_truth/receipts/manifest.json`
- `_truth/receipts/CHANGELOG.md`
- `_truth/receipts/*.json`

Do not assume `receipts/NY-*.json` exists unless a future receipt audit proves it.

## System Layers

### Civic Proof

- Public proof pages in `docs/proof/`
- Human-readable verification surfaces
- Links into the canonical truth layer

### Constitutional Machine

- `_truth/receipts/index.json`
- attestation receipt JSON files
- `docs/DOCTRINE.md`
- `docs/ARCHITECTURE.md`

### Agent Infrastructure

- observers
- validators
- automation
- future scheduled replay jobs

## How to Navigate

1. Start at `README.md`
2. Read `docs/ARCHITECTURE.md`
3. Read `docs/DOCTRINE.md`
4. Open `_truth/receipts/index.json`
5. Follow each indexed receipt `path`
6. Check `docs/proof/` for human-readable proof surfaces

No ghost paths. No decorative receipts. The map follows the files that exist.
