#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "HUMAN_IN_THE_LOOP_GATE_V2"
echo "human_operator=Jason"
echo "assistant=ChatGPT"
echo "infrastructure=Microsoft,GoogleCloudShell,Base"
echo "schema_uid=0x879d4e37dcd2fe24f977b78f7e8628902af9a54896cb731f5ee7c9e4f5b78c97"
echo "schema_status=NOT_YET_LIVE"
echo "attestation_blocked=true"
echo "signer_authorized=false"
echo "tx_authorized=false"
echo "required_next=JASON_SCHEMA_REGISTRATION_AUTHORIZATION"
echo "verdict=HOLD"
