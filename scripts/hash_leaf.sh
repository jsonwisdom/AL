#!/usr/bin/env bash
set -euo pipefail

FILE="$1"

# canonicalize JSON (sorted, no whitespace drift)
CANON=$(cat "$FILE" | python3 -c 'import json,sys;print(json.dumps(json.load(sys.stdin),separators=(",",":"),sort_keys=True))')

echo "$CANON" > /tmp/canon.json

# sha256 hash
HASH=$(printf "%s" "$CANON" | sha256sum | awk '{print $1}')

echo "CANONICAL_JSON:"
cat /tmp/canon.json
echo
echo "SHA256:"
echo $HASH
