#!/usr/bin/env bash
# =============================================================================
# ALMS Verify Engine — Machine Speed ALMS V2
#
# Truth executor: replay normalization, validate hashes, apply invariant scaffold,
# determine verdict, and emit a tamper-evident receipt.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NORMALIZER="$PROJECT_ROOT/scripts/alms_normalize.sh"
INVARIANTS_FILE="$PROJECT_ROOT/contracts/invariants/v1.json"

usage() {
  cat <<'EOF'
Usage:
  echo "claim text" | scripts/alms_verify.sh
  scripts/alms_verify.sh _truth/receipts/ALMS-MS-001.json

Modes:
  stdin raw claim  -> generate receipt
  receipt file     -> replay receipt and verify hash stability
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -gt 1 ]; then
  echo "ALMS_VERIFY_ERROR too_many_arguments" >&2
  usage >&2
  exit 2
fi

if [ ! -x "$NORMALIZER" ]; then
  echo "ALMS_VERIFY_ERROR normalizer_not_executable path=$NORMALIZER" >&2
  exit 2
fi

if [ ! -f "$INVARIANTS_FILE" ]; then
  echo "ALMS_VERIFY_ERROR missing_invariants path=$INVARIANTS_FILE" >&2
  exit 2
fi

MODE="raw"
RECEIPT_FILE=""
ORIGINAL_CLAIM=""

if [ "$#" -eq 0 ]; then
  ORIGINAL_CLAIM=$(cat)
else
  MODE="replay"
  RECEIPT_FILE="$1"
  if [ ! -f "$RECEIPT_FILE" ]; then
    echo "ALMS_VERIFY_ERROR missing_receipt path=$RECEIPT_FILE" >&2
    exit 2
  fi
  ORIGINAL_CLAIM=$(jq -r '.original_claim // empty' "$RECEIPT_FILE")
  if [ -z "$ORIGINAL_CLAIM" ]; then
    echo "ALMS_VERIFY_FAIL missing_original_claim" >&2
    exit 1
  fi
fi

NORMALIZE_OUTPUT=$(printf '%s' "$ORIGINAL_CLAIM" | "$NORMALIZER")
INPUT_HASH=$(printf '%s' "$NORMALIZE_OUTPUT" | jq -r '.input_hash')
NORMALIZED_HASH=$(printf '%s' "$NORMALIZE_OUTPUT" | jq -r '.normalized_hash')
NORMALIZED_TEXT=$(printf '%s' "$NORMALIZE_OUTPUT" | jq -r '.normalized_text')

if [ "$MODE" = "replay" ]; then
  RECORDED_INPUT_HASH=$(jq -r '.input_hash' "$RECEIPT_FILE")
  RECORDED_NORMALIZED_HASH=$(jq -r '.normalized_hash' "$RECEIPT_FILE")

  if [ "$INPUT_HASH" != "$RECORDED_INPUT_HASH" ]; then
    echo "ALMS_VERIFY_FAIL input_hash_mismatch expected=$RECORDED_INPUT_HASH actual=$INPUT_HASH" >&2
    exit 1
  fi

  if [ "$NORMALIZED_HASH" != "$RECORDED_NORMALIZED_HASH" ]; then
    echo "ALMS_VERIFY_FAIL normalized_hash_mismatch expected=$RECORDED_NORMALIZED_HASH actual=$NORMALIZED_HASH" >&2
    exit 1
  fi
fi

# Invariant scaffold v1: intentionally honest. These are not automated yet,
# so they fail closed into NEEDS_MORE_EVIDENCE instead of pretending certainty.
INVARIANT_RESULTS=$(jq -n '[
  {"id":"temporal_order","passed":false,"details":"v1 scaffold: requires explicit temporal evidence extraction"},
  {"id":"numerical_consistency","passed":false,"details":"v1 scaffold: requires numeric component extraction"},
  {"id":"identity_resolution","passed":false,"details":"v1 scaffold: requires grounded entity resolution"},
  {"id":"cardinality_match","passed":false,"details":"v1 scaffold: requires count extraction"},
  {"id":"causal_direction","passed":false,"details":"v1 scaffold: requires causal evidence mapping"},
  {"id":"source_presence","passed":false,"details":"v1 scaffold: source proof not attached in raw mode"},
  {"id":"entity_uniqueness","passed":false,"details":"v1 scaffold: requires entity deduplication"},
  {"id":"logical_consistency","passed":false,"details":"v1 scaffold: requires contradiction scan"}
]')

