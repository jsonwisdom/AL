#!/usr/bin/env bash
set -euo pipefail

# Coinbase MCP Adapter V1
# Doctrine: preview-first, receipt-first, human-gated, no fake green.
# Default mode never moves funds.

MODE="${1:-preview}" # preview | approved-live
PAIR="${PAIR:-BTC-USD}"
AMOUNT_USD="${AMOUNT_USD:-1.00}"
RECEIPTS_DIR="${RECEIPTS_DIR:-receipts/coinbase-agent}"
IDENTITY_WITNESS="${IDENTITY_WITNESS:-jaywisdom.base.eth}"
TS="$(date -u +%Y%m%d-%H%M%S)"

mkdir -p "$RECEIPTS_DIR"

PREVIEW_FILE="$RECEIPTS_DIR/coinbase_mcp_preview_${TS}.json"
APPROVAL_FILE="$RECEIPTS_DIR/coinbase_mcp_approval_${TS}.json"
LIVE_FILE="$RECEIPTS_DIR/coinbase_mcp_live_${TS}.json"

echo "COINBASE_MCP_ADAPTER_V1"
echo "MODE=$MODE"
echo "PAIR=$PAIR"
echo "AMOUNT_USD=$AMOUNT_USD"
echo "IDENTITY_WITNESS=$IDENTITY_WITNESS"

if ! command -v coinbase >/dev/null 2>&1; then
  cat > "$PREVIEW_FILE" <<EOF
{
  "adapter": "coinbase_mcp_adapter_v1",
  "status": "REJECTED",
  "failure_class": "CLI_MISSING",
  "reason": "coinbase CLI not found on PATH",
  "pair": "$PAIR",
  "amount_usd": "$AMOUNT_USD",
  "identity_witness": "$IDENTITY_WITNESS",
  "funds_moved": false
}
EOF
  sha256sum "$PREVIEW_FILE" > "$PREVIEW_FILE.sha256"
  echo "CLI_MISSING_RECEIPT_EMITTED=$PREVIEW_FILE"
  exit 127
fi

# Preview only: product/market lookup. This must not move funds.
if ! coinbase products get "$PAIR" > "$PREVIEW_FILE"; then
  sha256sum "$PREVIEW_FILE" > "$PREVIEW_FILE.sha256"
  echo "PREVIEW_FAILED_RECEIPT_EMITTED=$PREVIEW_FILE"
  exit 1
fi

sha256sum "$PREVIEW_FILE" > "$PREVIEW_FILE.sha256"
PREVIEW_SHA256="$(cut -d ' ' -f1 "$PREVIEW_FILE.sha256")"

cat > "$APPROVAL_FILE" <<EOF
{
  "adapter": "coinbase_mcp_adapter_v1",
  "mode": "$MODE",
  "pair": "$PAIR",
  "amount_usd": "$AMOUNT_USD",
  "identity_witness": "$IDENTITY_WITNESS",
  "preview_receipt": "$PREVIEW_FILE",
  "preview_sha256": "$PREVIEW_SHA256",
  "human_approval_required": true,
  "approved": false,
  "funds_moved": false,
  "doctrine": "PREVIEW_FIRST_RECEIPT_FIRST_HUMAN_GATED"
}
EOF

sha256sum "$APPROVAL_FILE" > "$APPROVAL_FILE.sha256"

case "$MODE" in
  preview)
    echo "PREVIEW_COMPLETE"
    echo "APPROVAL_RECEIPT=$APPROVAL_FILE"
    exit 0
    ;;
  approved-live)
    if ! jq -e '.approved == true' "$APPROVAL_FILE" >/dev/null 2>&1; then
      cat > "$LIVE_FILE" <<EOF
{
  "adapter": "coinbase_mcp_adapter_v1",
  "status": "BLOCKED",
  "failure_class": "HUMAN_APPROVAL_MISSING",
  "approval_receipt": "$APPROVAL_FILE",
  "funds_moved": false
}
EOF
      sha256sum "$LIVE_FILE" > "$LIVE_FILE.sha256"
      echo "LIVE_BLOCKED_NO_FUNDS_MOVED=$LIVE_FILE"
      exit 2
    fi

    echo "LIVE PAYMENT CALL NOT IMPLEMENTED IN V1 SAFETY HARNESS"
    echo "NO_FUNDS_MOVED"
    exit 3
    ;;
  *)
    echo "ERROR: invalid mode. Use preview or approved-live."
    exit 64
    ;;
esac
