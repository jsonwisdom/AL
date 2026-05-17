#!/bin/bash
set -euo pipefail

echo "🧾 Sovereign Replay Court — Public Oath"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v python3 &> /dev/null; then
    echo "❌ REPLAY_REJECTED: python3 not found"
    exit 1
fi

python3 src/matrix_runner.py
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧾 REPLAY_CONFIRMED | No drift detected"
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️ REPLAY_REJECTED | Drift detected"
fi

exit $exit_code
