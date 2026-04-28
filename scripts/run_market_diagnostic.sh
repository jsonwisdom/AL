#!/usr/bin/env bash
set -euo pipefail

ROUNDS="${1:-50}"
RESET_PROFILES="${RESET_PROFILES:-1}"

command -v jq >/dev/null 2>&1 || { echo "MARKET_DIAG_FAIL reason=missing_jq" >&2; exit 2; }

mkdir -p _truth/routing agents

# Fresh diagnostic window.
: > _truth/routing/history.jsonl
: > _truth/routing/profile_history.jsonl

# Fresh evolutionary trial unless RESET_PROFILES=0 is supplied.
if [ "$RESET_PROFILES" = "1" ]; then
  cat > agents/agent_alpha_profile.json <<'JSON'
{
  "agent_id": "agent_alpha",
  "accuracy_target": 0.98,
  "cost_target": 0.01,
  "strategy": "leader_precision",
  "last_reason": "reset"
}
JSON

  cat > agents/agent_beta_profile.json <<'JSON'
{
  "agent_id": "agent_beta",
  "accuracy_target": 0.7,
  "cost_target": 0.005,
  "strategy": "challenger_efficiency",
  "last_reason": "reset"
}
JSON
fi

bash scripts/simulate_agents.sh "$ROUNDS"
bash scripts/export_routing_history.sh
bash scripts/diagnose_routing_history.sh | tee _truth/routing/diagnostic.json

echo "MARKET_DIAG_OK rounds=$ROUNDS reset_profiles=$RESET_PROFILES diagnostic=_truth/routing/diagnostic.json history=docs/routing-history.json profiles=_truth/routing/profile_history.jsonl"
