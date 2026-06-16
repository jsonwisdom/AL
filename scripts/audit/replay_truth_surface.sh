#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

mkdir -p _truth/audit

STATUS_FILE="status.json"
LAST_RUN_FILE="_truth/status/last_run.json"
ROOT_HISTORY="_truth/root_history/root_history.jsonl"
BASELINE_ROOT="dc4b992f9f6eb41139056a5f75af6d523ed6f55a9775da21401e8bc185e86f5c"
BASELINE_SHA="fc78b6b71e02b7ecf316d37da89032955bae161053b55c241702e35a7557514a"
BASELINE_ALGORITHM="sha256_hex_concat_v1"
BASELINE_LEAF_COUNT="2"

for f in "$STATUS_FILE" "$LAST_RUN_FILE" "$ROOT_HISTORY"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING_REQUIRED_FILE $f" >&2
    exit 1
  fi
done

status_root="$(jq -r '.merkle_root' "$STATUS_FILE")"
status_sha="$(jq -r '.root_sha256' "$STATUS_FILE")"
status_leaf_count="$(jq -r '.leaf_count' "$STATUS_FILE")"
status_consensus="$(jq -r '.consensus' "$STATUS_FILE")"
status_algorithm="$(jq -r '.merkle_algorithm' "$STATUS_FILE")"

latest_root_line="$(tail -n 1 "$ROOT_HISTORY")"
history_root="$(printf '%s' "$latest_root_line" | jq -r '.merkle_root')"
history_sha="$(printf '%s' "$latest_root_line" | jq -r '.root_sha256')"

ok=true
[[ "$status_root" == "$history_root" ]] || ok=false
[[ "$status_sha" == "$history_sha" ]] || ok=false
[[ "$status_root" == "$BASELINE_ROOT" ]] || ok=false
[[ "$status_sha" == "$BASELINE_SHA" ]] || ok=false
[[ "$status_algorithm" == "$BASELINE_ALGORITHM" ]] || ok=false
[[ "$status_leaf_count" == "$BASELINE_LEAF_COUNT" ]] || ok=false
[[ "$status_consensus" == "true" ]] || ok=false

cat > _truth/audit/replay_truth_surface_report.json <<JSON
{
  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",
  "gate": "replay_truth_surface",
  "mode": "BASELINE_ROOT_HARDENED",
  "ok": $ok,
  "baseline": {
    "merkle_root": "$BASELINE_ROOT",
    "root_sha256": "$BASELINE_SHA",
    "merkle_algorithm": "$BASELINE_ALGORITHM",
    "leaf_count": $BASELINE_LEAF_COUNT
  },
  "status_json": {
    "merkle_root": "$status_root",
    "root_sha256": "$status_sha",
    "leaf_count": $status_leaf_count,
    "consensus": $status_consensus,
    "merkle_algorithm": "$status_algorithm"
  },
  "root_history_latest": {
    "merkle_root": "$history_root",
    "root_sha256": "$history_sha"
  }
}
JSON

if [[ "$ok" != true ]]; then
  echo "REPLAY_TRUTH_SURFACE_FAIL"
  cat _truth/audit/replay_truth_surface_report.json
  exit 1
fi

echo "REPLAY_TRUTH_SURFACE_OK root=$status_root sha=$status_sha leaf_count=$status_leaf_count consensus=$status_consensus algorithm=$status_algorithm"
