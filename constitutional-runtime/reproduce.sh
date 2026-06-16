#!/usr/bin/env bash
set -euo pipefail

npm install
npm run build
npm run replay:valid

set +e
npm run replay:divergent
code=$?
set -e

if [ "$code" -ne 2 ]; then
  echo "Expected divergent receipt to exit 2, got $code"
  exit 1
fi

# === CONTRADICTION CONTROL WITH LINEAGE BINDING ===
echo "→ Testing contradiction receipt with lineage binding (expect CONSTITUTIONAL_CONTRADICTION / exit 2)"
set +e
node dist/cli.js fixtures/contradiction.valid.json fixtures/lineage.valid.json
contradiction_code=$?
set -e

if [ "$contradiction_code" -ne 2 ]; then
  echo "Wrong exit code for lineage-bound contradiction: $contradiction_code"
  exit 1
fi

echo "✅ CONSTITUTIONAL_CONTRADICTION with lineage_tip verified (exit 2)"
echo "🎉 All three constitutional controls verified (MATCH / DIVERGENCE / CONSTITUTIONAL_CONTRADICTION with lineage binding)"
echo "REPRODUCE_OK"
