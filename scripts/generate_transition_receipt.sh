#!/usr/bin/env bash
set -euo pipefail

FROM="${2:-HEARTBEAT_STABLE}"
TO="${4:-READY_FOR_CEREMONY}"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

mkdir -p _truth/governance

cat > "_truth/governance/HEARTBEAT_STABLE_TO_READY_RECEIPT.json" <<EOF
{
  "receipt_id": "HEARTBEAT_STABLE_TO_READY",
  "track": "TRACK_001",
  "transition": "${FROM} → ${TO}",
  "trigger": "observed_consecutive_green_commits >= 3",
  "timestamp_utc": "${TIMESTAMP}",
  "state_machine_position": {
    "previous": "${FROM}",
    "current": "${TO}",
    "next": "CEREMONY_IN_PROGRESS"
  },
  "verifier": "verifier/src/ceremony/receipt.rs"
}
EOF
