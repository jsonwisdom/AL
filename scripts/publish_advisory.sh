#!/usr/bin/env bash
set -euo pipefail

# ALMS Advisory Publisher
# Open public system: GitHub is conduit. Replay decides validity.

: "${PINATA_JWT:?Set PINATA_JWT first}"

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
COMMIT="$(git rev-parse HEAD)"
ROOT_FILE="_truth/merkle/root.txt"
MANIFEST_FILE="_truth/merkle/manifest.json"
LEAVES_FILE="_truth/merkle/leaves.jsonl"
OUT_BASE="_truth/advisory"
IPFS_OUT="_truth/ipfs/latest_advisory_index.json"
SNAP="$OUT_BASE/alms_advisory_$TS"
ARCHIVE="$SNAP.tar.gz"

mkdir -p "$OUT_BASE" "_truth/ipfs"

test -f "$ROOT_FILE" || { echo "FAIL missing $ROOT_FILE"; exit 1; }
test -f "$MANIFEST_FILE" || { echo "FAIL missing $MANIFEST_FILE"; exit 1; }
test -f "$LEAVES_FILE" || { echo "FAIL missing $LEAVES_FILE"; exit 1; }

jq . "$MANIFEST_FILE" >/dev/null
ROOT="$(tr -d '[:space:]' < "$ROOT_FILE")"
MANIFEST_ROOT="$(jq -r '.root' "$MANIFEST_FILE" | sed 's/^sha256://')"

if [ "$ROOT" != "$MANIFEST_ROOT" ]; then
  echo "FAIL merkle_root_mismatch root.txt=$ROOT manifest=$MANIFEST_ROOT"
  exit 1
fi

# Remove failed Pinata response folders and stray failed responses from previous manual runs.
find "$OUT_BASE" -type f -name 'pinata_response.json' -print0 2>/dev/null | while IFS= read -r -d '' f; do
  if jq -e 'has("error")' "$f" >/dev/null 2>&1; then
    dir="$(dirname "$f")"
    echo "CLEAN_FAILED_PINATA_RESPONSE $dir"
    rm -rf "$dir"
  fi
done

mkdir -p "$SNAP"
cp "$ROOT_FILE" "$SNAP/root.txt"
cp "$MANIFEST_FILE" "$SNAP/manifest.json"
cp "$LEAVES_FILE" "$SNAP/leaves.jsonl"

jq -cn \
  --arg ts "$TS" \
  --arg commit "$COMMIT" \
  --arg root "sha256:$ROOT" \
  --arg identity "jaywisdom.base.eth" \
  '{
    type:"ALMS_ADVISORY_INDEX_V1",
    identity:$identity,
    generated_at:$ts,
    git_commit:$commit,
    merkle_root:$root,
    files:{
      root:"root.txt",
      manifest:"manifest.json",
      leaves:"leaves.jsonl"
    },
    doctrine:"Open public system. GitHub is conduit. Replay decides validity."
  }' > "$SNAP/advisory.json"

tar -czf "$ARCHIVE" -C "$SNAP" .
ARCHIVE_SHA256="$(sha256sum "$ARCHIVE" | awk '{print $1}')"

curl -s -X POST https://api.pinata.cloud/pinning/pinFileToIPFS \
  -H "Authorization: Bearer $PINATA_JWT" \
  -F "file=@$ARCHIVE" \
  | tee "$SNAP/pinata_response.json" >/dev/null

if jq -e 'has("error")' "$SNAP/pinata_response.json" >/dev/null; then
  echo "FAIL pinata_error $(cat "$SNAP/pinata_response.json")"
  exit 1
fi

CID="$(jq -r '.IpfsHash' "$SNAP/pinata_response.json")"
PIN_SIZE="$(jq -r '.PinSize // empty' "$SNAP/pinata_response.json")"
PIN_TS="$(jq -r '.Timestamp // empty' "$SNAP/pinata_response.json")"

test -n "$CID" && test "$CID" != "null" || { echo "FAIL missing_ipfs_hash"; exit 1; }

jq -cn \
  --arg cid "$CID" \
  --arg root "sha256:$ROOT" \
  --arg commit "$COMMIT" \
  --arg ts "$TS" \
  --arg archive_sha256 "$ARCHIVE_SHA256" \
  --arg pin_size "$PIN_SIZE" \
  --arg pin_ts "$PIN_TS" \
  '{
    type:"ALMS_LATEST_ADVISORY_INDEX_V1",
    advisory_cid:$cid,
    advisory_uri:("ipfs://" + $cid),
    gateway:("https://gateway.pinata.cloud/ipfs/" + $cid),
    merkle_root:$root,
    git_commit:$commit,
    generated_at:$ts,
    archive:"tar.gz",
    archive_sha256:$archive_sha256,
    pinata:{pin_size:$pin_size,timestamp:$pin_ts},
    doctrine:"Open public system. GitHub is conduit. Replay decides validity."
  }' > "$IPFS_OUT"

echo "ADVISORY_PUBLISH_OK cid=$CID root=sha256:$ROOT commit=$COMMIT archive=$ARCHIVE sha256=$ARCHIVE_SHA256"

echo "VERIFY_START"

if ./scripts/verify_advisory.sh _truth/ipfs/latest_advisory_index.json; then
  echo "PUBLISH_VERIFY_OK cid=$CID"
else
  echo "FAIL publish_verification_failed"
  exit 1
fi
