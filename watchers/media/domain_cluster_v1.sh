#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — DOMAIN CLUSTER V1.1
# PURPOSE: Group media mesh receipts by normalized host + redirect count
# RULE: No ML, no similarity scoring, no semantic inference

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <jsonl_file>" >&2
  exit 2
fi

INPUT_JSONL="$1"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [ ! -f "$INPUT_JSONL" ]; then
  jq -n -cS --arg reason "INPUT_FILE_NOT_FOUND" --arg ts "$TIMESTAMP_UTC" '{cluster_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
fi

if ! jq -e 'select(.root_domain and (.redirect_count != null) and .resolved_url)' "$INPUT_JSONL" >/dev/null 2>&1; then
  jq -n -cS --arg reason "MALFORMED_INPUT" --arg ts "$TIMESTAMP_UTC" '{cluster_status:"HARD_FAIL",reason:$reason,timestamp_utc:$ts}'
  exit 1
fi

TMP_CLUSTERS="$(mktemp)"
trap 'rm -f "$TMP_CLUSTERS"' EXIT

jq -cS --arg ts "$TIMESTAMP_UTC" '
  [inputs] as $rows
  | $rows
  | group_by([.root_domain, .redirect_count])
  | map({
      cluster_input: (.[0].root_domain + ":" + (.[0].redirect_count|tostring)),
      drift_count: (map(select(.drift_status? and .drift_status != "NO_DRIFT")) | length),
      redirect_count: .[0].redirect_count,
      root_domain: .[0].root_domain,
      sample_count: length,
      sample_urls: (map(.resolved_url) | unique | .[0:10])
    })
  | {
      cluster_status: "OK",
      clusters: .,
      generated_at_utc: $ts,
      input_count: ($rows | length)
    }
' /dev/null "$INPUT_JSONL" > "$TMP_CLUSTERS"

jq -c '.clusters[]' "$TMP_CLUSTERS" | while IFS= read -r cluster; do
  CLUSTER_INPUT="$(printf '%s' "$cluster" | jq -r '.cluster_input')"
  CLUSTER_KEY="$(printf '%s' "$CLUSTER_INPUT" | sha256sum | awk '{print $1}')"
  printf '%s\n' "$cluster" | jq -cS --arg cluster_key "$CLUSTER_KEY" 'del(.cluster_input) + {cluster_key:$cluster_key}'
done | jq -s -cS --arg ts "$TIMESTAMP_UTC" --argjson input_count "$(jq -r '.input_count' "$TMP_CLUSTERS")" '{cluster_status:"OK",clusters:.,generated_at_utc:$ts,input_count:$input_count}'
