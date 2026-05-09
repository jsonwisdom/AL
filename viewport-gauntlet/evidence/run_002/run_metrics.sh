#!/bin/bash
set -euo pipefail

RUN_JSON="viewport-gauntlet/evidence/run_002/run_002.json"
OUTPUT="viewport-gauntlet/evidence/run_002/metrics_output.txt"

if [ ! -f "$RUN_JSON" ]; then
  echo "Missing: $RUN_JSON"
  exit 1
fi

python viewport-gauntlet/metrics.py "$RUN_JSON" | tee "$OUTPUT"
