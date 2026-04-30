#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — MERGED RECEIPT V1
# PURPOSE: Bind watcher + extractor + drift (+ optional cluster/break) into one canonical leaf receipt
# RULE: No inference, no fallback logic, no best effort

if [ "$#" -lt 3 ]; then
  echo "usage: $0 <watcher_json> <extractor_json> <drift_json> [cluster_json] [break_json]" >&2
  exit 2
fi

WATCHER_JSON="$1"
EXTRACTOR_JSON="$2"
DRIFT_JSON="$3"
CLUSTER_JSON="${4:-}"
BREAK_JSON="${5:-}"
GENERATED_AT_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

hard_fail() {
  jq -n -cS --arg reason "$1" --arg ts "$GENERATED_AT_UTC" '{merge_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
}

[ -f "$WATCHER_JSON" ] || hard_fail "WATCHER_FILE_NOT_FOUND"
[ -f "$EXTRACTOR_JSON" ] || hard_fail "EXTRACTOR_FILE_NOT_FOUND"
[ -f "$DRIFT_JSON" ] || hard_fail "DRIFT_FILE_NOT_FOUND"

jq -e '.source_url and .resolved_url and .root_domain and (.redirect_count != null) and .discovered_from' "$WATCHER_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_WATCHER_INPUT"
jq -e '.source_url and .claim_excerpt and .timestamp_utc' "$EXTRACTOR_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_EXTRACTOR_INPUT"
jq -e '.source_url and .raw_hash and .norm_hash and (.raw_changed != null) and (.norm_changed != null) and .drift_status' "$DRIFT_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_DRIFT_INPUT"

WATCHER_SOURCE_URL="$(jq -r '.source_url' "$WATCHER_JSON")"
WATCHER_RESOLVED_URL="$(jq -r '.resolved_url' "$WATCHER_JSON")"
EXTRACTOR_SOURCE_URL="$(jq -r '.source_url' "$EXTRACTOR_JSON")"
DRIFT_SOURCE_URL="$(jq -r '.source_url' "$DRIFT_JSON")"

[ "$WATCHER_RESOLVED_URL" = "$EXTRACTOR_SOURCE_URL" ] || hard_fail "WATCHER_EXTRACTOR_URL_MISMATCH"
[ "$WATCHER_RESOLVED_URL" = "$DRIFT_SOURCE_URL" ] || hard_fail "WATCHER_DRIFT_URL_MISMATCH"

CLUSTER_KEY=""
if [ -n "$CLUSTER_JSON" ]; then
  [ -f "$CLUSTER_JSON" ] || hard_fail "CLUSTER_FILE_NOT_FOUND"
  jq -e '.cluster_key' "$CLUSTER_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_CLUSTER_INPUT"
  CLUSTER_KEY="$(jq -r '.cluster_key' "$CLUSTER_JSON")"
fi

BREAK_STATUS=""
SAME_ROOT=false
SAME_WITNESS=false
if [ -n "$BREAK_JSON" ]; then
  [ -f "$BREAK_JSON" ] || hard_fail "BREAK_FILE_NOT_FOUND"
  jq -e '.break_status and (.same_root != null) and (.same_witness != null)' "$BREAK_JSON" >/dev/null 2>&1 || hard_fail "MALFORMED_BREAK_INPUT"
  BREAK_RESOLVED_URL="$(jq -r '.resolved_url' "$BREAK_JSON")"
  [ "$WATCHER_RESOLVED_URL" = "$BREAK_RESOLVED_URL" ] || hard_fail "WATCHER_BREAK_URL_MISMATCH"
  BREAK_STATUS="$(jq -r '.break_status' "$BREAK_JSON")"
  SAME_ROOT="$(jq -r '.same_root' "$BREAK_JSON")"
  SAME_WITNESS="$(jq -r '.same_witness' "$BREAK_JSON")"
fi

jq -n -cS \
  --arg break_status "$BREAK_STATUS" \
  --arg claim_excerpt "$(jq -r '.claim_excerpt' "$EXTRACTOR_JSON")" \
  --arg cluster_key "$CLUSTER_KEY" \
  --arg discovered_from "$(jq -r '.discovered_from' "$WATCHER_JSON")" \
  --arg drift_status "$(jq -r '.drift_status' "$DRIFT_JSON")" \
  --arg generated_at_utc "$GENERATED_AT_UTC" \
  --arg input_url "$WATCHER_SOURCE_URL" \
  --arg norm_hash "$(jq -r '.norm_hash' "$DRIFT_JSON")" \
  --arg raw_hash "$(jq -r '.raw_hash' "$DRIFT_JSON")" \
  --arg resolved_url "$WATCHER_RESOLVED_URL" \
  --arg root_domain "$(jq -r '.root_domain' "$WATCHER_JSON")" \
  --arg timestamp_utc "$(jq -r '.timestamp_utc' "$EXTRACTOR_JSON")" \
  --argjson norm_changed "$(jq -r '.norm_changed' "$DRIFT_JSON")" \
  --argjson raw_changed "$(jq -r '.raw_changed' "$DRIFT_JSON")" \
  --argjson redirect_count "$(jq -r '.redirect_count' "$WATCHER_JSON")" \
  --argjson same_root "$SAME_ROOT" \
  --argjson same_witness "$SAME_WITNESS" \
  '{break_status:$break_status,claim_excerpt:$claim_excerpt,cluster_key:$cluster_key,discovered_from:$discovered_from,drift_status:$drift_status,generated_at_utc:$generated_at_utc,input_url:$input_url,norm_changed:$norm_changed,norm_hash:$norm_hash,raw_changed:$raw_changed,raw_hash:$raw_hash,redirect_count:$redirect_count,resolved_url:$resolved_url,root_domain:$root_domain,same_root:$same_root,same_witness:$same_witness,timestamp_utc:$timestamp_utc}'
