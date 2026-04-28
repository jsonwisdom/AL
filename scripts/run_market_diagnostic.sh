#!/usr/bin/env bash
set -euo pipefail

ROUNDS="${1:-50}"

command -v jq >/dev/null 2>&1 || { echo "MARKET_DIAG_FAIL reason=missing_jq" >&2; exit 2; }

mkdir -p _truth/routing

# Fresh diagnostic window. Comment this out if you want cumulative history.
: > _truth/routing/history.jsonl

bash scripts/simulate_agents.sh "$ROUNDS"
bash scripts/export_routing_history.sh
bash scripts/diagnose_routing_history.sh | tee _truth/routing/diagnostic.json

echo "MARKET_DIAG_OK rounds=$ROUNDS diagnostic=_truth/routing/diagnostic.json history=docs/routing-history.json"
