# Reflection Authority Rules

## Controlling Rule
The M2 verification receipt records successful public machine replay only.
It does **not** authorize:
- signing
- ENS mutation
- promotion of any artifact beyond the published, machine-verifiable state

## Bound Identifiers
- directory_cid: `bafybeieetilehphhd25bp2rcyukupp7s5eu2exiyvzj7uxphiy4xzxi3kq`
- graph-node.schema.json → bafkreid2s37uwee6nmvzakdgd6td5lnfkuft5bizjt3mijusw4lbx6j2ae (3291 bytes)
- graph-event.schema.json → bafkreifkhjhsnn6aaln55lqqjpzvzurlcef4enhn7i2c4ryxk7rb6pjytu (8294 bytes)
- graphService.ts → bafkreiepu2wypttib4qxsbhfcobe3q2zphbjspi2pshqmtkc6svgbcxbmm (54207 bytes)

## Placement
Canonical tree under `Reflection/`:
- schemas/
- server/src/services/
- ledger/receipts/
- ledger/events/
- docs/
- (workflow lives at repository root `.github/workflows/`)

## Workflow Constraint
GitHub Actions workflows execute only from the repository-level `.github/workflows/` directory.
