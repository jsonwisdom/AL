#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH — DOMAIN CLUSTER V1
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

jq -cS --arg ts "$TIMESTAMP_UTC" '
  def sha256_key:
    @base64;

  [inputs] as $rows
  | $rows
  | group_by([.root_domain, .redirect_count])
  | map({
      cluster_key: (
        (.[0].root_domain + ":" + (.[0].redirect_count|tostring))
        | @base64
      ),
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
' /dev/null "$INPUT_JSONL"
