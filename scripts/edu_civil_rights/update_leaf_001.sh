#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 INPUT.json" >&2
  exit 64
fi

INPUT="$1"

python3 scripts/edu_civil_rights/populate_mn_leaf_001.py < "$INPUT"
