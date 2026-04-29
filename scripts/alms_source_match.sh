#!/usr/bin/env bash
# =============================================================================
# ALMS Source Match v1
# Checks whether anchored numeric values from a claim appear in a source excerpt.
#
# This is NOT web/PDF truth verification. It is local excerpt matching:
#   claim numbers -> canonical numeric fingerprint -> source excerpt numbers
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTRACTOR="$SCRIPT_DIR/alms_extract_numbers.sh"

usage() {
  cat <<'EOF'
Usage:
  scripts/alms_source_match.sh claim.txt source_excerpt.txt

Returns JSON with source_match results.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -ne 2 ]; then
  echo "ALMS_SOURCE_MATCH_ERROR expected_claim_and_source_files" >&2
  usage >&2
  exit 2
fi

CLAIM_FILE="$1"
SOURCE_FILE="$2"

if [ ! -f "$CLAIM_FILE" ]; then
  echo "ALMS_SOURCE_MATCH_ERROR missing_claim_file path=$CLAIM_FILE" >&2
  exit 2
fi

if [ ! -f "$SOURCE_FILE" ]; then
  echo "ALMS_SOURCE_MATCH_ERROR missing_source_file path=$SOURCE_FILE" >&2
  exit 2
fi

CLAIM_NUMBERS=$(cat "$CLAIM_FILE" | "$EXTRACTOR")
SOURCE_NUMBERS=$(cat "$SOURCE_FILE" | "$EXTRACTOR")

python3 - "$CLAIM_NUMBERS" "$SOURCE_NUMBERS" <<'PY'
import json
import sys

claim = json.loads(sys.argv[1])
source = json.loads(sys.argv[2])

source_values = set()
for n in source.get('numbers', []):
    source_values.add((n.get('unit'), n.get('base_value'), n.get('scale')))

results = []
for n in claim.get('numbers', []):
    key = (n.get('unit'), n.get('base_value'), n.get('scale'))
    matched = key in source_values
    results.append({
        'index': n.get('index'),
        'raw': n.get('raw'),
        'unit': n.get('unit'),
        'base_value': n.get('base_value'),
        'scale': n.get('scale'),
        'source_anchor': n.get('source_anchor'),
        'matched': matched,
    })

passed = all(r['matched'] for r in results) if results else True
print(json.dumps({
    'checker_version': 'alms_source_match_v1',
    'passed': passed,
    'results': results,
}, indent=2, sort_keys=True))
PY
