#!/usr/bin/env bash
# ALMS WebSocket Session Verifier v0.1
# Replays the hash chain and validates integrity.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: scripts/verify_ws_session.sh <path_to_session.json>" >&2
  exit 1
fi

FILE="$1"
if [[ ! -f "$FILE" ]]; then
  echo "Error: File not found" >&2
  exit 1
fi

COUNT="$(jq '.entries | length' "$FILE")"

prev_hash="0x0"
valid=true

for ((i=0;i<COUNT;i++)); do
  payload="$(jq -r ".entries[$i].payload" "$FILE")"
  reported_entry_hash="$(jq -r ".entries[$i].entry_hash" "$FILE")"
  reported_prev_hash="$(jq -r ".entries[$i].prev_hash" "$FILE")"
  payload_hash="$(jq -r ".entries[$i].payload_hash" "$FILE")"

  calc_payload_hash="$(printf '%s' "$payload" | sha256sum | awk '{print $1}')"
  calc_entry_hash="$(printf '%s' "${prev_hash}${payload}" | sha256sum | awk '{print $1}')"

  if [[ "$reported_prev_hash" != "$prev_hash" ]]; then
    valid=false; break
  fi
  if [[ "$payload_hash" != "$calc_payload_hash" ]]; then
    valid=false; break
  fi
  if [[ "$reported_entry_hash" != "$calc_entry_hash" ]]; then
    valid=false; break
  fi

  prev_hash="$calc_entry_hash"
done

final_state_hash="$(jq -r '.final_state_hash' "$FILE")"

if [[ "$prev_hash" != "$final_state_hash" ]]; then
  valid=false
fi

printf '{"valid": %s, "replay_match": %s, "deltas_processed": %s}\n' "$valid" "$valid" "$COUNT"
