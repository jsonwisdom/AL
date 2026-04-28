#!/usr/bin/env bash
set -euo pipefail

# Simple multi-agent simulation
ITERATIONS=${1:-10}
CLAIM_PREFIX="SIM"

for i in $(seq 1 $ITERATIONS); do
  CLAIM_ID="${CLAIM_PREFIX}_$i"

  # Simulate agent alpha (high accuracy, higher cost)
  STATE_ALPHA="RESOLVED"
  COST_ALPHA="0.01"

  # Simulate agent beta (lower accuracy, cheaper)
  if (( RANDOM % 2 )); then
    STATE_BETA="DRIFT"
  else
    STATE_BETA="FAIL"
  fi
  COST_BETA="0.005"

  echo "Simulating claim $CLAIM_ID"

  # Run router after receipts exist
  bash scripts/router.sh "$CLAIM_ID"
done
