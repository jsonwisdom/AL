# Frost Archive Status

## Directory Rule

AL is the source of truth.

All Frost work lives under:

- `frost-mock-emitter/`

Do not use a separate home-level `~/frost-mock-emitter` directory.

## On-chain EAS Artifacts

Schema #1570:

`0x70ddc1203b381b4c90cb10da80db94223af35e621399583b324ca735086d95f9`

Bootstrap Attestation #0001:

`0x809cf90cb2f31451ead1f916ca4e93a4f97f7ca830ec53609ac02cdc5135eaa6`

Simulation Attestation #0002:

`0xa63d9920373d1cbd565c47adb0475fddaa9f73ce703715bf3c4a46351503a8c2`

## Current State

- BASE_MAINNET_SCHEMA_1570 = GREEN
- BASE_MAINNET_BOOTSTRAP_0001 = GREEN
- BASE_MAINNET_SIMULATION_0002 = GREEN
- MOCK_EMITTER_FLOW = PREPARED
- VERIFY_RECEIPT_TRUE = PENDING
- FIRST_REAL_LIQUIDITY_RECEIPT = HOLD

## Boundary Rules

- PREPARED is not EXECUTED
- EXECUTED is not VERIFIED
- VERIFIED is not LIQUIDITY

No mainnet liquidity claim may be made until a real PoolManager/v4 liquidity event exists.

## Prepared Manifest Boundary

Committed manifest path:

- `frost-mock-emitter/manifest_prepared.json`

Current committed manifest timestamp:

- `1780993154`

Current committed prepared root:

- `0x570b33f52d3a5bf956905aa6cb34b131f975b1706ff1798a43b334aa8a98aae7`

Older or local-only roots are not active unless the matching manifest is committed at `frost-mock-emitter/manifest_prepared.json`.

Additional boundary rule:

- A prepared root is current only if it matches the committed manifest.
