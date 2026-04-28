#!/usr/bin/env bash
set -euo pipefail

DIAG="${1:-_truth/routing/diagnostic.json}"

command -v jq >/dev/null 2>&1 || { echo "ASSERT_FAIL reason=missing_jq" >&2; exit 2; }

if [ ! -f "$DIAG" ]; then
  echo "ASSERT_FAIL reason=missing_diagnostic path=$DIAG" >&2
  exit 2
fi

ROUNDS=$(jq -r '.rounds // 0' "$DIAG")
FLIPS=$(jq -r '.flip_count // 0' "$DIAG")
STRATS=$(jq -r '[.strategy_distribution[]?.strategy] | unique | length' "$DIAG")
DRIFT=$(jq -r '[.profile_drift[]? | select((.first.accuracy_target != .last.accuracy_target) or (.first.cost_target != .last.cost_target))] | length' "$DIAG")
DIAGNOSIS=$(jq -r '.diagnosis // "UNKNOWN"' "$DIAG")

if [ "$ROUNDS" -lt 10 ]; then
  echo "ASSERT_FAIL reason=too_few_rounds rounds=$ROUNDS" >&2
  exit 1
fi

if [ "$STRATS" -lt 2 ]; then
  echo "ASSERT_FAIL reason=no_strategy_diversity strategies=$STRATS" >&2
  exit 1
fi

if [ "$DRIFT" -lt 1 ]; then
  echo "ASSERT_FAIL reason=no_profile_drift" >&2
  exit 1
fi

if [ "$DIAGNOSIS" = "CHAOTIC_OR_UNDER_CONSTRAINED" ]; then
  echo "ASSERT_FAIL reason=chaotic flip_count=$FLIPS" >&2
  exit 1
fi

echo "ASSERT_OK rounds=$ROUNDS flips=$FLIPS strategies=$STRATS drift_agents=$DRIFT diagnosis=$DIAGNOSIS"
