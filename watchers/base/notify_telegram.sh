#!/usr/bin/env bash
set -euo pipefail

MSG="${1:-TEST}"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="$MSG" > /dev/null

echo "SENT: $MSG"
