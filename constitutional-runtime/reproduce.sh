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

# === OBSERVER TRANSITION TESTS ===
echo "→ Running observer transition evaluator tests"
node dist/observer-transition.test.js
echo "✅ ObserverTransition pure evaluator tests passed"

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

# === REVOKED OBSERVER NEGATIVE CONTROL ===
echo "→ Testing contradiction with REVOKED observer (expect INSUFFICIENT_EVIDENCE / exit 4)"
set +e
revoked_result=$(node dist/cli.js fixtures/contradiction.revoked-observer.json fixtures/lineage.valid.json)
revoked_code=$?
set -e

if [ "$revoked_code" -ne 4 ]; then
  echo "Wrong exit code for revoked-observer case: $revoked_code (expected 4)"
  echo "$revoked_result"
  exit 1
fi

revoked_verdict=$(echo "$revoked_result" | grep -o '"verdict": "[^"]*"' | cut -d'"' -f4)
if [ "$revoked_verdict" != "INSUFFICIENT_EVIDENCE" ]; then
  echo "Wrong verdict: $revoked_verdict (expected INSUFFICIENT_EVIDENCE)"
  echo "$revoked_result"
  exit 1
fi

active_count=$(echo "$revoked_result" | grep -o '"activeObserverCount": [0-9]*' | cut -d':' -f2 | tr -d ' ' || echo "0")
echo "✅ INSUFFICIENT_EVIDENCE verified (exit 4, activeObserverCount=${active_count})"

echo "🎉 All controls and transition tests verified (MATCH / DIVERGENCE / CONSTITUTIONAL_CONTRADICTION + observer transitions)"
echo "REPRODUCE_OK"
