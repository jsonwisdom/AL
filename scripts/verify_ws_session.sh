#!/usr/bin/env bash
# ALMS WebSocket Session Verifier v0.3
# Verifies JSON and binary frame chains.

set -euo pipefail

FILE="$1"
[[ ! -f "$FILE" ]] && { echo "Error: File not found"; exit 1; }

COUNT=$(jq '.entries | length' "$FILE")
prev_hash="0x0"
valid=true

for ((i=0;i<COUNT;i++)); do
  type=$(jq -r ".entries[$i].type" "$FILE")
  reported_entry_hash=$(jq -r ".entries[$i].entry_hash" "$FILE")
  reported_prev_hash=$(jq -r ".entries[$i].prev_hash" "$FILE")

  if [[ "$reported_prev_hash" != "$prev_hash" ]]; then valid=false; break; fi

  if [[ "$type" == "canonical_json_frame" ]]; then
    canonical_frame=$(jq -r ".entries[$i].canonical_frame" "$FILE")
    calc_hash=$(printf '%s' "$canonical_frame" | sha256sum | awk '{print $1}')
    calc_entry=$(printf '%s' "${prev_hash}${calc_hash}" | sha256sum | awk '{print $1}')

  elif [[ "$type" == "binary_frame" ]]; then
    binary_hash=$(jq -r ".entries[$i].binary_hash" "$FILE")
    calc_entry=$(printf '%s' "${prev_hash}${binary_hash}" | sha256sum | awk '{print $1}')

  else
    valid=false; break
  fi

  [[ "$reported_entry_hash" != "$calc_entry" ]] && { valid=false; break; }
  prev_hash="$calc_entry"
done

final=$(jq -r '.final_state_hash' "$FILE")
[[ "$prev_hash" != "$final" ]] && valid=false

printf '{"valid": %s, "replay_match": %s, "deltas_processed": %s}\n' "$valid" "$valid" "$COUNT"
