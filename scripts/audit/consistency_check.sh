#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"
mkdir -p _truth/audit

required=(
  "status.json"
  "_truth/status/last_run.json"
  "_truth/root_history/root_history.jsonl"
  "_truth/timeline/timeline.json"
)

for f in "${required[@]}"; do
  [[ -f "$f" ]] || { echo "CONSISTENCY_FAIL missing=$f" >&2; exit 1; }
done

status_root="$(jq -r '.merkle_root' status.json)"
status_sha="$(jq -r '.root_sha256' status.json)"
status_commit="$(jq -r '.commit' status.json)"
status_consensus="$(jq -r '.consensus' status.json)"

last_root="$(jq -r '.merkle_root' _truth/status/last_run.json)"
last_sha="$(jq -r '.root_sha256' _truth/status/last_run.json)"
last_commit="$(jq -r '.commit' _truth/status/last_run.json)"
last_consensus="$(jq -r '.consensus' _truth/status/last_run.json)"

history_line="$(tail -n 1 _truth/root_history/root_history.jsonl)"
history_root="$(printf '%s' "$history_line" | jq -r '.merkle_root')"
history_sha="$(printf '%s' "$history_line" | jq -r '.root_sha256')"

ok=true
[[ "$status_root" == "$last_root" && "$status_root" == "$history_root" ]] || ok=false
[[ "$status_sha" == "$last_sha" && "$status_sha" == "$history_sha" ]] || ok=false
[[ "$status_commit" == "$last_commit" ]] || ok=false
[[ "$status_consensus" == "$last_consensus" ]] || ok=false

cat > _truth/audit/consistency_report.json <<JSON
{
  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",
  "gate": "consistency_check",
  "ok": $ok,
  "status": {
    "commit": "$status_commit",
    "merkle_root": "$status_root",
    "root_sha256": "$status_sha",
    "consensus": $status_consensus
  },
  "last_run": {
    "commit": "$last_commit",
    "merkle_root": "$last_root",
    "root_sha256": "$last_sha",
    "consensus": $last_consensus
  },
  "root_history_latest": {
    "merkle_root": "$history_root",
    "root_sha256": "$history_sha"
  }
}
JSON

if [[ "$ok" != true ]]; then
  echo "CONSISTENCY_CHECK_FAIL"
  cat _truth/audit/consistency_report.json
  exit 1
fi

echo "CONSISTENCY_CHECK_OK root=$status_root sha=$status_sha commit=$status_commit"
