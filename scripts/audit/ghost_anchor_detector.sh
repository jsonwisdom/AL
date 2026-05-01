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
# Track 001 harden phase: any hit is a CI failure.
grep -RInE "IPFS|CID|EAS|UID|Zora|contract|verified|anchored" "${find_scope[@]}" 2>/dev/null \
  | grep -Ev "Qm[1-9A-HJ-NP-Za-km-z]{44}|bafy[0-9a-z]{50,}|0x[a-fA-F0-9]{40}|0x[a-fA-F0-9]{64}|zora\.co|easscan\.org|basescan\.org|github\.com|AWAITING_CID|AWAITING_EAS_UID|AWAITING_ZORA_URL|PENDING_LIVE_CID|PENDING_BASE_UID|WITHHELD|MINT_PENDING_COURT_RULING" \
  > "$hits_file" || true

count="$(wc -l < "$hits_file" | tr -d ' ')"
ok=true
if [[ "$count" != "0" ]]; then
  ok=false
fi

{
  echo '{'
  echo '  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",'
  echo '  "gate": "ghost_anchor_detector",'
  echo '  "mode": "HARD_FAIL",'
  echo "  \"ok\": $ok,"
  echo "  \"possible_ghost_anchor_count\": $count,"
  echo '  "policy": "CI fails on ghost anchor claims unless concrete CID, UID, URL, tx hash, address, or explicit withheld/pending marker is present.",'
  echo '  "possible_hits": ['
  awk 'BEGIN{first=1} {gsub(/\\/,"\\\\"); gsub(/"/,"\\\""); if(!first) printf ",\n"; first=0; printf "    \"%s\"", $0}' "$hits_file"
  echo
  echo '  ]'
  echo '}'
} > "$report"

if [[ "$count" != "0" ]]; then
  echo "GHOST_ANCHOR_DETECTOR_FAIL count=$count report=$report"
  cat "$report"
  exit 1
fi

echo "GHOST_ANCHOR_DETECTOR_OK count=0 report=$report"
