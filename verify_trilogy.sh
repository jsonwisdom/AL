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
EXPECTED_BUNDLE="$(strip0x "$(jq -r '.bundle.sha256' "$TARGET")")"

echo "Downloading bundle: $CID"
curl -fL --retry 3 --connect-timeout 20 \
  "https://ipfs.io/ipfs/${CID}" \
  -o "$WORK/bundle.zip"

ACTUAL_BUNDLE="$(sha256sum "$WORK/bundle.zip" | awk '{print $1}')"
[[ "$ACTUAL_BUNDLE" == "$EXPECTED_BUNDLE" ]] || fail "bundle.zip mismatch"

unzip -q "$WORK/bundle.zip" -d "$WORK/unpacked"

for f in $(jq -r '.images | keys[]' "$TARGET"); do
  expected="$(strip0x "$(jq -r ".images[\"$f\"]" "$TARGET")")"
  actual="$(sha256sum "$WORK/unpacked/$f" | awk '{print $1}')"
  [[ "$actual" == "$expected" ]] || fail "$f mismatch"
done

cat > "$RECEIPT" <<JSON
{"status":"PASS","artifact":"ALMS_TRILOGY_V1_CI_REPLAY","bundle_cid":"$CID","ts":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
JSON

echo "PASS: Trilogy verified"
