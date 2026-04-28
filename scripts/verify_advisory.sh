#!/usr/bin/env bash
set -euo pipefail

INDEX="${1:-_truth/ipfs/latest_advisory_index.json}"

test -f "$INDEX" || { echo "FAIL missing_index $INDEX"; exit 1; }

jq . "$INDEX" >/dev/null

CID="$(jq -r '.advisory_cid' "$INDEX")"
ROOT_EXPECTED="$(jq -r '.merkle_root' "$INDEX" | sed 's/^sha256://')"
ARCHIVE_SHA_EXPECTED="$(jq -r '.archive_sha256 // empty' "$INDEX")"

test -n "$CID" && test "$CID" != "null" || { echo "FAIL missing_cid"; exit 1; }
test -n "$ROOT_EXPECTED" && test "$ROOT_EXPECTED" != "null" || { echo "FAIL missing_root"; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

URL="https://gateway.pinata.cloud/ipfs/$CID"
ARCHIVE="$TMP/advisory.tar.gz"

curl -L -s "$URL" -o "$ARCHIVE"

if [ ! -s "$ARCHIVE" ]; then
  echo "FAIL empty_archive cid=$CID"
  exit 1
fi

if [ -n "$ARCHIVE_SHA_EXPECTED" ] && [ "$ARCHIVE_SHA_EXPECTED" != "null" ]; then
  ARCHIVE_SHA_ACTUAL="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
  if [ "$ARCHIVE_SHA_ACTUAL" != "$ARCHIVE_SHA_EXPECTED" ]; then
    echo "FAIL archive_sha_mismatch expected=$ARCHIVE_SHA_EXPECTED actual=$ARCHIVE_SHA_ACTUAL"
    exit 1
  fi
fi

mkdir -p "$TMP/unpack"
tar -xzf "$ARCHIVE" -C "$TMP/unpack"

test -f "$TMP/unpack/root.txt" || { echo "FAIL missing_root_txt"; exit 1; }
test -f "$TMP/unpack/manifest.json" || { echo "FAIL missing_manifest"; exit 1; }
test -f "$TMP/unpack/leaves.jsonl" || { echo "FAIL missing_leaves"; exit 1; }

ROOT_TXT="$(tr -d '[:space:]' < "$TMP/unpack/root.txt")"
ROOT_MANIFEST="$(jq -r '.root' "$TMP/unpack/manifest.json" | sed 's/^sha256://')"

if [ "$ROOT_TXT" != "$ROOT_EXPECTED" ]; then
  echo "FAIL root_txt_mismatch expected=$ROOT_EXPECTED actual=$ROOT_TXT"
  exit 1
fi

if [ "$ROOT_MANIFEST" != "$ROOT_EXPECTED" ]; then
  echo "FAIL manifest_root_mismatch expected=$ROOT_EXPECTED actual=$ROOT_MANIFEST"
  exit 1
fi

echo "ADVISORY_VERIFY_OK root=sha256:$ROOT_EXPECTED cid=$CID"
