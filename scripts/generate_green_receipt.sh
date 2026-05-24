#!/usr/bin/env bash
set -euo pipefail

if [ "${GITHUB_EVENT_WORKFLOW_CONCLUSION:-}" != "success" ]; then
  echo "Refusing to issue GREEN receipt: workflow conclusion is not success"
  exit 1
fi

NUMBER="${2:-1}"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
PADDED="$(printf "%03d" "$NUMBER")"

mkdir -p _truth/governance

cat > "_truth/governance/HEARTBEAT_COURT_GREEN_RECEIPT_${PADDED}.json" <<EOF
{
  "receipt_id": "HEARTBEAT_COURT_GREEN_${PADDED}",
  "track": "TRACK_001",
  "status": "GREEN",
  "issued_by": "AL Verifier Bot",
  "timestamp_utc": "${TIMESTAMP}",
  "constitutional_epoch_boundary": "fab0e39388aa37c971ab4d172f189173e19b1d9b"
}
EOF
