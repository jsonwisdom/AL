# JOY_ZORA_BASESCAN_USER_READBACK_V0_1

## STATUS: USER_BASESCAN_READBACK_OBSERVED
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This receipt records a user-provided BaseScan readback for the JOY Zora transaction.

The assistant did not independently fetch the BaseScan page. Direct tool fetch failed, so this receipt is admitted only as user-supplied readback evidence.

## Transaction

```text
network=Base
transaction_hash=0x6f7862b61b9998238d70e2ce76ce03fc24c5a9f2404a8cbf87092510adfbd31a
status=Success
block=47285603
timestamp_utc=Jun-13-2026 02:22:33 PM +UTC
type=Account Abstraction Bundle
user_ops_count=1
```

## Reported Transaction Action

```text
action=Transfer
amount=0.000000000001
token=JOY: Proof, Not Promises
recipient=jaywisdom.base.eth
```

## Reported Parties

```text
from=0xAF2bFB6b69Dfe6eFd257fE8cD694175156a23812
interacted_with=0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789
interacted_with_label=Entry Point 0.6.0
reported_token_sender=0x829AdfEd...cAef055E
reported_token_recipient=jaywisdom.base.eth
```

## Reported Token Transfer

```text
token_standard=ERC-20
token_display=JOY: Proof, Not Promises
amount=0.000000000001
value_eth=0
```

## Reported Fees

```text
transaction_fee_eth=0.000001028288031899
transaction_fee_usd=0.001726
gas_price_gwei=0.006
internal_transfer_from=Entry Point 0.6.0
internal_transfer_to=0xAF2bFB6b...156a23812
internal_transfer_amount_eth=0.000001030512
```

## Verification Boundary

```text
basescan_url_presented=true
basescan_user_readback_presented=true
assistant_direct_basescan_fetch=false
assistant_independent_verification=false
screenshot_or_user_readback_observed=true
```

## What This Supports

```text
JOY_ZORA_ARTIFACT = LIVE_SCREENSHOT_OBSERVED
BASE_TX_SUCCESS = USER_BASESCAN_READBACK_REPORTED_SUCCESS
BASE_BLOCK = USER_BASESCAN_READBACK_REPORTED_47285603
TOKEN_TRANSFER = USER_BASESCAN_READBACK_REPORTED_JOY_TO_JAYWISDOM_BASE_ETH
```

## What This Does Not Support

```text
revenue_confirmed=false
creator_earnings_confirmed=false
contract_code_verified_by_assistant=false
market_cap_verified_by_assistant=false
holder_count_verified_by_assistant=false
authority_claimed=false
```

## Ruling

```text
TX_RECEIPT_STRENGTH = USER_BASESCAN_READBACK
ASSISTANT_DIRECT_READBACK = FALSE
TX_SUCCESS = REPORTED_SUCCESS
TOKEN_MOVE = REPORTED_TRUE
REVENUE = NOT_CONFIRMED
CHAIN_WRITE_BY_ASSISTANT = FALSE
WALLET_CONTROL_BY_ASSISTANT = FALSE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
