#!/usr/bin/env bash
set -euo pipefail

# ALMS Base Attestation Preview Generator (No-Signer Edition)
# Version: 2.0.0
# Target: Base Mainnet EAS

MERKLE_ROOT="${MERKLE_ROOT:-}"

if [[ ! "$MERKLE_ROOT" =~ ^0x[0-9a-fA-F]{64}$ ]]; then
    echo "ERROR: MERKLE_ROOT must be 0x-prefixed 32-byte hex string"
    exit 1
fi

SCHEMA_UID="0x40367a8c4b68ebd564d3e0558d417fb209a82d33622761a3c804a74ce02120d3" # Example ALMS Schema
FUNC_SIG="attest((bytes32,uint64,bool,bytes32,bytes,uint256))"

TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
OUTPUT_DIR="_truth/attest"
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/base_alms_attest_2026_04_v2_preview_$TIMESTAMP.txt"

# Constructing a simulated EAS payload for preview
# (schema, expirationTime, revocable, refUID, data, value)
# Here we just pack the key info into a human-readable and machine-verifiable format.

cat > "$OUTPUT_FILE" <<OUT
ALMS_ATTEST_PREVIEW_V2
network=base
schema_uid=$SCHEMA_UID
merkle_root=$MERKLE_ROOT
func_sig=$FUNC_SIG
request=eth_sendTransaction
data=0x[ENCODED_EAS_DATA_FOR_ROOT_$MERKLE_ROOT]
NO_SIGNER_USED
NO_TX_SENT
TIMESTAMP=$TIMESTAMP
OUT

echo "PREVIEW_CREATED=$OUTPUT_FILE"
