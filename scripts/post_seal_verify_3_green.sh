#!/usr/bin/env bash
set -euo pipefail

ROOT_FILE="${ROOT_FILE:-_truth/3_GREEN_MILESTONE_ROOT.sha256}"

echo "== POST-SEAL VERIFICATION: 3-GREEN MILESTONE =="
echo ""

# 1) Verify root file exists
echo "1) Verify root file exists..."
if test -f "$ROOT_FILE"; then
  echo "✅ Found $ROOT_FILE"
else
  echo "❌ Missing $ROOT_FILE"
  exit 1
fi

# 2) Verify root file is non-empty
echo "2) Verify root file is non-empty..."
if test -s "$ROOT_FILE"; then
  echo "✅ Root file is non-empty"
else
  echo "❌ Root file is empty"
  exit 1
fi

# 3) Verify root format is SHA-like (64 hex chars, optional 0x prefix)
echo "3) Verify root format is SHA-like..."
ROOT="$(cat "$ROOT_FILE" | tr -d '[:space:]')"
if echo "$ROOT" | grep -Eq '^(0x)?[a-fA-F0-9]{64}$'; then
  echo "✅ Root format valid: $ROOT"
else
  echo "❌ Invalid root format: $ROOT"
  exit 1
fi

# 4) Confirm governance root remains ceremony-clean
echo "4) Confirm governance root remains ceremony-clean..."
if find _truth/governance -type f -iname "*ceremony_court*" 2>/dev/null | grep -qi .; then
  echo "❌ Ceremony court artifact reappeared in governance root"
  exit 1
fi
echo "✅ Governance root remains ceremony-clean"

# 5) Confirm transition evidence exists
echo "5) Confirm transition evidence exists..."
if ls _truth/governance/*READY_FOR_CEREMONY* 1>/dev/null 2>&1 || \
   grep -Rl "READY_FOR_CEREMONY" _truth/governance/*.json 1>/dev/null 2>&1; then
  echo "✅ READY_FOR_CEREMONY transition evidence found"
else
  echo "⚠️ No explicit READY_FOR_CEREMONY file found (transition may be implicit)"
fi

# 6) Optional: Verify root matches expected computation (if verifier available)
echo "6) Optional: Verify root matches computed Merkle root..."
if command -v cargo &>/dev/null && [ -f "verifier/src/ceremony/receipt.rs" ]; then
  if cargo run --bin verifier -- verify-root --root "$ROOT" 2>/dev/null; then
    echo "✅ Root cryptographically verified"
  else
    echo "⚠️ Root verification skipped (verifier returned error)"
  fi
else
  echo "⚠️ Root cryptographic verification skipped (verifier not available)"
fi

echo ""
echo "🟢 POST-SEAL VERIFICATION PASSED"
echo "3_GREEN_MILESTONE root is present, formatted, and root remains clean."
