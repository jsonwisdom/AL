#!/usr/bin/env bash
set -euo pipefail

FILE="_truth/root/alms_root.json"
STATE="_truth/root/.last_root_hash"

CURRENT=$(jq -r '.root_sha256' "$FILE")

if [ -f "$STATE" ]; then
  PREV=$(cat "$STATE")
else
  PREV=""
fi

if [ "$CURRENT" != "$PREV" ]; then
  echo "ALMS_ROOT_CHANGED old=$PREV new=$CURRENT"
  echo "$CURRENT" > "$STATE"
else
  echo "ALMS_ROOT_STABLE hash=$CURRENT"
fi
