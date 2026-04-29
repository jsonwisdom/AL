#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "HUMAN_IN_THE_LOOP_GATE_V1"
echo "human_operator=Jason"
echo "assistant=ChatGPT"
echo "infrastructure=Microsoft"
echo "status=CURRENT"
echo "preview_script_locked=true"
echo "live_script_created=false"
echo "signer_authorized=false"
echo "tx_authorized=false"
echo "required_next=REAL_ROOT_PREVIEW_WITNESS"
echo "verdict=HOLD"
