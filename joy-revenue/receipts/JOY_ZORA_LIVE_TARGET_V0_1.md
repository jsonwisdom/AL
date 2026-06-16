# JOY_ZORA_LIVE_TARGET_V0_1

## STATUS: CANONICAL_TARGET_FIXTURE
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This fixture indexes the live JOY Zora target inside the repository so the artifact can be discovered by contract, Zora URL, X post, and transaction hash.

It bridges the externally visible Zora/Base artifact to the internal GitHub archive without invoking external APIs, chain writes, wallet authority, signer authority, or revenue claims.

## Canonical Target

```text
title=JOY: Proof, Not Promises
platform=Zora
network=Base
profile=jaywisdom
contract=0x71f45dac7f2b0d5a5e7974972321a9d6286057ca
zora_url=https://zora.co/coin/base:0x71f45dac7f2b0d5a5e7974972321a9d6286057ca
x_post_url=https://x.com/jaywisdom12/status/2065808482549330034
base_tx_hash=0x6f7862b61b9998238d70e2ce76ce03fc24c5a9f2404a8cbf87092510adfbd31a
artifact=Goblin JOY cover art
```

## Observed Inputs

```text
zora_url_presented=true
zora_screenshot_observed=true
x_post_url_presented=true
x_post_screenshot_observed=true
basescan_user_readback_observed=true
github_only_archive=true
```

## Supporting Receipts

```text
joy-revenue/receipts/JOY_ZORA_BASESCAN_USER_READBACK_V0_1.md
joy-revenue/receipts/JOY_REVENUE_REPLAY_V0_1.md
joy-revenue/receipts/GITHUB_ONLY_REVENUE_STACK_V0_1.md
```

## Revenue Boundary

```text
market_surface=observed_from_screenshot
token_move=user_readback_reported_true
creator_earnings=unproven
net_profit=unproven
withdrawable_balance=unproven
revenue_status=not_confirmed
```

## Verification Boundary

```text
assistant_direct_zora_fetch=false
assistant_direct_basescan_fetch=false
assistant_independent_contract_verification=false
user_readback_admitted=true
screenshot_readback_admitted=true
```

## Non-Capabilities

```text
chain_write=false
wallet_control=false
signing=false
broadcast=false
workflow_dispatch=false
revenue_claim=false
authority=false
no_fake_green=true
```

## Plain Meaning

The JOY artifact is indexed in the repo as a live Zora/Base target based on provided links, screenshots, and user readbacks.

This fixture makes the target findable by repository search and machine indexing. It does not claim creator revenue, holder count, market cap verification, or assistant-independent contract verification.

## CRO Archive Note

```text
signal_core=repo_audit_found_fixture_gap
acceleration_path=canonical_target_fixture
failure_mode_dodged=fragmented_proofs
next_reaudit=search_full_contract_and_zora_url
```

## Ruling

```text
CANONICAL_JOY_ZORA_TARGET = LANDED
FULL_CONTRACT_INDEXED = TRUE
ZORA_URL_INDEXED = TRUE
X_POST_INDEXED = TRUE
BASE_TX_HASH_INDEXED = TRUE
REVENUE_STATUS = NOT_CONFIRMED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
