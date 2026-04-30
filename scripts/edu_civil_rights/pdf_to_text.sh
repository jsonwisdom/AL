#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 INPUT.pdf OUTPUT.txt" >&2
  exit 64
fi

INPUT="$1"
OUTPUT="$2"

pdftotext -layout "$INPUT" "$OUTPUT"
