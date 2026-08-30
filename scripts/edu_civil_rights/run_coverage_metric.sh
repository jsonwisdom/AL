#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/edu_civil_rights/national/coverage.json"
mkdir -p "$(dirname "$OUT")"

python3 scripts/edu_civil_rights/coverage_metric.py > "$OUT"
