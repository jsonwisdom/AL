# JAYWISDOM_TOKEN_AGENT_MANUAL_V0_1

## STATUS: AGENT_MANUAL_READ_ONLY
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This manual defines the read-only agent workflow for replaying the inception and transfer history of the `$JAYWISDOM` token on Base.

It does not claim live chain verification by itself. BaseScan and Zora may block automated browsing, so the workflow depends on direct operator export, direct pasted fields, screenshots, or a configured public RPC read.

## Token Target

```text
token_name=$JAYWISDOM
network=Base
contract=0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
source_status=operator_presented_existing_repo_registry
```

## Existing Repo Registry Reference

The repo contains an older EVM address registry entry for a JAYWISDOM creator coin. This manual does not overwrite that registry. It defines a replay method for validating a CSV transfer export against token supply evidence.

## What The Agent May Do

```text
read_csv=true
validate_required_headers=true
summarize_earliest_row=true
summarize_latest_row=true
sum_transfer_values=true
classify_source_column=true
optionally_call_totalSupply_via_public_rpc=true
write_json_receipt_to_stdout=true
```

## What The Agent Must Not Do

```text
chain_write=false
wallet_control=false
signing=false
broadcast=false
private_key_handling=false
claim_revenue=false
claim_holder_count_without_index=false
fabricate_missing_rows=false
invent_inception_event=false
```

## Required CSV Headers

```text
blockNumber,timestamp_utc,txHash,from_address,to_address,value_raw,value_formatted,method,source
```

## Operator Workflow

1. Open the token page in a normal browser.
2. Export the Transfers CSV from the explorer UI.
3. Paste or normalize rows into the template starting at row 2.
4. Set `source` to the evidence origin, for example `BaseScan Export`.
5. Run the validator.
6. Store the validator JSON output as the replay receipt.

## Replay Test

The validator checks:

```text
required_headers_present=true
rows_present=true
earliest_row_selected_by_block_then_timestamp=true
latest_row_selected_by_block_then_timestamp=true
value_raw_sum=computed_from_csv
value_formatted_sum=computed_from_csv
rpc_total_supply_optional=true
csv_total_vs_rpc_total=only_if_rpc_configured
```

## Public RPC Optional Check

The validator may call ERC-20 `totalSupply()` using a public Base RPC URL supplied by the operator:

```bash
BASE_RPC_URL=https://your-base-rpc.example \
python3 tools/replay/jaywisdom_inception_replay_validator.py \
  --csv docs/zora/fixtures/JAYWISDOM_inception_replay_template.csv \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
```

If no RPC URL is supplied, the validator remains CSV-only and does not claim on-chain confirmation.

## Boundary Ruling

```text
JAYWISDOM_INCEPTION_REPLAY = TEMPLATE_AND_VALIDATOR_READY
CSV_ROWS = OPERATOR_SUPPLIED_REQUIRED
RPC_TOTAL_SUPPLY = OPTIONAL_READ_ONLY
INCEPTION_ANCHOR = UNCONFIRMED_UNTIL_ROWS_EXIST
REVENUE = NOT_CONFIRMED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
