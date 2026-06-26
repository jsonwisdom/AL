#!/bin/bash
set -euo pipefail

COURT_ROOT="14d406410f13c7210c20935fa8639b3d8fcbb81f47cd44407506d23391c79547"

if [[ "${1:-}" == "--signature-check" ]]; then
    if [[ -z "${2:-}" ]]; then
        echo "REPLAY_REFUSED: missing envelope path"
        exit 2
    fi
    if ! command -v python3 &> /dev/null; then
        echo "REPLAY_REFUSED: python3 not found"
        exit 2
    fi
    if ! command -v openssl &> /dev/null; then
        echo "REPLAY_REFUSED: openssl not found"
        exit 2
    fi
    python3 contracts/replay/v0.1/verify_envelope_signature.py "$2"
    exit $?
fi

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
