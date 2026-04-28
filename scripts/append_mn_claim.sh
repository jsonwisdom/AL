#!/usr/bin/env bash
set -euo pipefail

CLAIM_TEXT="${1:-}"
CLAIM_ID="${2:-}"
LEDGER="${LEDGER:-_truth/ledger.jsonl}"

if [ -z "$CLAIM_TEXT" ]; then
  echo "APPEND_MN_FAIL reason=missing_claim_text" >&2
  echo "usage: scripts/append_mn_claim.sh 'CLAIM_TEXT' [CLAIM_ID]" >&2
  exit 2
fi

command -v jq >/dev/null 2>&1 || { echo "APPEND_MN_FAIL reason=missing_jq" >&2; exit 2; }
command -v sha256sum >/dev/null 2>&1 || { echo "APPEND_MN_FAIL reason=missing_sha256sum" >&2; exit 2; }

mkdir -p "$(dirname "$LEDGER")"
touch "$LEDGER"

if [ -z "$CLAIM_ID" ]; then
  CLAIM_ID="mn_$(date -u +%Y%m%dT%H%M%SZ)_$(printf '%s' "$CLAIM_TEXT" | sha256sum | awk '{print substr($1,1,8)}')"
fi

TEXT_HASH="$(printf '%s' "$CLAIM_TEXT" | sha256sum | awk '{print $1}')"

if [ -s "$LEDGER" ]; then
  LAST_LINE="$(tail -n 1 "$LEDGER")"
  PREV_HASH="sha256:$(printf '%s' "$LAST_LINE" | sha256sum | awk '{print $1}')"
else
  PREV_HASH="null"
fi

jq -cn \
  --arg claim_id "$CLAIM_ID" \
  --arg claim_text "$CLAIM_TEXT" \
  --arg document "Minnesota source document" \
  --arg watcher "append_mn_claim.sh" \
  --arg text_hash "sha256:$TEXT_HASH" \
  --arg prev_hash "$PREV_HASH" \
  '{claim_id:$claim_id, claim_text:$claim_text, source:{document:$document, watcher:$watcher}, artifacts:{text_hash:$text_hash}, prev_hash:$prev_hash, status:"verified"}' \
  >> "$LEDGER"

echo "APPEND_MN_OK claim_id=$CLAIM_ID text_hash=sha256:$TEXT_HASH prev_hash=$PREV_HASH ledger=$LEDGER"
