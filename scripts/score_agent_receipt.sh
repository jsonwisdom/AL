#!/usr/bin/env bash
set -euo pipefail

# INPUT: receipt.json
FILE="$1"

# Extract fields (jq required)
STATE=$(jq -r '.state' "$FILE")
PAID=$(jq -r '.payment.paid' "$FILE")
COST=$(jq -r '.payment.cost_usd' "$FILE")

# Accuracy scoring (simple deterministic)
case "$STATE" in
  RESOLVED) ACC=1.0 ;;
  DRIFT) ACC=0.5 ;;
  FAIL) ACC=0.0 ;;
  *) ACC=0.0 ;;
esac

# Payment gate
if [ "$PAID" != "true" ]; then
  ROUTE_WEIGHT=0
else
  # routing weight = accuracy / cost
  ROUTE_WEIGHT=$(awk "BEGIN {print $ACC / ($COST + 0.0001)}")
fi

# Emit updated receipt
jq \
  --argjson acc "$ACC" \
  --argjson rw "$ROUTE_WEIGHT" \
  '.accuracy.score = $acc | .accuracy.basis = "state_mapping_v1" | .routing.weight = $rw | .routing.rule = "accuracy_over_cost"' \
  "$FILE"
