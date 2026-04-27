#!/usr/bin/env bash
set -euo pipefail

SRC="data/intake/official_sources.json"

jq -c '.sources[]' "$SRC" | while read -r s; do
  id=$(echo "$s" | jq -r '.id')
  url=$(echo "$s" | jq -r '.url')
  label=$(echo "$s" | jq -r '.label')

  echo "SOURCE_FOUND id=$id label=\"$label\" url=$url"
done

echo "CRAWL_DONE"
