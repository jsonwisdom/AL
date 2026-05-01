#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

mkdir -p _truth/audit

STATUS_FILE="status.json"
LAST_RUN_FILE="_truth/status/last_run.json"
ROOT_HISTORY="_truth/root_history/root_history.jsonl"

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

latest_root_line="$(tail -n 1 "$ROOT_HISTORY")"
history_root="$(printf '%s' "$latest_root_line" | jq -r '.merkle_root')"
history_sha="$(printf '%s' "$latest_root_line" | jq -r '.root_sha256')"

cat > _truth/audit/replay_truth_surface_report.json <<JSON
{
  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",
  "gate": "replay_truth_surface",
  "status_json": {
    "merkle_root": "$status_root",
    "root_sha256": "$status_sha",
    "leaf_count": $status_leaf_count,
    "consensus": $status_consensus
  },
  "root_history_latest": {
    "merkle_root": "$history_root",
    "root_sha256": "$history_sha"
  },
  "match": $([[ "$status_root" == "$history_root" && "$status_sha" == "$history_sha" ]] && echo true || echo false)
}
JSON

if [[ "$status_root" != "$history_root" || "$status_sha" != "$history_sha" ]]; then
  echo "REPLAY_TRUTH_SURFACE_FAIL"
  cat _truth/audit/replay_truth_surface_report.json
  exit 1
fi

echo "REPLAY_TRUTH_SURFACE_OK root=$status_root sha=$status_sha leaf_count=$status_leaf_count consensus=$status_consensus"
