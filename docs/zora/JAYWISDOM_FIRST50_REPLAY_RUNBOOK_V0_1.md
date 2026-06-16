# JAYWISDOM_FIRST50_REPLAY_RUNBOOK_V0_1

## STATUS: FIRST50_REPLAY_READY
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This runbook documents two read-only ways to populate the first 50 `$JAYWISDOM` token transfers on Base.

## Token Target

```text
network=Base
contract=0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
```

## Files

```text
docs/zora/fixtures/JAYWISDOM_inception_replay_first50_template.csv
tools/replay/convert_basescan_to_jaywisdom.py
tools/replay/fetch_first_50_jaywisdom_transfers.py
tools/replay/jaywisdom_inception_replay_validator.py
```

## Option A — Operator BaseScan Export

Use this when the operator can download the CSV manually from the explorer UI.

```bash
python3 tools/replay/convert_basescan_to_jaywisdom.py \
  --input /path/to/basescan-token-transfer-export.csv \
  --output docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --decimals 18 \
  --source basescan_export
```

Then validate:

```bash
python3 tools/replay/jaywisdom_inception_replay_validator.py \
  --csv docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
```

## Option B — Read-Only RPC Fetch

Use this when the operator supplies a public Base RPC URL.

```bash
python3 tools/replay/fetch_first_50_jaywisdom_transfers.py \
  --rpc-url https://your-base-rpc.example \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F \
  --from-block 0 \
  --limit 50 \
  --output docs/zora/fixtures/JAYWISDOM_first50_transfers.csv
```

Then validate with optional supply check:

```bash
BASE_RPC_URL=https://your-base-rpc.example \
python3 tools/replay/jaywisdom_inception_replay_validator.py \
  --csv docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
```

## Boundary

```text
BaseScan automated crawling=false
operator_export_allowed=true
rpc_getLogs_allowed=true
eth_call_totalSupply_allowed=true
chain_write=false
wallet_control=false
signing=false
broadcast=false
revenue_confirmed=false
authority=false
no_fake_green=true
```

## Ruling

```text
FIRST50_TEMPLATE = LANDED
BASESCAN_CONVERTER = LANDED
RPC_FETCHER = LANDED
VALIDATOR = LANDED
INCEPTION_ROWS = NOT_POPULATED_UNTIL_OPERATOR_EXPORT_OR_RPC_RUN
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
