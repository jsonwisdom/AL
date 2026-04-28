#!/usr/bin/env bash
set -euo pipefail

ITERATIONS=${1:-10}
CLAIM_PREFIX="SIM"

for i in $(seq 1 $ITERATIONS); do
  CLAIM_ID="${CLAIM_PREFIX}_$i"

  echo "Simulating claim $CLAIM_ID"

  # Run router (assumes receipts exist)
  bash scripts/router.sh "$CLAIM_ID"

  # Adaptive step every 10 rounds
  if (( i % 10 == 0 )); then
    TOP=$(jq -r '.[0].agent_id' _truth/routing/leaderboard.json)

    if [ "$TOP" = "agent_alpha" ]; then
      bash scripts/adapt_agent.sh agent_alpha 1 0.8 1.2
      bash scripts/adapt_agent.sh agent_beta 2 0.8 1.0
    else
      bash scripts/adapt_agent.sh agent_beta 1 0.8 1.2
      bash scripts/adapt_agent.sh agent_alpha 2 0.8 1.0
    fi
  fi
done
