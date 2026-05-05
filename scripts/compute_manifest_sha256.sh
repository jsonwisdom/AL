#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-}"
FIELD="${2:-}"

if [ -z "$FILE" ] || [ -z "$FIELD" ]; then
  echo "Usage: $0 <json_file> <manifest_hash_field>"
  echo "Example: $0 _truth/views/VIEW_LAYER_001.json view_manifest_sha256"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "FILE_NOT_FOUND: $FILE"
  exit 1
fi

jq --arg field "$FIELD" '.[$field]=null' "$FILE" \
  | jq -cS . \
  | sha256sum \
  | awk '{print $1}'
