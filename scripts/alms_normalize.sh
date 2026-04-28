#!/usr/bin/env bash
# =============================================================================
# ALMS Normalize Strict v1
# Machine Speed ALMS V2 — Deterministic Normalization Gate
#
# Rule: same input bytes -> identical normalized output + hash.
# No exceptions. No drift. No vibes.
# =============================================================================

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  echo "claim text" | scripts/alms_normalize.sh
  scripts/alms_normalize.sh raw_claim.txt

Outputs JSON:
  {
    "transform_version": "normalize_strict_v1",
    "input_hash": "sha256:...",
    "normalized_hash": "sha256:...",
    "normalized_text": "..."
  }
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -gt 1 ]; then
  echo "ALMS_NORMALIZE_ERROR too_many_arguments" >&2
  usage >&2
  exit 2
fi

if [ "$#" -eq 0 ]; then
  INPUT=$(cat)
else
  if [ ! -f "$1" ]; then
    echo "ALMS_NORMALIZE_ERROR missing_file path=$1" >&2
    exit 2
  fi
  INPUT=$(cat "$1")
fi

# ----------------------------------------------------------------------
# Deterministic Normalization Pipeline: normalize_strict_v1
# ----------------------------------------------------------------------
NORMALIZED=$(printf '%s' "$INPUT" \
  | iconv -f UTF-8 -t UTF-8 -c \
  | tr -s '[:space:]' ' ' \
  | sed 's/[[:cntrl:]]//g' \
  | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# ----------------------------------------------------------------------
# Hashing: SHA-256 with schema-compatible prefix
# ----------------------------------------------------------------------
INPUT_HASH="sha256:$(printf '%s' "$INPUT" | sha256sum | awk '{print $1}')"
NORMALIZED_HASH="sha256:$(printf '%s' "$NORMALIZED" | sha256sum | awk '{print $1}')"

# ----------------------------------------------------------------------
# Output: JSON aligned with contracts/receipt_schema.json
# ----------------------------------------------------------------------
jq -n \
  --arg transform_version "normalize_strict_v1" \
  --arg input_hash "$INPUT_HASH" \
  --arg normalized_hash "$NORMALIZED_HASH" \
  --arg normalized_text "$NORMALIZED" \
  '{
    transform_version: $transform_version,
    input_hash: $input_hash,
    normalized_hash: $normalized_hash,
    normalized_text: $normalized_text
  }'
