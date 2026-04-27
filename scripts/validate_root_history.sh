#!/usr/bin/env bash
set -euo pipefail

FILE="_truth/root_history/root_history.jsonl"

PREV="GENESIS"

while read -r line; do
  CANON=$(echo "$line" | jq 'del(.entry_hash)' | jq -cS .)
  HASH=$(printf '%s' "$CANON" | sha256sum | awk '{print $1}')
  STORED=$(echo "$line" | jq -r '.entry_hash')
  LINK=$(echo "$line" | jq -r '.prev_entry_hash')

  if [ "$HASH" != "$STORED" ]; then
    echo "HASH_MISMATCH"
    exit 1
  fi

  if [ "$LINK" != "$PREV" ]; then
    echo "CHAIN_BREAK"
    exit 1
  fi

  PREV="$STORED"
done < "$FILE"

echo "ROOT_HISTORY_CHAIN_OK"
