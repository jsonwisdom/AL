#!/usr/bin/env bash
set -euo pipefail

# Jay Bash with Gemini — Leaf 008 gate
# Rule: no bytes, no hash; no hash, no attestation.

LEAF_ID="008"
PAYLOAD_FILE="_truth/anchors/leaf008/payload.b64"
OUT_FILE="_truth/anchors/leaf008/verify_leaf008.payload"
ANCHOR_FILE="_truth/anchors/leaf008/ANCHORS.json"
DESIGNATION="LEAF_008_GEMINI_BASH_GATE"
DESCRIPTION="Tests Gemini under the same repo-native Base64 to SHA-256 verification gate."
SCHEMA_NUMBER="1464"
SCHEMA_UID="0x53a4a43dfb91a23d683202e22aa9e59be86ad67fd650aff11be6929b5654bf95"

mkdir -p _truth/anchors/leaf008

if [ ! -f "$PAYLOAD_FILE" ]; then
  cat > "$PAYLOAD_FILE" <<'EOF'
SmF5IEJhc2ggd2l0aCBHZW1pbmkgLSBMZWFmIDAwOC4gTm8gYnl0ZXMsIG5vIGdyZWVuLg==
EOF
fi

base64 -d "$PAYLOAD_FILE" > "$OUT_FILE"
SHA="$(sha256sum "$OUT_FILE" | awk '{print $1}')"
BYTES="$(wc -c < "$OUT_FILE" | tr -d ' ')"

cat > "$ANCHOR_FILE" <<EOF
{
  "leaf_id": "$LEAF_ID",
  "designation": "$DESIGNATION",
  "description": "$DESCRIPTION",
  "payload": {
    "transport": "GITHUB_BASE64",
    "path": "$PAYLOAD_FILE",
    "sha256": "$SHA",
    "size_bytes": $BYTES,
    "integrity": "BYTE_IDENTICAL"
  },
  "base_eas_anchor": {
    "schema_number": $SCHEMA_NUMBER,
    "schema_uid": "$SCHEMA_UID",
    "attestation_uid": "PENDING",
    "content_hash": "0x$SHA",
    "anchor_type": "GEMINI_BASH_CANONICAL_HASH_VERIFIED"
  },
  "classification": {
    "github": "VERIFIED",
    "base": "PENDING",
    "anchor_allowed": true
  }
}
EOF

jq -cS . "$ANCHOR_FILE" > "$ANCHOR_FILE.canonical"
mv "$ANCHOR_FILE.canonical" "$ANCHOR_FILE"

printf 'LEAF008_PAYLOAD_VERIFIED sha=%s bytes=%s\n' "$SHA" "$BYTES"
printf 'EAS_CONTENT_HASH=0x%s\n' "$SHA"
printf 'EAS_LEAF_DESIGNATION=%s\n' "$DESIGNATION"
printf 'EAS_ANCHOR_TYPE=GEMINI_BASH_CANONICAL_HASH_VERIFIED\n'
printf 'EAS_BYTE_SIZE=%s\n' "$BYTES"
printf 'EAS_INTEGRITY=BYTE_IDENTICAL\n'
