#!/usr/bin/env bash
# ALMS WebSocket Session Receipt Captor v0.1
# Captures ordered payload deltas into a deterministic SHA-256 hash chain.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_DIR="$ROOT_DIR/_truth/websocket_sessions"
mkdir -p "$SESSION_DIR"

usage() {
  cat <<'USAGE'
Usage:
  scripts/ws_session_receipt.sh <session_name> <payload1> [payload2 ...]
  printf '%s\n' payload1 payload2 | scripts/ws_session_receipt.sh <session_name> --stdin

Output:
  Writes _truth/websocket_sessions/<session_name>.json and prints its path.

Rules:
  - No randomness.
  - No private keys.
  - No RPC.
  - Hash chain starts from prev_hash = 0x0.
  - entry_hash = sha256(prev_hash + payload).
USAGE
}

sha256_text() {
  printf '%s' "$1" | sha256sum | awk '{print $1}'
}

json_escape() {
  jq -Rn --arg s "$1" '$s'
}

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 1
fi

SESSION_NAME="$1"
shift

if [[ ! "$SESSION_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "ALMS_WS_RECEIPT_INVALID reason=bad_session_name" >&2
  exit 1
fi

OUT_FILE="$SESSION_DIR/${SESSION_NAME}.json"
TMP_FILE="${OUT_FILE}.tmp"

payloads=()
if [[ "${1:-}" == "--stdin" ]]; then
  while IFS= read -r line; do
    payloads+=("$line")
  done
else
  payloads=("$@")
fi

if [[ ${#payloads[@]} -eq 0 ]]; then
  echo "ALMS_WS_RECEIPT_INVALID reason=no_payloads" >&2
  exit 1
fi

prev_hash="0x0"
entries_json="[]"
seq_no=1

for payload in "${payloads[@]}"; do
  payload_hash="$(sha256_text "$payload")"
  entry_hash="$(sha256_text "${prev_hash}${payload}")"

  entry="$(jq -cn \
    --argjson seq "$seq_no" \
    --arg type "delta" \
    --arg payload "$payload" \
    --arg payload_hash "$payload_hash" \
    --arg prev_hash "$prev_hash" \
    --arg entry_hash "$entry_hash" \
    '{seq:$seq,type:$type,payload:$payload,payload_hash:$payload_hash,prev_hash:$prev_hash,entry_hash:$entry_hash}')"

  entries_json="$(jq -cn --argjson entries "$entries_json" --argjson entry "$entry" '$entries + [$entry]')"
  prev_hash="$entry_hash"
  seq_no=$((seq_no + 1))
done

session_id="$(sha256_text "$SESSION_NAME")"
final_state_hash="$prev_hash"

jq -cn \
  --arg schema "alms.ws_session_receipt.v0.1" \
  --arg session_name "$SESSION_NAME" \
  --arg session_id "$session_id" \
  --arg initial_state_hash "0x0" \
  --arg final_state_hash "$final_state_hash" \
  --argjson entries "$entries_json" \
  '{schema:$schema,session_name:$session_name,session_id:$session_id,initial_state_hash:$initial_state_hash,entries:$entries,final_state_hash:$final_state_hash}' \
  > "$TMP_FILE"

mv "$TMP_FILE" "$OUT_FILE"
echo "$OUT_FILE"
