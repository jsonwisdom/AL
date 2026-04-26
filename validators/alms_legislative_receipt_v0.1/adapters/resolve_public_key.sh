#!/usr/bin/env bash
set -euo pipefail

ENS_NAME="${1:-}"
TEXT_KEY="${2:-alms.public_key}"
ETH_RPC_URL="${ETH_RPC_URL:-https://ethereum.publicnode.com}"

[ -z "$ENS_NAME" ] && { echo ""; exit 0; }

REGISTRY="0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"

RESOLVER=$(cast call "$REGISTRY" \
  "resolver(bytes32)(address)" \
  "$(cast namehash "$ENS_NAME")" \
  --rpc-url "$ETH_RPC_URL" 2>/dev/null || true)

if [ -z "$RESOLVER" ] || [ "$RESOLVER" = "0x0000000000000000000000000000000000000000" ]; then
  echo ""
  exit 0
fi

RAW=$(cast call "$RESOLVER" \
  "text(bytes32,string)(string)" \
  "$(cast namehash "$ENS_NAME")" \
  "$TEXT_KEY" \
  --rpc-url "$ETH_RPC_URL" 2>/dev/null || true)

printf '%s\n' "$RAW" | sed 's/^"//; s/"$//'
