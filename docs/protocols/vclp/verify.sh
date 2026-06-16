#!/usr/bin/env bash
set -euo pipefail

LEDGER="${1:-_truth/ledger.jsonl}"
PATTERNS="${2:-_truth/patterns.json}"

echo "=== VCLP Runtime Ledger Verification v1.1 ==="

if [[ ! -f "$LEDGER" ]]; then echo "x ledger not found: $LEDGER"; exit 1; fi
if [[ ! -f "$PATTERNS" ]]; then echo "x patterns not found: $PATTERNS"; exit 1; fi
if ! jq empty "$PATTERNS" >/dev/null 2>&1; then echo "x patterns.json invalid JSON"; exit 1; fi
echo "v patterns.json valid"

KNOWN_MEDIA_TYPES=("application/json" "application/octet-stream" "application/pdf" "image/gif" "image/jpeg" "image/png" "image/webp" "text/csv" "text/html" "text/markdown" "text/plain")

is_known_media_type() {
  local mt="$1"
  local known
  for known in "${KNOWN_MEDIA_TYPES[@]}"; do
    [[ "$mt" == "$known" ]] && return 0
  done
  [[ "$mt" == text/* ]] && return 0
  return 1
}

total=0; clean=0
source_bound=0; source_bound_unknown=0; source_legacy=0; source_missing=0; source_media_missing=0
fail_invalid_json=0; fail_missing_required=0; fail_hash_mismatch=0; fail_chain_break=0
fail_source_hash_missing=0; fail_source_hash_malformed=0; fail_source_media_missing=0; fail_schema_unknown=0; fail_pattern_mismatch=0

failed=0
line_no=0
prev_line_hash=""
pattern_count="$(jq 'length' "$PATTERNS")"

while IFS= read -r line; do
  line_no=$((line_no + 1))
  [[ -z "$line" ]] && continue
  total=$((total + 1))

  entry_failed=0
  axis_chain="fail"
  axis_text="fail"
  axis_source="missing"

  if ! printf "%s" "$line" | jq empty >/dev/null 2>&1; then
    echo "x line $line_no invalid JSON"
    echo "VCLP_AXES line=$line_no chain=fail text=fail source=missing"
    failed=1
    fail_invalid_json=$((fail_invalid_json + 1))
    prev_line_hash="$(printf "%s" "$line" | sha256sum | awk '{print $1}')"
    continue
  fi

  claim_id="$(printf "%s" "$line" | jq -r '.claim_id // empty')"
  claim_text="$(printf "%s" "$line" | jq -r '.claim_text // empty')"
  stored_text_hash="$(printf "%s" "$line" | jq -r '.artifacts.text_hash // empty' | sed 's/^sha256://')"
  prev_hash="$(printf "%s" "$line" | jq -r '.prev_hash // "null"')"
  schema_version="$(printf "%s" "$line" | jq -r '.schema_version // empty')"

  if [[ -z "$claim_id" || -z "$claim_text" || -z "$stored_text_hash" ]]; then
    echo "x line $line_no missing required fields"
    echo "VCLP_AXES line=$line_no chain=fail text=fail source=missing"
    failed=1
    fail_missing_required=$((fail_missing_required + 1))
    prev_line_hash="$(printf "%s" "$line" | sha256sum | awk '{print $1}')"
    continue
  fi

  computed_text_hash="$(printf "%s" "$claim_text" | sha256sum | awk '{print $1}')"
  if [[ "$computed_text_hash" != "$stored_text_hash" ]]; then
    echo "x $claim_id text_hash MISMATCH"
    failed=1
    entry_failed=1
    fail_hash_mismatch=$((fail_hash_mismatch + 1))
  else
    echo "v $claim_id text_hash ok"
    axis_text="ok"
  fi

  if [[ "$line_no" -eq 1 ]]; then
    if [[ "$prev_hash" != "null" ]]; then
      echo "x $claim_id genesis prev_hash must be null"
      failed=1
      entry_failed=1
      fail_chain_break=$((fail_chain_break + 1))
    else
      echo "v $claim_id genesis ok"
      axis_chain="ok"
    fi
  else
    expected_prev="sha256:$prev_line_hash"
    if [[ "$prev_hash" != "$expected_prev" ]]; then
      echo "x $claim_id prev_hash CHAIN BREAK"
      failed=1
      entry_failed=1
      fail_chain_break=$((fail_chain_break + 1))
    else
      echo "v $claim_id prev_hash ok"
      axis_chain="ok"
    fi
  fi

  if [[ -z "$schema_version" ]]; then
    echo "~ $claim_id SOURCE_LEGACY"
    axis_source="legacy"
    source_legacy=$((source_legacy + 1))
  elif [[ "$schema_version" == "vclp-1.1" ]]; then
    raw_source_hash="$(printf "%s" "$line" | jq -r '.artifacts.source_hash // empty')"
    source_media_type="$(printf "%s" "$line" | jq -r '.artifacts.source_media_type // empty')"

    if [[ -z "$raw_source_hash" ]]; then
      echo "x $claim_id FAIL_SOURCE_HASH_MISSING"
      failed=1
      entry_failed=1
      fail_source_hash_missing=$((fail_source_hash_missing + 1))
      source_missing=$((source_missing + 1))
      axis_source="missing"
    elif ! printf "%s" "$raw_source_hash" | grep -qE '^sha256:[a-f0-9]{64}$'; then
      echo "x $claim_id FAIL_SOURCE_HASH_MALFORMED"
      failed=1
      entry_failed=1
      fail_source_hash_malformed=$((fail_source_hash_malformed + 1))
      source_missing=$((source_missing + 1))
      axis_source="malformed"
    elif [[ -z "$source_media_type" ]]; then
      echo "x $claim_id FAIL_SOURCE_MEDIA_TYPE_MISSING"
      failed=1
      entry_failed=1
      fail_source_media_missing=$((fail_source_media_missing + 1))
      source_media_missing=$((source_media_missing + 1))
      axis_source="missing"
    elif ! is_known_media_type "$source_media_type"; then
      echo "~ $claim_id SOURCE_MEDIA_TYPE_UNKNOWN source=bound-unknown"
      source_bound_unknown=$((source_bound_unknown + 1))
      axis_source="bound-unknown"
    else
      echo "v $claim_id source_hash bound"
      source_bound=$((source_bound + 1))
      axis_source="bound"
    fi
  else
    echo "x $claim_id FAIL_SCHEMA_VERSION_UNKNOWN"
    failed=1
    entry_failed=1
    fail_schema_unknown=$((fail_schema_unknown + 1))
    axis_source="missing"
  fi

  echo "VCLP_AXES id=$claim_id chain=$axis_chain text=$axis_text source=$axis_source"

  if [[ "$entry_failed" -eq 0 && "$pattern_count" -gt 0 ]]; then
    while IFS= read -r pattern; do
      required_regex="$(printf "%s" "$pattern" | jq -r '.required_regex // empty')"
      forbidden_regex="$(printf "%s" "$pattern" | jq -r '.forbidden_regex // empty')"

      if [[ -n "$required_regex" ]] && ! printf "%s" "$claim_text" | grep -qE "$required_regex"; then
        echo "x $claim_id FAIL_PATTERN_MISMATCH required_regex"
        failed=1
        entry_failed=1
        fail_pattern_mismatch=$((fail_pattern_mismatch + 1))
      fi

      if [[ -n "$forbidden_regex" ]] && printf "%s" "$claim_text" | grep -qE "$forbidden_regex"; then
        echo "x $claim_id FAIL_PATTERN_MISMATCH forbidden_regex"
        failed=1
        entry_failed=1
        fail_pattern_mismatch=$((fail_pattern_mismatch + 1))
      fi

      if printf "%s" "$pattern" | jq -e '.required_result_states' >/dev/null 2>&1; then
        entry_result="$(printf "%s" "$line" | jq -r '.result // empty')"
        if ! printf "%s" "$pattern" | jq -e --arg r "$entry_result" '.required_result_states | map(. == $r) | any' >/dev/null 2>&1; then
          echo "x $claim_id FAIL_PATTERN_MISMATCH result_state"
          failed=1
          entry_failed=1
          fail_pattern_mismatch=$((fail_pattern_mismatch + 1))
        fi
      fi
    done < <(jq -c '.[]' "$PATTERNS")
  fi

  [[ "$entry_failed" -eq 0 ]] && clean=$((clean + 1))
  prev_line_hash="$(printf "%s" "$line" | sha256sum | awk '{print $1}')"
done < "$LEDGER"

total_failures=$((fail_invalid_json + fail_missing_required + fail_hash_mismatch + fail_chain_break + fail_source_hash_missing + fail_source_hash_malformed + fail_source_media_missing + fail_schema_unknown + fail_pattern_mismatch))

echo ""
echo "VCLP_SUMMARY entries=$total clean=$clean failures=$total_failures"
echo "VCLP_SOURCE source_bound=$source_bound source_bound_unknown=$source_bound_unknown source_legacy=$source_legacy source_missing=$source_missing source_media_missing=$source_media_missing"
echo "VCLP_FAILURES invalid_json=$fail_invalid_json missing_required=$fail_missing_required hash_mismatch=$fail_hash_mismatch chain_break=$fail_chain_break source_hash_missing=$fail_source_hash_missing source_hash_malformed=$fail_source_hash_malformed source_media_missing=$fail_source_media_missing schema_unknown=$fail_schema_unknown pattern_mismatch=$fail_pattern_mismatch"

if [[ "$failed" -ne 0 ]]; then
  echo "FAIL"
  exit 1
elif [[ "$source_legacy" -gt 0 ]]; then
  echo "PASS_WITH_LEGACY_SOURCE_NAMED_ONLY"
  exit 0
else
  echo "PASS_STRONG"
  exit 0
fi
