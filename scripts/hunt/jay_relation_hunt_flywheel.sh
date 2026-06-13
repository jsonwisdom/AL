#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

HUNT_ROOT="${HUNT_ROOT:-$ROOT}"
DAYS="${DAYS:-30}"
MAX_REPOS="${MAX_REPOS:-40}"
MAX_COMMITS="${MAX_COMMITS:-250}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="ALMS/hunts/runs/jay_relation_hunt_$STAMP"

mkdir -p "$OUT"

SEED_RE='jaywisdom\.base\.eth|jaywisdom\.eth|0x992d94aA31dcD8fDb7d8E6885370ef8202AED399|0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5'
KEY_RE='schema_uid|schema_id|attestation_uid|attestation|attester|recipient|tx_hash|transaction_hash|transactionHash|EAS|eas|0x[a-fA-F0-9]{64}|bafy[a-zA-Z0-9]+|Qm[a-zA-Z0-9]{44}'
REGEX="$SEED_RE|$KEY_RE"

REPOS="$OUT/repos.txt"
CURRENT="$OUT/current_tracked_content_hits.tsv"
HISTORY="$OUT/last30d_patch_hits.tsv"
TOKENS="$OUT/extracted_uid_tx_tokens.txt"
SUMMARY="$OUT/SUMMARY.md"
MANIFEST="$OUT/manifest.json"

find "$HUNT_ROOT" -maxdepth 6 -type d -name .git \
  ! -path "*/.cache/*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.codex/*" \
  ! -path "*/.gemini/*" \
  ! -path "*/lib/forge-std/*" \
  ! -path "*/lib/openzeppelin-contracts/*" \
  | sed 's#/.git$##' | sort | head -n "$MAX_REPOS" > "$REPOS"

echo -e "repo\tfile\tline\tmatch" > "$CURRENT"
echo -e "repo\tcommit\tdate\tfile\tmatch" > "$HISTORY"

while IFS= read -r repo; do
  [ -d "$repo/.git" ] || continue
  echo "CURRENT $repo"

  timeout 20s git -C "$repo" grep -nIE "$REGEX" HEAD -- \
    '*.json' '*.jsonl' '*.md' '*.txt' '*.yml' '*.yaml' '*.sh' '*.sol' '*.js' '*.ts' 2>/dev/null |
  while IFS=: read -r ref file line text; do
    clean="$(printf '%s' "$text" | tr '\t' ' ' | head -c 260)"
    printf "%s\t%s\t%s\t%s\n" "$repo" "$file" "$line" "$clean" >> "$CURRENT"
  done || true
done < "$REPOS"

while IFS= read -r repo; do
  [ -d "$repo/.git" ] || continue
  echo "HISTORY $repo"

  git -C "$repo" log --all --since="$DAYS days ago" --format='%H%x09%aI' 2>/dev/null | head -n "$MAX_COMMITS" |
  while IFS=$'\t' read -r sha cdate; do
    [ -n "$sha" ] || continue

    timeout 8s git -C "$repo" show --pretty=format: --unified=0 --no-ext-diff "$sha" -- \
      '*.json' '*.jsonl' '*.md' '*.txt' '*.yml' '*.yaml' '*.sh' '*.sol' '*.js' '*.ts' 2>/dev/null |
    awk '/^\+\+\+ b\//{file=$0; sub(/^\+\+\+ b\//,"",file)} /^[+-][^+-]/{print file "\t" $0}' |
    grep -IE "$REGEX" |
    head -80 |
    while IFS=$'\t' read -r file text; do
      clean="$(printf '%s' "$text" | tr '\t' ' ' | head -c 260)"
      printf "%s\t%s\t%s\t%s\t%s\n" "$repo" "$sha" "$cdate" "$file" "$clean" >> "$HISTORY"
    done || true
  done
done < "$REPOS"

cat "$CURRENT" "$HISTORY" \
  | grep -Eo '0x[a-fA-F0-9]{40}|0x[a-fA-F0-9]{64}|bafy[a-zA-Z0-9]+|Qm[a-zA-Z0-9]{44}' \
  | sort -u > "$TOKENS" || true

REPO_COUNT="$(wc -l < "$REPOS" | tr -d ' ')"
CURRENT_COUNT="$(( $(wc -l < "$CURRENT") - 1 ))"
HISTORY_COUNT="$(( $(wc -l < "$HISTORY") - 1 ))"
TOKEN_COUNT="$(wc -l < "$TOKENS" | tr -d ' ')"

cat > "$SUMMARY" <<EOF2
# JAY_RELATION_HUNT_FLYWHEEL_RUN

STATUS: COMPLETE
TRUTH_STATE: OBSERVED
AUTHORITY: FALSE
NO_FAKE_GREEN: TRUE

Repos: $REPO_COUNT
Current hits: $CURRENT_COUNT
History hits: $HISTORY_COUNT
UID/TX/address/CID tokens: $TOKEN_COUNT

Final ruling: repo evidence only. Tokens are replay candidates, not chain proof.
EOF2

jq -n \
  --arg status "COMPLETE" \
  --arg truth_state "OBSERVED" \
  --argjson authority false \
  --argjson no_fake_green true \
  --arg out "$OUT" \
  --argjson repos "$REPO_COUNT" \
  --argjson current_hits "$CURRENT_COUNT" \
  --argjson history_hits "$HISTORY_COUNT" \
  --argjson token_count "$TOKEN_COUNT" \
  '{
    status:$status,
    truth_state:$truth_state,
    authority:$authority,
    no_fake_green:$no_fake_green,
    output_dir:$out,
    repos:$repos,
    current_hits:$current_hits,
    history_hits:$history_hits,
    token_count:$token_count,
    green:false,
    ruling:"repo evidence only; replay candidates require chain/resolver verification"
  }' > "$MANIFEST"

echo "== HUNT SUMMARY =="
cat "$SUMMARY"
echo
echo "== TOP TOKENS =="
sed -n '1,80p' "$TOKENS"
echo
echo "== OUTPUT =="
echo "$OUT"
