# AL — Attestation Ledger

Public verifiable claims with cryptographic receipts.

## Authority

All authority resolves to:

- **Receipt index:** `_truth/receipts/index.json`
- **Public proof surface:** https://jsonwisdom.github.io/AL/proof/
- **Receipt viewer:** https://jsonwisdom.github.io/AL/proof/index.html

## Canonical Boundary

The canonical truth source for this repository is `_truth/receipts/index.json`.

Only receipts present in that index are authoritative AL claims. Public files in this repository are visible working surfaces, but visibility alone does not make a file canonical.

Experimental artifacts, draft receipts, epoch-chain files, and working documents are **not canon** unless they are explicitly indexed and replay-linked through `_truth/receipts/index.json`.

Epoch-chain artifacts do not assert public legitimacy claims unless the canonical index binds them as such.

## Meme MetaVerse / War Board

New public workflow surfaces:

- `docs/MEME_METAVERSE_DAILY_DOCKER_DOCKETS.md`
- `docs/specs/JAYS_MEME_RUBRIC_V1.md`
- `docs/specs/JAYS_WISDOM_WAR_BOARD_V0_2.md`

Core doctrine:

```text
The joke can fly. The receipt must land.
```

The War Board introduces provenance-aware meme governance:

- county-resolution vernacular records
- attestation-aware docketing
- collision-window inspection
- `JOINT_ORIGIN` status for synchronous independent emergence
- visible corrections and revocations
- anti-ghost-anchor enforcement

## Verification

Pick a receipt from `_truth/receipts/index.json`, open the referenced JSON, inspect `claim`, `algorithm`, `commitment`, `timestamp`, and `signature`. A claim is public only when the receipt is present, indexed, and replay-linked.

```bash
# Browse the index
cat _truth/receipts/index.json | jq '.index.receipts[] | {path, claims}'

# Verify a specific receipt
cat receipts/2025-04-10T08-30-00Z-attestation.json | jq '{claim, algorithm, timestamp, signature}'
```

## Structure

```txt
AL/
├── README.md
├── docs/
│   ├── proof/
│   ├── specs/
│   │   ├── JAYS_MEME_RUBRIC_V1.md
│   │   └── JAYS_WISDOM_WAR_BOARD_V0_2.md
│   ├── MEME_METAVERSE_DAILY_DOCKER_DOCKETS.md
│   ├── ARCHITECTURE.md
│   ├── DOCTRINE.md
│   └── REPO_MAP.md
├── _truth/
│   └── receipts/
├── receipts/
└── data/
```

## License

See repository metadata.
