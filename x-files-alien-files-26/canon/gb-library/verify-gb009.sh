#!/bin/bash
# Automated SHA-256 verification for GB-009 Replay Reston

COMMIT="d2c56febb931c701f9bac88464fb28aec9eb0910"
FILE="x-files-alien-files-26/canon/gb-library/GB-009-replay-reston.md"
EXPECTED="e5cc313f26bbcd97958bd9907f71889d9a6f813bc715d549b523a9cb6b590d90"

echo "Verifying GB-009 at commit $COMMIT"
git checkout "$COMMIT" 2>/dev/null || { echo "Checkout failed"; exit 1; }

ACTUAL=$(sha256sum "$FILE" | awk '{print $1}')
echo "Actual SHA256: $ACTUAL"

echo "Expected: $EXPECTED"
if [ "$ACTUAL" = "$EXPECTED" ]; then
  echo "✅ GB-009 Canon Verified - Full replay fidelity"
  exit 0
else
  echo "❌ Mismatch - Tamper detected"
  exit 1
fi