#!/usr/bin/env bash
set -euo pipefail

VCLP_VERIFY="docs/protocols/vclp/verify.sh"
LEDGER="_truth/ledger.jsonl"
PATTERNS="_truth/patterns.json"

echo "=== AL Verification via VCLP ==="

if [[ ! -x "$VCLP_VERIFY" ]]; then
  echo "✗ VCLP verifier missing or not executable: $VCLP_VERIFY"
  exit 1
fi

"$VCLP_VERIFY" "$LEDGER" "$PATTERNS"
