#!/usr/bin/env bash
set -euo pipefail

LEAF="$1"

mkdir -p data/$LEAF

cat > data/$LEAF/source.json <<EOT
{
  "leaf_id": "$LEAF",
  "schema": "manual_intake_v1",
  "note": "fill this with real source"
}
EOT

echo "NEW_LEAF_READY: data/$LEAF/source.json"
