#!/usr/bin/env bash
# Boss Bre anomaly detector v0.1
# Purpose: convert statewide fiscal text/receipts into storefront-safe anomaly leads.
# Doctrine: NO_FAKE_GREEN. This emits leads only, never fraud verdicts.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
RULES="$ROOT/data/boss_bre_anomaly_rules.json"
STATE_DIR="$ROOT/projects/mn-fiscal-replay/boss_bre"
LATEST="$STATE_DIR/latest_sweep_summary.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="${UTC//[:]/-}"
RUN_DIR="$STATE_DIR/runs/$RUN_ID"
OUT_JSONL="$RUN_DIR/anomaly_leads.jsonl"
PUBLIC_MD="$STATE_DIR/boss_bre_public_anomaly_board.md"
LATEST_LEADS="$STATE_DIR/latest_anomaly_leads.jsonl"

mkdir -p "$RUN_DIR" "$STATE_DIR"
: > "$OUT_JSONL"

if [ ! -f "$RULES" ]; then
  jq -nc --arg utc "$UTC" '{utc:$utc,status:"BLOCKED",blocked_reason:"ANOMALY_RULES_MISSING",public_content_claim:"BLOCKED",no_fake_green:true}' > "$LATEST_LEADS"
  cp "$LATEST_LEADS" "$OUT_JSONL"
  exit 0
fi

hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}'; else shasum -a 256 "$1" | awk '{print $1}'; fi
}

emit_lead() {
  local lane="$1" source_path="$2" rule_id="$3" severity="$4" label="$5" evidence="$6"
  evidence="$(printf '%s' "$evidence" | tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g' | cut -c1-420)"
  jq -nc \
    --arg utc "$UTC" \
    --arg lane "$lane" \
    --arg source_path "$source_path" \
    --arg rule_id "$rule_id" \
    --arg severity "$severity" \
    --arg label "$label" \
    --arg evidence "$evidence" \
    '{utc:$utc,lane:$lane,source_path:$source_path,rule_id:$rule_id,severity:$severity,label:$label,evidence_excerpt:$evidence,claim_status:"ANOMALY_LEAD_ONLY",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",human_review_required:true,no_fake_green:true}' >> "$OUT_JSONL"
}

scan_text_file() {
  local f="$1" rel lane
  rel="${f#$ROOT/}"
  lane="GLOBAL"
  case "$rel" in
    projects/mn-fiscal-replay/live_fetch/*/*) lane="$(printf '%s' "$rel" | cut -d/ -f4)" ;;
    projects/mn-fiscal-replay/boss_bre/*) lane="BOSS_BRE" ;;
  esac

  jq -c '.rules[]' "$RULES" | while IFS= read -r rule; do
    rule_id="$(jq -r '.id' <<<"$rule")"
    severity="$(jq -r '.severity' <<<"$rule")"
    label="$(jq -r '.label' <<<"$rule")"
    pattern="$(jq -r '.pattern' <<<"$rule")"
    match="$(grep -Einm 1 "$pattern" "$f" 2>/dev/null || true)"
    if [ -n "$match" ]; then
      emit_lead "$lane" "$rel" "$rule_id" "$severity" "$label" "$match"
    fi
  done
}

# Scan forensic outputs, receipts, sweep summaries, source text extracts, and logs.
while IFS= read -r -d '' f; do
  scan_text_file "$f"
done < <(find "$ROOT/projects/mn-fiscal-replay" -type f \( \
  -name '*.txt' -o -name '*.md' -o -name '*.json' -o -name '*.jsonl' -o -name '*.diff' \
\) -print0 | sort -z)

LEAD_COUNT="$(wc -l < "$OUT_JSONL" | tr -d ' ')"
HIGH_COUNT="$(jq -sr '[.[] | select(.severity=="HIGH")] | length' "$OUT_JSONL")"
MED_COUNT="$(jq -sr '[.[] | select(.severity=="MEDIUM")] | length' "$OUT_JSONL")"
LOW_COUNT="$(jq -sr '[.[] | select(.severity=="LOW")] | length' "$OUT_JSONL")"
UNIQUE_LANES="$(jq -sr '[.[] .lane] | unique | length' "$OUT_JSONL")"
OUT_HASH="$(hash_file "$OUT_JSONL")"

cp "$OUT_JSONL" "$LATEST_LEADS"

cat > "$PUBLIC_MD" <<MD
# Boss Bre Minnesota Anomaly Board

UTC: $UTC

## Status

- Anomaly leads: $LEAD_COUNT
- HIGH: $HIGH_COUNT
- MEDIUM: $MED_COUNT
- LOW: $LOW_COUNT
- Unique lanes: $UNIQUE_LANES
- Leads hash: sha256:$OUT_HASH

## Doctrine

Boss Bre publishes **audit leads**, not fraud verdicts.

- PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW
- HUMAN_REVIEW_REQUIRED: TRUE
- NO_FAKE_GREEN: ACTIVE
- CLAIM TYPE: ANOMALY_LEAD_ONLY

## Latest leads

\`\`\`json
$(jq -s '.[0:25]' "$OUT_JSONL")
\`\`\`
MD

jq -n \
  --arg utc "$UTC" \
  --arg anomaly_leads_path "${OUT_JSONL#$ROOT/}" \
  --arg latest_leads_path "${LATEST_LEADS#$ROOT/}" \
  --arg public_board_path "${PUBLIC_MD#$ROOT/}" \
  --arg sha256 "$OUT_HASH" \
  --argjson lead_count "$LEAD_COUNT" \
  --argjson high_count "$HIGH_COUNT" \
  --argjson medium_count "$MED_COUNT" \
  --argjson low_count "$LOW_COUNT" \
  --argjson unique_lanes "$UNIQUE_LANES" \
  '{utc:$utc,status:"ANOMALY_SCAN_COMPLETE",lead_count:$lead_count,high_count:$high_count,medium_count:$medium_count,low_count:$low_count,unique_lanes:$unique_lanes,anomaly_leads_path:$anomaly_leads_path,latest_leads_path:$latest_leads_path,public_board_path:$public_board_path,sha256:$sha256,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"ANOMALY_LEAD_ONLY",human_review_required:true,no_fake_green:true}' \
  > "$STATE_DIR/latest_anomaly_summary.json"

echo "=== Boss Bre anomaly detector complete ==="
echo "Leads: $LEAD_COUNT"
echo "High: $HIGH_COUNT Medium: $MED_COUNT Low: $LOW_COUNT"
echo "Public board: $PUBLIC_MD"
echo "PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW"
echo "NO_FAKE_GREEN: ACTIVE"
