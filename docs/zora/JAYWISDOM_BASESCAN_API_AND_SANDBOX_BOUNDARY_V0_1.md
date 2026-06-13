# JAYWISDOM_BASESCAN_API_AND_SANDBOX_BOUNDARY_V0_1

## STATUS: OPERATOR_PROVIDED_BOUNDARY_RECEIPT
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This receipt records the operator-provided boundary for fetching the first 50 `$JAYWISDOM` token transfers on Base.

It does not independently verify BaseScan's current developer API rate limits. It records the operational constraint and preserves the replay path without fabricating transfer rows.

## Token Target

```text
network=Base
contract=0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
replay_target=first_50_transfer_events
```

## Operator-Provided BaseScan API Boundary

```text
basescan_developer_api_free_key_rate_limit=5_calls_per_second_per_ip_reported
basescan_no_key_or_default_rate_limit=1_call_per_5_seconds_reported
basescan_rate_limit_error=Max rate limit reached
hard_daily_quota_documented=false_reported
primary_limit=per_second_throttle_reported
independent_verification_by_assistant=false
```

## Acceleration Path

For first-50 inception replay, the preferred path is:

```text
preferred_path=direct_public_base_rpc
expected_calls=1_to_2_getLogs_calls_or_chunked_equivalent
api_key_required=false_for_public_rpc
basescan_export_path=operator_manual_export_clean
```

## Sandbox Boundary

```text
sandbox_outbound_rpc=false
assistant_direct_basescan_fetch=false
assistant_direct_zora_fetch=false
no_fake_rows=true
no_green_revenue_claim=true
first50_unpopulated_until_operator_or_rpc_feed=true
```

## Local Execution Vector

Run locally with a public Base RPC URL:

```bash
python3 tools/replay/fetch_first_50_jaywisdom_transfers.py \
  --rpc-url https://your-base-rpc.example \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F \
  --from-block 0 \
  --limit 50 \
  --output docs/zora/fixtures/JAYWISDOM_first50_transfers.csv
```

Then validate:

```bash
BASE_RPC_URL=https://your-base-rpc.example \
python3 tools/replay/jaywisdom_inception_replay_validator.py \
  --csv docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
```

## Alternative Operator Export Path

```text
operator_downloads_basescan_csv=true
converter_maps_to_replay_schema=true
source_column=basescan_export
no_api_hit_required=true
```

```bash
python3 tools/replay/convert_basescan_to_jaywisdom.py \
  --input /path/to/basescan-token-transfer-export.csv \
  --output docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --decimals 18 \
  --source basescan_export
```

## Validation Targets After Feed Arrives

```text
timestamp_ordering=true
earliest_50_selection=true
value_raw_sum=true
value_formatted_sum=true
source_column_present=true
revenue_confirmed=false
chain_write=false
wallet_control=false
signing=false
broadcast=false
```

## Files Already Landed

```text
docs/zora/JAYWISDOM_TOKEN_AGENT_MANUAL_V0_1.md
docs/zora/JAYWISDOM_FIRST50_REPLAY_RUNBOOK_V0_1.md
docs/zora/fixtures/JAYWISDOM_inception_replay_first50_template.csv
tools/replay/convert_basescan_to_jaywisdom.py
tools/replay/fetch_first_50_jaywisdom_transfers.py
tools/replay/jaywisdom_inception_replay_validator.py
```

## Ruling

```text
BASESCAN_API_LIMITS = OPERATOR_PROVIDED_NOT_ASSISTANT_VERIFIED
SANDBOX_AIRGAP = ACTIVE
FIRST50_PIPELINE = PRIMED
FIRST50_ROWS = NOT_POPULATED
LOCAL_RPC_OR_OPERATOR_EXPORT = REQUIRED
REVENUE = NOT_CONFIRMED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
