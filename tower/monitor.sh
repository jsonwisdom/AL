#!/usr/bin/env bash
set -euo pipefail

LEDGER="./trinity/ledger/audit_trail.jsonl"
STATE_LOG="./arcade/data/leaf_actions.log"

LAST_ROOT="$(tail -n 1 "$LEDGER" | jq -r '.root')"
CURRENT_ROOT="$(sha256sum "$STATE_LOG" | awk '{print $1}')"

if [[ "$LAST_ROOT" != "$CURRENT_ROOT" ]]; then
  echo "[ALERT] Constitutional Drift Detected. Arcade Halted."
  exit 1
fi

echo "[GREEN] Arcade root matches ledger."
