#!/usr/bin/env bash
# =============================================================================
# ALMS Source Authenticity Verifier v1
# Verifies structured source anchors against contracts/source_registry.v1.json.
#
# Input:
#   Path to a JSON array of numeric objects, each optionally containing:
#   .source_anchor = {
#     "type": "url",
#     "location": "https://...",
#     "expected_raw_hash": "sha256:...",
#     "ipfs_cid": "bafy...",
#     "ens_key": "alms..."
#   }
#
# Policy v1:
#   - Missing registry entry: WARN only
#   - Declared field mismatch: HARD FAIL
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY="$PROJECT_ROOT/contracts/source_registry.v1.json"
VERIFY_FAIL="ALMS_VERIFY_FAIL source_authenticity_failed"

usage() {
  cat <<'EOF'
Usage:
  scripts/alms_verify_anchor.sh numbers.json

numbers.json must be a JSON array of extracted numeric objects.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -ne 1 ]; then
  echo "ALMS_VERIFY_ANCHOR_ERROR expected_numbers_json" >&2
  usage >&2
  exit 2
fi

NUMBERS_FILE="$1"
if [ ! -f "$NUMBERS_FILE" ]; then
  echo "ALMS_VERIFY_ANCHOR_ERROR missing_numbers_file path=$NUMBERS_FILE" >&2
  exit 2
fi

if [ ! -f "$REGISTRY" ]; then
  echo "ALMS_WARN registry_missing path=$REGISTRY" >&2
  exit 0
fi

jq -c '.[]' "$NUMBERS_FILE" | while read -r num; do
  anchor_type=$(printf '%s' "$num" | jq -r '.source_anchor.type // empty')
  if [ "$anchor_type" != "url" ]; then
    continue
  fi

  url=$(printf '%s' "$num" | jq -r '.source_anchor.location // empty')
  exp_hash=$(printf '%s' "$num" | jq -r '.source_anchor.expected_raw_hash // empty')
  exp_ipfs=$(printf '%s' "$num" | jq -r '.source_anchor.ipfs_cid // empty')
  exp_ens=$(printf '%s' "$num" | jq -r '.source_anchor.ens_key // empty')

  if [ -z "$url" ]; then
    continue
  fi

  reg_entry=$(jq -c --arg url "$url" '.sources[]? | select(.url == $url)' "$REGISTRY" | head -1)

  if [ -z "$reg_entry" ] || [ "$reg_entry" = "null" ]; then
    echo "ALMS_WARN source_authenticity_no_registry url=$url" >&2
    continue
  fi

  reg_hash=$(printf '%s' "$reg_entry" | jq -r '.raw_hash // empty')
  reg_ipfs=$(printf '%s' "$reg_entry" | jq -r '.ipfs_cid // empty')
  reg_ens=$(printf '%s' "$reg_entry" | jq -r '.ens_key // empty')

  if [ -n "$exp_hash" ] && [ "$exp_hash" != "$reg_hash" ]; then
    echo "$VERIFY_FAIL url=$url expected_hash=$exp_hash registry_hash=$reg_hash" >&2
    exit 1
  fi

  if [ -n "$exp_ipfs" ] && [ "$exp_ipfs" != "$reg_ipfs" ]; then
    echo "$VERIFY_FAIL url=$url expected_ipfs=$exp_ipfs registry_ipfs=$reg_ipfs" >&2
    exit 1
  fi

  if [ -n "$exp_ens" ] && [ "$exp_ens" != "$reg_ens" ]; then
    echo "$VERIFY_FAIL url=$url expected_ens=$exp_ens registry_ens=$reg_ens" >&2
    exit 1
  fi

done

echo "ALMS_VERIFY_ANCHOR_OK"
