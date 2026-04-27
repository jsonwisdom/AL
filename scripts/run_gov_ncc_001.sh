#!/usr/bin/env bash
set -euo pipefail

./scripts/verify_gov_ncc_event.sh data/gov_ncc_001/source.json
cat _truth/receipts/gov_ncc_001.receipt.json
echo
