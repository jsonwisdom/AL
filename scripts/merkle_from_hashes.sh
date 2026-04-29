#!/usr/bin/env bash
set -euo pipefail

TMP="$(mktemp)"
cat | sed 's/^sha256://' | grep -E '^[a-f0-9]{64}$' | LC_ALL=C sort > "$TMP"

COUNT="$(wc -l < "$TMP" | tr -d ' ')"
test "$COUNT" -gt 0 || { echo "NO_HASHES"; exit 1; }

CUR="$TMP"
while [ "$(wc -l < "$CUR" | tr -d ' ')" -gt 1 ]; do
  NEXT="$(mktemp)"
  while read -r left; do
    read -r right || right="$left"
    printf '%s%s' "$left" "$right" | sha256sum | awk '{print $1}' >> "$NEXT"
  done < "$CUR"
  CUR="$NEXT"
done

echo "sha256:$(cat "$CUR")"
