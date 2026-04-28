#!/usr/bin/env bash
set -euo pipefail

MANIFEST="${1:-docs/verified-claims.json}"

command -v jq >/dev/null 2>&1 || { echo "MANIFEST_FAIL reason=missing_jq" >&2; exit 2; }

test -f "$MANIFEST" || { echo "MANIFEST_FAIL reason=missing_manifest path=$MANIFEST" >&2; exit 1; }

jq empty "$MANIFEST"

jq -r '.claims[].canonical_json' "$MANIFEST" \
  | sed 's#^\.\./##' \
  | while read -r f; do
      test -f "$f" && echo "OK $f" || { echo "MISSING $f"; exit 1; }
    done

bash verify.sh

echo "MANIFEST_OK path=$MANIFEST"
