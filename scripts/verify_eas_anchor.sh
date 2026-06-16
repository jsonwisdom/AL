#!/usr/bin/env bash
set -euo pipefail

EAS_UID="${1:-0x321ae52ab6900744baebd637b87a4cbb307ffc7891810aa456638970111abf48}"
EAS_SCAN_URL="https://base.easscan.org/graphql"

echo "🔍 Verifying EAS Anchor: $EAS_UID"
echo "----------------------------------------"

# Step 1: Fetch attestation using correct plural query
ATTESTATION=$(curl -s -X POST "$EAS_SCAN_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"{ attestations(where: { id: { equals: \\\"$EAS_UID\\\" } }) { id decodedDataJson } }\"
  }")

# Check if attestation exists
if [ "$(echo "$ATTESTATION" | jq -r '.data.attestations[0].id')" = "null" ]; then
  echo "❌ FAIL: Attestation not found. Check UID or wait for indexing."
  echo "   Try: https://base.easscan.org/attestation/view/$EAS_UID"
  exit 1
fi

# Step 2: Extract decoded data
DECODED_JSON=$(echo "$ATTESTATION" | jq -r '.data.attestations[0].decodedDataJson')
DECODED=$(echo "$DECODED_JSON" | jq -r '.[] | {name: .name, value: .value.value}')

# Step 3: Parse fields
CONTENT_HASH=$(echo "$DECODED" | jq -r 'select(.name=="contentHash") | .value')
LEAF_DESIGNATION=$(echo "$DECODED" | jq -r 'select(.name=="leafDesignation") | .value')
ANCHOR_TYPE=$(echo "$DECODED" | jq -r 'select(.name=="anchorType") | .value')
COMMIT_REF=$(echo "$DECODED" | jq -r 'select(.name=="commitRef") | .value')
BYTE_SIZE=$(echo "$DECODED" | jq -r 'select(.name=="byteSize") | .value | if type=="object" then .hex else . end')
INTEGRITY=$(echo "$DECODED" | jq -r 'select(.name=="integrity") | .value')

# Handle byteSize hex conversion
if [[ "$BYTE_SIZE" == 0x* ]]; then
  BYTE_SIZE=$((BYTE_SIZE))
fi

echo "✅ Attestation fetched"
echo "   contentHash: $CONTENT_HASH"
echo "   leafDesignation: $LEAF_DESIGNATION"
echo "   anchorType: $ANCHOR_TYPE"
echo "   commitRef: $COMMIT_REF"
echo "   byteSize: $BYTE_SIZE"
echo "   integrity: $INTEGRITY"

# Step 4: Clone repo at exact commit
WORK_DIR=$(mktemp -d)
echo "📦 Checking out commit $COMMIT_REF..."
git clone --quiet https://github.com/jsonwisdom/AL.git "$WORK_DIR"
cd "$WORK_DIR"
git checkout --quiet "$COMMIT_REF"

# Step 5: Verify merkle root
BATCH_ROOT=$(jq -r .merkle_root _truth/batches/kb_batch_001.json)
echo "📊 Batch merkle_root: 0x$BATCH_ROOT"

if [ "0x$BATCH_ROOT" != "$CONTENT_HASH" ]; then
  echo "❌ FAIL: Merkle root mismatch"
  echo "   EAS: $CONTENT_HASH"
  echo "   Repo: 0x$BATCH_ROOT"
  exit 1
fi

# Step 6: Verify payload integrity
PAYLOAD_BYTES=$(wc -c < _truth/batches/kb_batch_001_anchor_payload.canonical.json | tr -d ' ')
PAYLOAD_HASH="sha256:$(sha256sum _truth/batches/kb_batch_001_anchor_payload.canonical.json | awk '{print $1}')"

echo "📄 Payload byteSize: $PAYLOAD_BYTES"
echo "🔐 Payload integrity: $PAYLOAD_HASH"

if [ "$PAYLOAD_BYTES" != "$BYTE_SIZE" ]; then
  echo "❌ FAIL: Byte size mismatch"
  echo "   EAS: $BYTE_SIZE"
  echo "   Repo: $PAYLOAD_BYTES"
  exit 1
fi

if [ "$PAYLOAD_HASH" != "$INTEGRITY" ]; then
  echo "❌ FAIL: Integrity mismatch"
  echo "   EAS: $INTEGRITY"
  echo "   Repo: $PAYLOAD_HASH"
  exit 1
fi

# Cleanup
cd /tmp
rm -rf "$WORK_DIR"

echo "----------------------------------------"
echo "✅ EAS_VERIFY_OK uid=$EAS_UID root=$BATCH_ROOT commit=$COMMIT_REF size=$BYTE_SIZE"
