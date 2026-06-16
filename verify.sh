#!/bin/bash
set -euo pipefail

COURT_ROOT="14d406410f13c7210c20935fa8639b3d8fcbb81f47cd44407506d23391c79547"

echo "🧾 Sovereign Replay Court — Public Oath"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode: Stranger-Friendly Verification"

if ! command -v python3 &> /dev/null; then
    echo "❌ REPLAY_REJECTED: python3 not found"
    exit 1
fi

python3 src/matrix_runner.py
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧾 REPLAY_CONFIRMED | No drift detected"
    echo "ROOT: ${COURT_ROOT}"
    echo "MATRIX: GREEN"
    echo "Execution ≡ Registry holds."
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️ REPLAY_REJECTED | Drift detected"
fi

exit $exit_code
