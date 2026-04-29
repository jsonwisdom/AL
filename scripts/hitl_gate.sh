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
echo "required_next=JASON_LIVE_AUTHORIZATION"
echo "witness=_truth/attest/base_alms_attest_2026_04_v2_preview_20260429T191530Z.txt"
echo "verdict=HOLD"
