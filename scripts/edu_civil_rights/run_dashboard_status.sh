#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/edu_civil_rights/national/dashboard_state_status.json"
mkdir -p "$(dirname "$OUT")"

python3 scripts/edu_civil_rights/dashboard_state_status.py > "$OUT"
