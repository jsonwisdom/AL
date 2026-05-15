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

# === OBSERVER REGISTRY TESTS ===
echo "→ Running observer registry evaluator tests"
node dist/observer-registry.test.js
echo "✅ ObserverRegistry pure evaluator tests passed"

# === OBSERVER REGISTRY OBSERVABILITY ===
echo "→ Testing observer-registry observability in validator"
registry_result=$(node dist/cli.js fixtures/observer-registry.valid.json fixtures/lineage.valid.json)
registry_total_active=$(echo "$registry_result" | grep -o '"totalActive": [0-9]*' | head -n 1 | cut -d':' -f2 | tr -d ' ' || true)
registry_total_revoked=$(echo "$registry_result" | grep -o '"totalRevoked": [0-9]*' | head -n 1 | cut -d':' -f2 | tr -d ' ' || true)
registry_observer_count=$(echo "$registry_result" | grep -o '"observerCount": [0-9]*' | head -n 1 | cut -d':' -f2 | tr -d ' ' || true)
registry_replay_len=$(echo "$registry_result" | grep -o '"replayPathLength": [0-9]*' | head -n 1 | cut -d':' -f2 | tr -d ' ' || true)
registry_consistent_totals=$(echo "$registry_result" | grep -o '"hasConsistentTotals": true' | cut -d':' -f2 | tr -d ' ' || true)

if [ "$registry_total_active" = "2" ] && [ "$registry_total_revoked" = "1" ] && [ "$registry_observer_count" = "3" ] && [ "$registry_replay_len" = "3" ] && [ "$registry_consistent_totals" = "true" ]; then
  echo "✅ Observer registry observability verified"
  echo "   totalActive=${registry_total_active}, totalRevoked=${registry_total_revoked}, observerCount=${registry_observer_count}"
  echo "   replayPathLength=${registry_replay_len}, hasConsistentTotals=true"
  echo "   visible context ≠ authoritative settlement"
else
  echo "❌ Registry observability assertion failed"
  echo "$registry_result"
  exit 1
fi

# === OBSERVER TRANSITION LINEAGE CONSISTENCY OBSERVABILITY ===
echo "→ Testing observer transition lineage consistency observability"
transition_result=$(node dist/cli.js fixtures/observer.revoked.json fixtures/lineage.valid.json)
transition_reason=$(echo "$transition_result" | grep -o '"reason": "observer_resolved_with_placeholder_key"' | cut -d'"' -f4 || true)
transition_consistency=$(echo "$transition_result" | grep -o '"isConsistent": true' | cut -d':' -f2 | tr -d ' ' || true)
transition_valid_binding=$(echo "$transition_result" | grep -o '"hasValidLineageBinding": true' | cut -d':' -f2 | tr -d ' ' || true)

if [ "$transition_reason" = "observer_resolved_with_placeholder_key" ] && [ "$transition_consistency" = "true" ] && [ "$transition_valid_binding" = "true" ]; then
  echo "✅ Lineage binding + placeholder observer resolution verified"
  echo "   hasValidLineageBinding=true (structural binding enforced)"
  echo "   isConsistent=true (synthetic placeholder observer; not authoritative registry state)"
else
  echo "❌ Lineage consistency observability failed"
  echo "$transition_result"
  exit 1
fi

# === RESOLVED OBSERVER OBSERVABILITY ===
echo "→ Testing resolvedObserver visibility in validator"
resolved_observer_available=$(echo "$transition_result" | grep -o '"resolvedObserverAvailable": true' | cut -d':' -f2 | tr -d ' ' || true)
placeholder_source=$(echo "$transition_result" | grep -o '"public_key_source": "placeholder"' | cut -d'"' -f4 || true)

if [ "$resolved_observer_available" = "true" ] && [ "$placeholder_source" = "placeholder" ]; then
  echo "✅ resolvedObserver visibility confirmed"
  echo "   resolvedObserverAvailable=true"
  echo "   public_key_source=placeholder (synthetic)"
  echo "   Context is visible (no registry authority yet)"
else
  echo "❌ resolvedObserver visibility assertion failed"
  echo "$transition_result"
  exit 1
fi

# === OBSERVER TRANSITION REPLAY-PATH VISIBILITY ===
echo "→ Testing replay-path visibility in observer transition"
transition_replay_path_length=$(echo "$transition_result" | grep -o '"replayPathLength": [0-9]*' | head -n 1 | cut -d':' -f2 | tr -d ' ' || true)

if [ -n "$transition_replay_path_length" ]; then
  echo "✅ Replay-path visibility confirmed (replayPathLength=${transition_replay_path_length})"
  echo "   Context is visible, not enforced"
else
  echo "❌ Replay-path visibility failed"
  echo "$transition_result"
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

echo "🎉 All controls and evaluator tests verified (MATCH / DIVERGENCE / CONSTITUTIONAL_CONTRADICTION + observer transitions + observer registry)"
echo "REPRODUCE_OK"
