#!/usr/bin/env bash
# =============================================================================
# ALMS Numeric Extractor v1
# Extracts obvious numeric claims from normalized text for Machine Speed ALMS V2.
# Conservative by design: extraction is for replay stability and drift detection,
# not full semantic truth adjudication.
# =============================================================================

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  echo "Minnesota projects a $3.7 billion balance." | scripts/alms_extract_numbers.sh

Outputs JSON:
  {
    "extractor_version": "alms_numeric_extractor_v1",
    "numbers": [...],
    "numbers_hash": "sha256:..."
  }
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -gt 0 ]; then
  echo "ALMS_NUMERIC_EXTRACT_ERROR too_many_arguments" >&2
  usage >&2
  exit 2
fi

TEXT=$(cat)

python3 - "$TEXT" <<'PY'
import hashlib
import json
import re
import sys

text = sys.argv[1]
pattern = re.compile(r'(?P<prefix>[$])?\b(?P<number>\d+(?:,\d{3})*(?:\.\d+)?|\d+)(?P<percent>%)?(?:\s+(?P<scale>billion|million|trillion|thousand))?', re.IGNORECASE)

numbers = []
for match in pattern.finditer(text):
    raw = match.group(0)
    number_raw = match.group('number')
    normalized_number = number_raw.replace(',', '')
    scale = (match.group('scale') or '').lower()
    unit = 'percent' if match.group('percent') else ('usd' if match.group('prefix') else 'number')

    multiplier = {
        'thousand': 1_000,
        'million': 1_000_000,
        'billion': 1_000_000_000,
        'trillion': 1_000_000_000_000,
        '': 1,
    }[scale]

    try:
        value = float(normalized_number) * multiplier
    except ValueError:
        value = None

    numbers.append({
        'raw': raw,
        'number': normalized_number,
        'scale': scale,
        'unit': unit,
        'value': value,
        'start': match.start(),
        'end': match.end(),
    })

canonical = json.dumps(numbers, sort_keys=True, separators=(',', ':'))
digest = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
print(json.dumps({
    'extractor_version': 'alms_numeric_extractor_v1',
    'numbers': numbers,
    'numbers_hash': 'sha256:' + digest,
}, indent=2, sort_keys=True))
PY
