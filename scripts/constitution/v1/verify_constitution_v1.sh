#!/usr/bin/env bash
set -euo pipefail
FILE="constitution/v1/constitution_v1.canonical.json"
BYTES=$(wc -c < "$FILE")
LAST_BYTE=$(tail -c 1 "$FILE" | od -An -tx1 | tr -d ' \n')
SHA256=$(sha256sum "$FILE" | awk '{print $1}')
SHA3=$(openssl dgst -sha3-256 "$FILE" | awk '{print $2}')
BLAKE3=$(b3sum "$FILE" | awk '{print $1}')
cat > receipts/constitution/v1/constitution_v1_verification_receipt.json <<JSON
{
  "artifact": "constitution/v1/constitution_v1.canonical.json",
  "byte_count": $BYTES,
  "last_byte_hex": "$LAST_BYTE",
  "sha3_256": "$SHA3",
  "sha256": "$SHA256",
  "blake3_256": "$BLAKE3",
  "status": "CANONICAL_RECONCILIATION_VERIFIED",
  "seal": "BLOCKED_PENDING_SIGNATURE",
  "runtime": "BLOCKED",
  "siege": "BLOCKED",
  "authority": "NO_SIGNATURE_NO_ENACTMENT"
}
JSON
cat receipts/constitution/v1/constitution_v1_verification_receipt.json
