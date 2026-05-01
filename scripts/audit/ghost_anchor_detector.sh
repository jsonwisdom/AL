#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"
mkdir -p _truth/audit

report="_truth/audit/ghost_anchor_report.json"
find_scope=(docs site _truth)

hits_file="$(mktemp)"
trap 'rm -f "$hits_file"' EXIT

# Ghost patterns: claims of external anchors without concrete identifiers nearby.
# This is intentionally conservative in Track 001: report first, fail later.
grep -RInE "IPFS|CID|EAS|UID|Zora|contract|verified|anchored" "${find_scope[@]}" 2>/dev/null \
  | grep -Ev "Qm[1-9A-HJ-NP-Za-km-z]{44}|bafy[0-9a-z]{50,}|0x[a-fA-F0-9]{40}|0x[a-fA-F0-9]{64}|zora\.co|easscan\.org|basescan\.org|github\.com" \
  > "$hits_file" || true

count="$(wc -l < "$hits_file" | tr -d ' ')"

{
  echo '{'
  echo '  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",'
  echo '  "gate": "ghost_anchor_detector",'
  echo '  "mode": "REPORT_ONLY",'
  echo "  \"possible_ghost_anchor_count\": $count,"
  echo '  "policy": "Report first in Track 001. Convert to CI fail gate after baseline review.",'
  echo '  "possible_hits": ['
  awk 'BEGIN{first=1} {gsub(/\\/,"\\\\"); gsub(/"/,"\\\""); if(!first) printf ",\n"; first=0; printf "    \"%s\"", $0}' "$hits_file"
  echo
  echo '  ]'
  echo '}'
} > "$report"

echo "GHOST_ANCHOR_DETECTOR_REPORT_ONLY count=$count report=$report"
