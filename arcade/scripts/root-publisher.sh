#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="./arcade/data"
STATE_LOG="$STATE_DIR/leaf_actions.log"
LEDGER="./trinity/ledger/audit_trail.jsonl"

validate_state() {
  [[ -f "$STATE_LOG" ]] || { echo "[ERROR] Missing state log."; exit 1; }

  if [[ -s "$STATE_LOG" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      echo "$line" | jq -e . >/dev/null || {
        echo "[ERROR] Corrupt JSON leaf."
        exit 1
      }
    done < "$STATE_LOG"
  fi
}

generate_root() {
  sha256sum "$STATE_LOG" | awk '{print $1}'
}

publish_to_ledger() {
  local ROOT="$1"
  local TIMESTAMP
  TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  jq -nc \
    --arg ts "$TIMESTAMP" \
    --arg root "$ROOT" \
    --arg status "VERIFIED" \
    '{timestamp:$ts, root:$root, status:$status, subsystem:"arcade"}' >> "$LEDGER"

  echo "[VERDICT: GOLD] Root sealed: $ROOT"
}

validate_state
ROOT="$(generate_root)"
publish_to_ledger "$ROOT"
