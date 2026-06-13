# JAYWISDOM_FIRST50_OPERATOR_EXECUTION_PACKET_V0_1

## STATUS: LOCAL_RUNBOOK_ONLY
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This packet is a local runbook for collecting **up to 50 real** `$JAYWISDOM` ERC-20 `Transfer` events on Base.

It is not a live node, not a classifier, not a validated chain result, and not a revenue receipt.

No fake rows. No padded rows. No assistant-side RPC claim. No BaseScan crawling claim. No revenue claim.

## Target

```text
network=Base
contract=0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
output_csv=docs/zora/fixtures/JAYWISDOM_first50_transfers.csv
validator=tools/replay/jaywisdom_inception_replay_validator.py
```

## Critical Row Rule

```text
requested_limit=50
csv_rows=min(50, actual_real_transfer_event_count)
padding_allowed=false
placeholder_rows_allowed=false
```

If the token has only 2 real `Transfer` events, the CSV must contain exactly 2 rows, not 50.

Shortfall is recorded as validator or receipt metadata, not as fake CSV rows.

## Operator-Reported Current Claim

The following is operator-reported until backed by a CSV export, screenshot, RPC output, or explorer/API evidence:

```text
reported_transfer_event_count=2
reported_holders=92
reported_total_supply=1000000000
reported_decimals=18
reported_contract_type=CreatorCoin proxy
assistant_independent_verification=false
```

## Path A — Public Base RPC

Use this when the operator has a public Base RPC URL.

```bash
set -e

cd ~/AL 2>/dev/null || cd ~/COMPUTERWISDOM/AL 2>/dev/null || cd ~/COMPUTERWISDOM/JOY 2>/dev/null || pwd

echo "== JAYWISDOM UP-TO-50 REAL TRANSFER FETCH =="
python3 tools/replay/fetch_first_50_jaywisdom_transfers.py \
  --rpc-url "$BASE_RPC_URL" \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F \
  --from-block 0 \
  --limit 50 \
  --output docs/zora/fixtures/JAYWISDOM_first50_transfers.csv

echo "== VALIDATE CSV + OPTIONAL TOTALSUPPLY =="
BASE_RPC_URL="$BASE_RPC_URL" \
python3 tools/replay/jaywisdom_inception_replay_validator.py \
  --csv docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F \
  | tee docs/zora/fixtures/JAYWISDOM_first50_validation_receipt.json

echo "== HASH OUTPUTS =="
sha256sum docs/zora/fixtures/JAYWISDOM_first50_transfers.csv
sha256sum docs/zora/fixtures/JAYWISDOM_first50_validation_receipt.json

echo "== PREVIEW =="
head -n 6 docs/zora/fixtures/JAYWISDOM_first50_transfers.csv
```

## Path B — Operator BaseScan CSV Export

Use this when the operator manually downloads a BaseScan token transfer export.

```bash
set -e

cd ~/AL 2>/dev/null || cd ~/COMPUTERWISDOM/AL 2>/dev/null || cd ~/COMPUTERWISDOM/JOY 2>/dev/null || pwd

INPUT_CSV="/path/to/basescan-token-transfer-export.csv"

echo "== CONVERT BASESCAN EXPORT =="
python3 tools/replay/convert_basescan_to_jaywisdom.py \
  --input "$INPUT_CSV" \
  --output docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --decimals 18 \
  --source basescan_export

echo "== VALIDATE CSV =="
python3 tools/replay/jaywisdom_inception_replay_validator.py \
  --csv docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  --contract 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F \
  | tee docs/zora/fixtures/JAYWISDOM_first50_validation_receipt.json

echo "== HASH OUTPUTS =="
sha256sum docs/zora/fixtures/JAYWISDOM_first50_transfers.csv
sha256sum docs/zora/fixtures/JAYWISDOM_first50_validation_receipt.json

echo "== PREVIEW =="
head -n 6 docs/zora/fixtures/JAYWISDOM_first50_transfers.csv
```

## Commit After Successful Local Run

Only run this after the CSV contains real rows from RPC or operator export and the validator has produced JSON.

```bash
git status --short

git add \
  docs/zora/fixtures/JAYWISDOM_first50_transfers.csv \
  docs/zora/fixtures/JAYWISDOM_first50_validation_receipt.json

git commit -m "data(zora): add JAYWISDOM transfer replay receipt"
git push origin master

git log --oneline -5
git status --short --branch
```

## Feed Back Here

Paste either:

```text
1. docs/zora/fixtures/JAYWISDOM_first50_validation_receipt.json
2. sha256sum outputs
3. real CSV rows
4. final commit SHA after push
```

## Validation Meaning

```text
rows_present=true only after real CSV rows exist
inception_anchor_ready=true only after earliest real row is validated
rpc_total_supply_checked=true only if BASE_RPC_URL validation succeeded
short_event_set_valid=true if fewer than 50 real events exist and no padding is used
revenue_confirmed=false always unless a separate creator earnings receipt exists
```

## Boundary

```text
chain_write=false
wallet_control=false
signing=false
broadcast=false
private_key_handling=false
revenue_confirmed=false
authority=false
no_fake_green=true
```

## Ruling

```text
LOCAL_RUNBOOK = LANDED
LOCAL_OPERATOR_ACTION_REQUIRED = TRUE
CSV_ROWS = REAL_TRANSFER_EVENTS_ONLY
PADDING_ALLOWED = FALSE
FIRST50_ROWS = NOT_POPULATED_BY_ASSISTANT
NEXT_RECEIPT = REAL_CSV_OR_VALIDATOR_STDOUT
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