VERDICT="NEEDS_MORE_EVIDENCE"
VERDICT_REASON="Invariant enforcement is scaffolded in v1 and fails closed until source proofs and domain checks are attached."
FAILURE_STATES_JSON='["NON_REPRODUCIBLE"]'

if [ "$MODE" = "replay" ]; then
  RECEIPT_ID=$(jq -r '.receipt_id' "$RECEIPT_FILE")
  VALID_AS_OF=$(jq -r '.valid_as_of' "$RECEIPT_FILE")
  REPLAY_CMD=$(jq -r '.replay_cmd' "$RECEIPT_FILE")
else
  RECEIPT_ID="ALMS-MS-$(date -u +%Y%m%d%H%M%S)"
  VALID_AS_OF=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  REPLAY_CMD="bash scripts/alms_verify.sh _truth/receipts/${RECEIPT_ID}.json"
fi

BASE_RECEIPT=$(jq -n \
  --arg receipt_id "$RECEIPT_ID" \
  --arg schema_version "2.0" \
  --arg input_hash "$INPUT_HASH" \
  --arg normalized_hash "$NORMALIZED_HASH" \
  --arg transform_version "normalize_strict_v1" \
  --arg invariant_version "invariants_v1" \
  --arg original_claim "$ORIGINAL_CLAIM" \
  --arg normalized_text "$NORMALIZED_TEXT" \
  --arg verdict "$VERDICT" \
  --arg verdict_reason "$VERDICT_REASON" \
  --argjson failure_states "$FAILURE_STATES_JSON" \
  --argjson invariants_results "$INVARIANT_RESULTS" \
  --arg valid_as_of "$VALID_AS_OF" \
  --arg replay_cmd "$REPLAY_CMD" \
  '{
    receipt_id: $receipt_id,
    schema_version: $schema_version,
    input_hash: $input_hash,
    normalized_hash: $normalized_hash,
    transform_version: $transform_version,
    invariant_version: $invariant_version,
    original_claim: $original_claim,
    normalized_text: $normalized_text,
    verdict: $verdict,
    verdict_reason: $verdict_reason,
    failure_states: $failure_states,
    invariants_results: $invariants_results,
    proofs: [],
    valid_as_of: $valid_as_of,
    replay_cmd: $replay_cmd,
    environment: {
      verifier_version: "alms_verify_v2_scaffold",
      git_commit: "unknown"
    }
  }')

RECEIPT_HASH="sha256:$(printf '%s' "$BASE_RECEIPT" | jq -cS . | sha256sum | awk '{print $1}')"
FINAL_RECEIPT=$(printf '%s' "$BASE_RECEIPT" | jq --arg receipt_hash "$RECEIPT_HASH" '. + {receipt_hash: $receipt_hash}')

if [ "$MODE" = "replay" ]; then
  RECORDED_RECEIPT_HASH=$(jq -r '.receipt_hash // empty' "$RECEIPT_FILE")
  if [ -n "$RECORDED_RECEIPT_HASH" ] && [ "$RECEIPT_HASH" != "$RECORDED_RECEIPT_HASH" ]; then
    echo "ALMS_VERIFY_FAIL receipt_hash_mismatch expected=$RECORDED_RECEIPT_HASH actual=$RECEIPT_HASH" >&2
    exit 1
  fi
  RECORDED_VERDICT=$(jq -r '.verdict' "$RECEIPT_FILE")
  if [ "$VERDICT" != "$RECORDED_VERDICT" ]; then
    echo "ALMS_VERIFY_FAIL verdict_mismatch expected=$RECORDED_VERDICT actual=$VERDICT" >&2
    exit 1
  fi
  echo "ALMS_VERIFY_OK replay receipt_id=$RECEIPT_ID verdict=$VERDICT hash=$RECEIPT_HASH" >&2
else
  echo "ALMS_VERIFY_OK generated receipt_id=$RECEIPT_ID verdict=$VERDICT hash=$RECEIPT_HASH" >&2
fi

printf '%s\n' "$FINAL_RECEIPT" | jq .
