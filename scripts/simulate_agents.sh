#!/usr/bin/env bash
set -euo pipefail

ITERATIONS=${1:-10}
CLAIM_PREFIX="SIM"
PROFILE_HISTORY="_truth/routing/profile_history.jsonl"

mkdir -p _truth/routing

for i in $(seq 1 $ITERATIONS); do
  CLAIM_ID="${CLAIM_PREFIX}_$i"

  echo "Simulating claim $CLAIM_ID"

  bash scripts/router.sh "$CLAIM_ID"

  # Adaptive step every 10 rounds using real leaderboard signals.
  # Rank is assigned only after explicit routing_weight sort, never implicit JSON order.
  if (( i % 10 == 0 )); then
    jq -r '
      sort_by(.routing_weight) | reverse
      | to_entries[]
      | [.value.agent_id, (.key + 1), (.value.avg_decay_factor // 1), (.value.reputation_multiplier // 1)]
      | @tsv
    ' _truth/routing/leaderboard.json \
      | while IFS=$'\t' read -r AGENT RANK DECAY REP; do
          bash scripts/adapt_agent.sh "$AGENT" "$RANK" "$DECAY" "$REP"
          jq -c --arg round "$i" '. + {round:($round|tonumber), snapshot_ts:now|todateiso8601}' "agents/${AGENT}_profile.json" >> "$PROFILE_HISTORY"
        done
  fi
done
