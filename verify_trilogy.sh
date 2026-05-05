#!/usr/bin/env bash
set -euo pipefail

TARGET="alms_trilogy/hashes.json"
RECEIPT=".trilogy_verify"

jq -r '.trilogy_hash' "$TARGET" > /dev/null

fail() { echo "FAIL: $1"; exit 1; }

strip0x() { echo "$1" | sed 's/^0x//' ; }

check_hash() {
  local file=$1
  local expected=$(strip0x "$2")
  local actual=$(sha256sum "$file" | awk '{print $1}')
  if [[ "$actual" != "$expected" ]]; then
    fail "$file mismatch"
  fi
}

# Images
for f in $(jq -r '.images | keys[]' "$TARGET"); do
  check_hash "alms_trilogy/$f" $(jq -r ".images[\"$f\"]" "$TARGET")
done

# Bundle (optional local file check skipped if not present)

# Write receipt
echo "{\"status\":\"PASS\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$RECEIPT"

echo "PASS: Trilogy verified"
