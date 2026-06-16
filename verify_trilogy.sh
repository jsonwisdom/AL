#!/usr/bin/env bash
set -euo pipefail
TARGET="alms_trilogy/hashes.json"
WORK=".trilogy_work"
RECEIPT=".trilogy_verify"

fail(){ echo "FAIL: $1"; exit 1; }
strip0x(){ echo "$1" | sed 's/^0x//'; }

rm -rf "$WORK"
mkdir -p "$WORK"

CID="$(jq -r '.bundle.cid' "$TARGET")"
EXPECTED_BUNDLE_HASH="$(strip0x "$(jq -r '.bundle.sha256' "$TARGET")")"

echo "Downloading directory from IPFS: $CID"

# Download each file from the IPFS directory using gateway
for f in $(jq -r '.images | keys[]' "$TARGET"); do
  echo "Downloading: $f"
  curl -fL --retry 3 --connect-timeout 20 \
    "https://ipfs.io/ipfs/${CID}/${f}" \
    -o "$WORK/$f"
  
  # Verify individual file hash
  expected="$(strip0x "$(jq -r ".images[\"$f\"]" "$TARGET")")"
  actual="$(sha256sum "$WORK/$f" | awk '{print $1}')"
  [[ "$actual" == "$expected" ]] || fail "$f mismatch"
  echo "✓ $f matches"
done

# Also verify bundle SHA256 is consistent (if bundle is ever used)
# For now, skip because CID is a directory not a file

cat > "$RECEIPT" <<JSON
{"status":"PASS","artifact":"ALMS_TRILOGY_V1_CI_REPLAY","bundle_cid":"$CID","ts":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
JSON

echo "PASS: Trilogy verified"
