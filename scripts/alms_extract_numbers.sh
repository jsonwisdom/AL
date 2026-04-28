#!/usr/bin/env bash
# =============================================================================
# ALMS Numeric Extractor v1
# Extracts and canonicalizes obvious numeric claims for Machine Speed ALMS V2.
#
# Guarantees:
#   - strips numeric formatting noise such as commas
#   - canonicalizes decimals such as 3.70 -> 3.7
#   - normalizes common scale words and abbreviations into base_value
#   - preserves appearance order for deterministic replay
#
# This is still not external truth verification. It is numeric meaning locking.
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
from decimal import Decimal, InvalidOperation, getcontext
import hashlib
import json
import re
import sys

getcontext().prec = 50
text = sys.argv[1]

scale_aliases = {
    'k': 'thousand',
    'thousand': 'thousand',
    'm': 'million',
    'mm': 'million',
    'mn': 'million',
    'million': 'million',
    'b': 'billion',
    'bn': 'billion',
    'billion': 'billion',
    't': 'trillion',
    'tn': 'trillion',
    'trillion': 'trillion',
    '': '',
}

scale_multipliers = {
    '': Decimal('1'),
    'thousand': Decimal('1000'),
    'million': Decimal('1000000'),
    'billion': Decimal('1000000000'),
    'trillion': Decimal('1000000000000'),
}

pattern = re.compile(
    r'(?P<prefix>[$])?'
    r'(?<![A-Za-z0-9.])'
    r'(?P<number>\d+(?:,\d{3})*(?:\.\d+)?|\d*\.\d+)'
    r'(?P<percent>%)?'
    r'(?:\s*(?P<scale>thousand|million|billion|trillion|bn|mn|mm|tn|k|m|b|t))?'
    r'(?![A-Za-z0-9])',
    re.IGNORECASE,
)

def canonical_decimal(value: Decimal) -> str:
    if value == value.to_integral_value():
        return str(value.quantize(Decimal('1')))
    return format(value.normalize(), 'f')

numbers = []
for idx, match in enumerate(pattern.finditer(text)):
    raw = match.group(0)
    number_raw = match.group('number')
    cleaned = number_raw.replace(',', '')
    percent = bool(match.group('percent'))
    scale_raw = (match.group('scale') or '').lower()
    scale = scale_aliases.get(scale_raw, scale_raw)

    try:
        value_decimal = Decimal(cleaned)
    except InvalidOperation:
        continue

    unit = 'percent' if percent else ('usd' if match.group('prefix') else 'number')
    multiplier = Decimal('1') if percent else scale_multipliers.get(scale, Decimal('1'))
    base_value_decimal = value_decimal * multiplier

    number_obj = {
        'index': idx,
        'raw': raw,
        'canonical_number': canonical_decimal(value_decimal),
        'scale': scale,
        'unit': unit,
        'base_value': canonical_decimal(base_value_decimal),
        'start': match.start(),
        'end': match.end(),
    }
    numbers.append(number_obj)

# Hash only canonical semantic numeric tuples, preserving appearance order.
# Raw/start/end remain in output for audit, but are excluded from numbers_hash
# so harmless formatting drift does not break numeric equivalence.
fingerprint = [
    {
        'index': n['index'],
        'unit': n['unit'],
        'base_value': n['base_value'],
        'scale': n['scale'],
    }
    for n in numbers
]
canonical = json.dumps(fingerprint, sort_keys=True, separators=(',', ':'))
digest = hashlib.sha256(canonical.encode('utf-8')).hexdigest()

print(json.dumps({
    'extractor_version': 'alms_numeric_extractor_v1',
    'numbers': numbers,
    'numbers_fingerprint': fingerprint,
    'numbers_hash': 'sha256:' + digest,
}, indent=2, sort_keys=True))
PY
