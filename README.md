# AL — Attestation Ledger

Public verifiable claims with cryptographic receipts.

## Authority

All authority resolves to:

- **Receipt index:** `_truth/receipts/index.json`
- **Public proof surface:** https://jsonwisdom.github.io/AL/proof/
- **Receipt viewer:** https://jsonwisdom.github.io/AL/proof/index.html

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
├── README.md              # This file
├── docs/
│   ├── proof/             # Public proof surfaces (GitHub Pages)
│   │   ├── computer-wisdom-public-proof.html
│   │   └── index.html     # Receipt viewer
│   ├── ARCHITECTURE.md    # System design
│   ├── DOCTRINE.md        # Constitutional rules
│   └── REPO_MAP.md        # File inventory
├── _truth/
│   └── receipts/
│       └── index.json     # Canonical receipt index
├── receipts/              # Individual attestation receipts, where present
└── data/                  # Legacy/public module outputs
    └── ny/                # NY climate-economic proof surface, where present
```

## Legacy/public module

NY climate-economic proof surface:

- Coverage: 62/62 counties (median household income)
- Climate observation: sparse station counties only
- Proofs archived under `data/ny/`, where present

All NY claims are attested via receipts in `_truth/receipts/index.json`.

## License

See repository metadata.
