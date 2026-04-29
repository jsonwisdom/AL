#!/usr/bin/env bash
set -euo pipefail

echo "PREFLIGHT_REPO_AUDIT"

test -f scripts/build_merkle_root.sh || { echo "FAIL missing merkle builder"; exit 1; }
test -f _truth/merkle/root.txt || { echo "FAIL missing merkle root"; exit 1; }
test -f _truth/merkle/manifest.json || { echo "FAIL missing merkle manifest"; exit 1; }

if git status --short | grep -q '^?? site/index.html'; then
  echo "FAIL new homepage detected: site/index.html"
  echo "Use site/live/index.html instead."
  exit 1
fi

if grep -R "UNKNOWN_HASH" _truth/receipts _truth/cards site/cards 2>/dev/null; then
  echo "WARN UNKNOWN_HASH present"
fi

jq . _truth/merkle/manifest.json >/dev/null

echo "PREFLIGHT_OK"

DUPES="$(jq -r 'select(.receipt_hash != null) | .receipt_hash' _truth/receipts/*.json 2>/dev/null | sort | uniq -d)"
if [ -n "$DUPES" ]; then
  echo "FATAL: DUPLICATE_RECEIPT_HASHES_DETECTED"
  echo "$DUPES"
  exit 1
fi

if grep -R "verified public record line" _truth/cards site/cards 2>/dev/null; then
  echo "FATAL: PLACEHOLDER_LINE_DETECTED"
  exit 1
fi

if grep -R "UNKNOWN_HASH" _truth 2>/dev/null; then
  echo "FATAL: UNKNOWN_HASH_DETECTED"
  exit 1
fi

echo "PREFLIGHT_HARDENED_VALIDATORS"

if grep -R "UNKNOWN_HASH" _truth 2>/dev/null; then
  echo "FATAL: UNKNOWN_HASH_DETECTED"
  exit 1
fi

if grep -R "verified public record line" _truth/cards site/cards 2>/dev/null; then
  echo "FATAL: PLACEHOLDER_LINE_DETECTED"
  exit 1
fi

MISSING_CARD_FIELD="$(jq -r 'select((has("leaf")|not) or (has("extracted_line")|not) or (has("hash")|not)) | input_filename' _truth/cards/*.card.json 2>/dev/null | head -1 || true)"
if [ -n "$MISSING_CARD_FIELD" ]; then
  echo "FATAL: CARD_SCHEMA_REQUIRED_FIELDS $MISSING_CARD_FIELD"
  exit 1
fi

DUPES="$(jq -r '.receipt_hash // .hash // empty' _truth/receipts/*.json 2>/dev/null | sort | uniq -d)"
if [ -n "$DUPES" ]; then
  echo "FATAL: DUPLICATE_RECEIPT_HASHES_DETECTED"
  echo "$DUPES"
  exit 1
fi


if [ -x ./scripts/verify_merkle_root.sh ]; then
  ./scripts/verify_merkle_root.sh >/dev/null
else
  echo "FATAL: MISSING_VERIFY_MERKLE_ROOT"
  exit 1
fi

echo "PREFLIGHT_HARDENED_VALIDATORS_OK"

echo "PREFLIGHT_MANIFEST_REFERENCE_CHECK"

MISSING_REFS="$(
  jq -r '.leaves[]? | .path // .file // .source // empty' _truth/merkle/manifest.json 2>/dev/null \
  | while read -r p; do
      [ -z "$p" ] && continue
      [ -f "$p" ] || echo "$p"
    done
)"

if [ -n "$MISSING_REFS" ]; then
  echo "FATAL: MANIFEST_REFERENCES_MISSING"
  echo "$MISSING_REFS"
  exit 1
fi

echo "PREFLIGHT_MANIFEST_REFERENCE_CHECK_OK"

echo "PREFLIGHT_SOURCE_REGISTRY_CHECK"

if [ -f contracts/source_registry.v1.json ]; then
  BAD_SOURCE_HASHES="$(
    jq -r '.sources[]? | select(.raw_hash? and (.raw_hash | test("^sha256:1{64}$|REPLACE_WITH_ACTUAL_HASH|UNKNOWN_HASH"))) | "\(.id):\(.raw_hash)"' contracts/source_registry.v1.json 2>/dev/null || true
  )"

  if [ -n "$BAD_SOURCE_HASHES" ]; then
    echo "FATAL: SOURCE_REGISTRY_PLACEHOLDER_HASH"
    echo "$BAD_SOURCE_HASHES"
    exit 1
  fi
fi

echo "PREFLIGHT_SOURCE_REGISTRY_CHECK_OK"

echo "PREFLIGHT_FULL_CHAIN_CONSISTENCY_CHECK"

REG_HASH="$(jq -r '.sources[]? | select(.id=="mn_mmb_feb2026_forecast") | .raw_hash // empty' contracts/source_registry.v1.json 2>/dev/null)"
MN1_URI="$(jq -r '.fetch_uri // .golden_uri // empty' _truth/receipts/MN_001.json 2>/dev/null)"
MN1_CONTENT_HASH="$(jq -r '.content_hash // empty' _truth/receipts/MN_001.json 2>/dev/null)"
MANIFEST_MN1_HASH="$(jq -r '.leaves[]? | select(.path=="_truth/receipts/MN_001.json") | .hash // empty' _truth/merkle/manifest.json 2>/dev/null)"
ACTUAL_MN1_FILE_HASH="sha256:$(sha256sum _truth/receipts/MN_001.json | awk '{print $1}')"

if [ -z "$REG_HASH" ]; then
  echo "FATAL: FULL_CHAIN_MISSING_SOURCE_REGISTRY_HASH"
  exit 1
fi

if [ -z "$MN1_URI" ]; then
  echo "FATAL: FULL_CHAIN_MISSING_RECEIPT_URI"
  exit 1
fi

if [ -z "$MN1_CONTENT_HASH" ]; then
  echo "FATAL: FULL_CHAIN_MISSING_RECEIPT_CONTENT_HASH"
  exit 1
fi

if [ -z "$MANIFEST_MN1_HASH" ]; then
  echo "FATAL: FULL_CHAIN_MISSING_MANIFEST_LEAF"
  exit 1
fi

if [ "$MANIFEST_MN1_HASH" != "$ACTUAL_MN1_FILE_HASH" ]; then
  echo "FATAL: FULL_CHAIN_MANIFEST_RECEIPT_HASH_MISMATCH"
  echo "manifest=$MANIFEST_MN1_HASH"
  echo "actual=$ACTUAL_MN1_FILE_HASH"
  exit 1
fi

if ! grep -q "$MN1_URI" contracts/source_registry.v1.json; then
  echo "FATAL: FULL_CHAIN_URI_NOT_IN_SOURCE_REGISTRY"
  echo "$MN1_URI"
  exit 1
fi

echo "PREFLIGHT_FULL_CHAIN_CONSISTENCY_CHECK_OK"
