#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-}"
REASON="${2:-unspecified}"

if [ -z "$FILE" ]; then
  echo "USAGE: tombstone_file.sh <file> <reason>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "ERROR: file does not exist: $FILE"
  exit 1
fi

LOG="_truth/tombstones/tombstones.jsonl"
mkdir -p _truth/tombstones

TS=$(date -u +%FT%TZ)
HASH=$(sha256sum "$FILE" | awk '{print $1}')
GIT_HEAD=$(git rev-parse HEAD 2>/dev/null || echo "NO_GIT")

# === WRITE TOMBSTONE ENTRY ===
jq -n \
  --arg ts "$TS" \
  --arg file "$FILE" \
  --arg reason "$REASON" \
  --arg hash "$HASH" \
  --arg git "$GIT_HEAD" \
  '{
    ts:$ts,
    type:"TOMBSTONE",
    file:$file,
    reason:$reason,
    sha256:$hash,
    git_head:$git,
    status:"TOMBSTONED"
  }' >> "$LOG"

echo "TOMBSTONE_WRITTEN $FILE"

# === DELETE FILE ===
rm -f "$FILE"

echo "FILE_REMOVED $FILE"
