#!/usr/bin/env bash
set -euo pipefail

# Poster 3 Sepolia Human Runbook
# This script is intentionally interactive. It does not store private keys.
# It prints the exact receipts Jay needs to paste back.

CIRCUIT_SOURCE_HASH="0x3333333333333333333333333333333333333333333333333333333333333333"
RECEIPT_HASH="0xe072bd91b31cb2e24eb6c3f561501f79adb705bcb6bb074bacf3b4e686e50ba0"
ENV_HASH="0x1111111111111111111111111111111111111111111111111111111111111111"
AUDIT_SCHEMA_HASH="0x2222222222222222222222222222222222222222222222222222222222222222"
TIER="PARTIAL_DETERMINISTIC"
STABILITY_INDEX="65"

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1"; exit 1; }
}

need forge
need cast
need jq

echo "=== Poster 3 Sepolia Promotion ==="
echo "This uses Foundry/cast. Do NOT paste private keys into chat."
echo

read -r -p "Sepolia RPC URL: " SEPOLIA_RPC
read -r -p "DEPLOYER private key env var name, e.g. DEPLOYER_PK: " DEPLOYER_PK_VAR
read -r -p "MARSHAL private key env var name, e.g. MARSHAL_PK: " MARSHAL_PK_VAR
read -r -p "COMMITTEE private key env var name, e.g. COMMITTEE_PK: " COMMITTEE_PK_VAR

DEPLOYER_PK="${!DEPLOYER_PK_VAR:-}"
MARSHAL_PK="${!MARSHAL_PK_VAR:-}"
COMMITTEE_PK="${!COMMITTEE_PK_VAR:-}"

if [[ -z "$DEPLOYER_PK" || -z "$MARSHAL_PK" || -z "$COMMITTEE_PK" ]]; then
  echo "One or more private-key env vars are empty. Export them first, then rerun."
  echo "Example: export DEPLOYER_PK='0x...'"
  exit 1
fi

MARSHAL_ADDRESS=$(cast wallet address --private-key "$MARSHAL_PK")
COMMITTEE_ADDRESS=$(cast wallet address --private-key "$COMMITTEE_PK")

echo
printf 'marshal_address: %s\n' "$MARSHAL_ADDRESS"
printf 'committee_address: %s\n' "$COMMITTEE_ADDRESS"
echo

echo "[1/5] Deploying SovereignCanonical..."
DEPLOY_OUT=$(forge create contracts/SovereignCanonical_v2_2.sol:SovereignCanonical \
  --constructor-args "$MARSHAL_ADDRESS" \
  --rpc-url "$SEPOLIA_RPC" \
  --private-key "$DEPLOYER_PK" \
  --json)

echo "$DEPLOY_OUT" | jq .
SEPOLIA_CONTRACT_ADDRESS=$(echo "$DEPLOY_OUT" | jq -r '.deployedTo // .contractAddress // empty')
DEPLOYMENT_TX_HASH=$(echo "$DEPLOY_OUT" | jq -r '.transactionHash // .txHash // empty')

if [[ -z "$SEPOLIA_CONTRACT_ADDRESS" || "$SEPOLIA_CONTRACT_ADDRESS" == "null" ]]; then
  echo "Could not parse deployed contract address from forge output. Copy it manually from output above."
  exit 1
fi

echo "[2/5] Adding veto committee member..."
ADD_VETO_TX=$(cast send "$SEPOLIA_CONTRACT_ADDRESS" \
  "addVetoMember(address)" \
  "$COMMITTEE_ADDRESS" \
  --rpc-url "$SEPOLIA_RPC" \
  --private-key "$MARSHAL_PK" \
  --json | jq -r '.transactionHash')

echo "[3/5] Signing EIP-712 payload..."
TMP_TYPED_DATA=$(mktemp)
cat > "$TMP_TYPED_DATA" <<EOF
{
  "types": {
    "EIP712Domain": [
      {"name":"name","type":"string"},
      {"name":"version","type":"string"},
      {"name":"chainId","type":"uint256"},
      {"name":"verifyingContract","type":"address"}
    ],
    "BuildPromotion": [
      {"name":"circuitSourceHash","type":"bytes32"},
      {"name":"receiptHash","type":"bytes32"},
      {"name":"vetoTriggered","type":"bool"}
    ]
  },
  "primaryType": "BuildPromotion",
  "domain": {
    "name": "SovereignCanonical",
    "version": "2",
    "chainId": 11155111,
    "verifyingContract": "$SEPOLIA_CONTRACT_ADDRESS"
  },
  "message": {
    "circuitSourceHash": "$CIRCUIT_SOURCE_HASH",
    "receiptHash": "$RECEIPT_HASH",
    "vetoTriggered": false
  }
}
EOF

EIP712_SIGNATURE=$(cast wallet sign --no-hash --data "$(cat "$TMP_TYPED_DATA")" --private-key "$COMMITTEE_PK")
rm -f "$TMP_TYPED_DATA"

echo "[4/5] Calling promoteBuild..."
PROMOTE_TX=$(cast send "$SEPOLIA_CONTRACT_ADDRESS" \
  "promoteBuild(bytes32,bytes32,bytes32,string,bytes32,uint256,bytes)" \
  "$CIRCUIT_SOURCE_HASH" \
  "$RECEIPT_HASH" \
  "$ENV_HASH" \
  "$TIER" \
  "$AUDIT_SCHEMA_HASH" \
  "$STABILITY_INDEX" \
  "$EIP712_SIGNATURE" \
  --rpc-url "$SEPOLIA_RPC" \
  --private-key "$MARSHAL_PK" \
  --json | jq -r '.transactionHash')

echo "[5/5] Replaying getCanonicalBuild..."
REPLAY_OUTPUT=$(cast call "$SEPOLIA_CONTRACT_ADDRESS" \
  "getCanonicalBuild(bytes32)(bytes32,bytes32,bytes32,bytes32,uint64,uint8,bool)" \
  "$CIRCUIT_SOURCE_HASH" \
  --rpc-url "$SEPOLIA_RPC")

echo
cat <<EOF
=== COPY THESE RECEIPTS BACK ===
sepolia_contract_address: $SEPOLIA_CONTRACT_ADDRESS
deployment_tx_hash: $DEPLOYMENT_TX_HASH
committee_address: $COMMITTEE_ADDRESS
addVetoMember_tx_hash: $ADD_VETO_TX
eip712_signature: $EIP712_SIGNATURE
promote_tx_hash: $PROMOTE_TX
getCanonicalBuild_output: $REPLAY_OUTPUT
EOF
