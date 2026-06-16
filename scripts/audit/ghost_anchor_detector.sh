#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"
mkdir -p _truth/audit

report="_truth/audit/ghost_anchor_report.json"
inventory="_truth/audit/truth_surface_inventory.json"

if [[ ! -f "$inventory" ]]; then
  echo "GHOST_ANCHOR_DETECTOR_FAIL missing=$inventory"
  exit 1
fi

patterns='IPFS|CID|EAS|UID|Zora|contract|verified|anchored|schema_uid'
receipts='Qm[1-9A-HJ-NP-Za-km-z]{44}|bafy[0-9a-z]{50,}|0x[a-fA-F0-9]{40}|0x[a-fA-F0-9]{64}|zora\.co|easscan\.org|basescan\.org|github\.com|AWAITING_CID|AWAITING_EAS_UID|AWAITING_ZORA_URL|PENDING_LIVE_CID|PENDING_BASE_UID|WITHHELD|MINT_PENDING_COURT_RULING|EXPLICITLY_PENDING|NOT_APPLICABLE'

tmp_files="$(mktemp)"
hard_hits="$(mktemp)"
legacy_hits="$(mktemp)"
trap 'rm -f "$tmp_files" "$hard_hits" "$legacy_hits"' EXIT

jq -r '
  .truth_surfaces[]
  | if type=="string" then . else .path end
' "$inventory" \
  | sed 's#/$##' \
  | while read -r p; do
      [[ -e "$p" ]] && find "$p" -type f 2>/dev/null || true
    done \
  | sort -u > "$tmp_files"

while read -r f; do
  grep -nE "$patterns" "$f" 2>/dev/null \
    | sed "s#^#$f:#" \
    | grep -Ev "$receipts" >> "$hard_hits" || true
done < "$tmp_files"

# Legacy report only, not fail gate.
grep -RInE "$patterns" docs site _truth 2>/dev/null \
  | grep -Ev "$receipts" \
  | grep -vFf "$hard_hits" \
  > "$legacy_hits" || true

hard_count="$(wc -l < "$hard_hits" | tr -d ' ')"
legacy_count="$(wc -l < "$legacy_hits" | tr -d ' ')"

jq -n \
  --arg mode "INVENTORY_HARD_FAIL_LEGACY_REPORT" \
  --argjson ok "$([[ "$hard_count" == "0" ]] && echo true || echo false)" \
  --argjson hard_count "$hard_count" \
  --argjson legacy_count "$legacy_count" \
  --slurpfile hard <(jq -R . "$hard_hits" | jq -s .) \
  --slurpfile legacy <(jq -R . "$legacy_hits" | jq -s .) \
  '{
    track:"ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",
    gate:"ghost_anchor_detector",
    mode:$mode,
    ok:$ok,
    hard_fail_count:$hard_count,
    legacy_report_count:$legacy_count,
    policy:"Only inventoried truth surfaces hard-fail. Legacy docs report-only until promoted into inventory.",
    hard_fail_hits:$hard[0],
    legacy_report_hits:$legacy[0]
  }' > "$report"

if [[ "$hard_count" != "0" ]]; then
  echo "GHOST_ANCHOR_DETECTOR_FAIL hard_count=$hard_count legacy_count=$legacy_count report=$report"
  jq . "$report"
  exit 1
fi

echo "GHOST_ANCHOR_DETECTOR_OK hard_count=0 legacy_count=$legacy_count report=$report"
