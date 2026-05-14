# AL — Attestation Ledger

Public verifiable claims with cryptographic receipts.

## Authority

All authority resolves to:

- **Receipt index:** `_truth/receipts/index.json`
- **Public proof surface:** https://jsonwisdom.github.io/AL/proof/
- **Receipt viewer:** https://jsonwisdom.github.io/AL/proof/index.html

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

## Baseline Governance

Baselines in this repository are not test fixtures.
Baselines are constitutional memory: the byte-stable record of expected system behavior.

They define what is trusted, what is allowed, and what constitutes drift.
All runners (calibration, capture, curriculum) are bound to these baselines.

The governance chain is:

manifest → check → drift receipt → approval evidence → human update

No step is implicit.
No step is automated.
No step is skipped.

### Manifest

The manifest is the only lawful registry of baseline pairs:

`reports/baselines/manifest_v1.json`

If a runner is not listed in the manifest, it does not exist.
CI and the governance CLI must read only this manifest.

### Baseline Drift Gate (CI)

The drift gate lives at:

`.github/workflows/baseline-drift.yml`

CI responsibilities:

- witness drift
- preserve drift evidence
- fail the build on drift

CI may not approve drift.
CI may not update baselines.
CI may not infer runners or discover files.

### Operator Commands

All governance actions are performed through the Baseline Governance CLI:

`scripts/baseline_governance.ts`

#### Status

```bash
npx ts-node scripts/baseline_governance.ts status reports/baselines/manifest_v1.json
```

#### Check

```bash
npx ts-node scripts/baseline_governance.ts check reports/baselines/manifest_v1.json
```

#### Approve Update (Evidence Only)

```bash
npx ts-node scripts/baseline_governance.ts approve-update \
  calibration \
  reports/calibration/latest.json \
  reports/baselines/calibration/baseline.json \
  --drift <driftReceiptHash> \
  --commit <commitHash> \
  --reason "<reason>" \
  --reviewer "<reviewer>"
```

Missing any required fields makes the update invalid.

### Manual Baseline Update Rule

A baseline may be replaced only when:

1. A drift receipt exists.
2. The operator has reviewed both canonical receipts.
3. An approval evidence block has been generated.
4. A human reviewer signs off.
5. CI re-runs and confirms stability.

There are no other lawful paths.

### Prohibited CI Behavior

- ❌ Auto-updating baselines
- ❌ Regenerating baselines
- ❌ Mutating baselines in CI
- ❌ Accepting drift without evidence
- ❌ Discovering runners or files
- ❌ Inferring baseline locations
- ❌ Silent absolution

Baselines change only through explicit operator action.

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
