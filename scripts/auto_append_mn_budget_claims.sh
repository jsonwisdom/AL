#!/usr/bin/env bash
set -euo pipefail

CANDIDATES="${CANDIDATES:-_truth/snapshots/mn_budget_claim_candidates.tsv}"
LIMIT="${LIMIT:-2}"
DRY_RUN="${DRY_RUN:-1}"
AUTO_COMMIT="${AUTO_COMMIT:-0}"
AUTO_PUSH="${AUTO_PUSH:-0}"
BRANCH="${BRANCH:-master}"
HASH_REGISTRY="${HASH_REGISTRY:-data/claim_hashes.txt}"

SOURCE_HASH="sha256:c4ac46e46b80b42a6abc24edbe0480ac4983cb0090a758bd7458b2ea62faca69"
EXTRACT_HASH="sha256:da5ad1bbe192eae56c96cf574025b8f915839d29c78c69e8d6b98a0ad9d7d917"

command -v jq >/dev/null 2>&1 || { echo "AUTO_APPEND_FAIL reason=missing_jq" >&2; exit 2; }
command -v sha256sum >/dev/null 2>&1 || { echo "AUTO_APPEND_FAIL reason=missing_sha256sum" >&2; exit 2; }

test -f "$CANDIDATES" || { echo "AUTO_APPEND_FAIL reason=missing_candidates path=$CANDIDATES" >&2; exit 1; }

mkdir -p claims/mn
mkdir -p "$(dirname "$HASH_REGISTRY")"
touch "$HASH_REGISTRY"

git_guard() {
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "AUTO_GIT_FAIL reason=not_git_repo" >&2; exit 1; }
}

slugify() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/&/and/g; s/[^a-z0-9]/_/g; s/_\+/_/g; s/^_//; s/_$//'
}

already_manifested() {
  local claim_text="$1"
  if [ -f docs/verified-claims.json ]; then
    jq -e --arg t "$claim_text" '.claims[]? | select(.claim_text == $t)' docs/verified-claims.json >/dev/null
  else
    return 1
  fi
}

next_num() {
  local max
  max=$(find claims/mn -type f -name 'mn_[0-9][0-9][0-9]_*.canonical.json' \
    | sed -E 's#.*mn_([0-9]{3})_.*#\1#' \
    | sort -n \
    | tail -n 1)
  if [ -z "${max:-}" ]; then
    printf '001'
  else
    printf '%03d' "$((10#$max + 1))"
  fi
}

added=0
while IFS=$'\t' read -r line_hint label value claim_text; do
  [ -n "${claim_text:-}" ] || continue

  claim_key_hash="$(printf '%s|%s|%s' "$label" "$value" "$SOURCE_HASH" | sha256sum | awk '{print $1}')"

  if grep -q "^${claim_key_hash}[[:space:]]" "$HASH_REGISTRY"; then
    echo "AUTO_DEDUPE_SKIP hash=$claim_key_hash line=$line_hint label=$label value=$value"
    continue
  fi

  if already_manifested "$claim_text"; then
    echo "AUTO_SKIP already_manifested line=$line_hint label=$label"
    continue
  fi

  num=$(next_num)
  slug=$(slugify "$label")
  canonical="claims/mn/mn_${num}_${slug}.canonical.json"

  echo "AUTO_CANDIDATE num=$num line=$line_hint hash=$claim_key_hash claim_text=$claim_text"

  if [ "$DRY_RUN" = "1" ]; then
    added=$((added + 1))
    [ "$added" -ge "$LIMIT" ] && break
    continue
  fi

  append_out=$(bash scripts/append_mn_claim.sh "$claim_text")
  echo "$append_out"
  claim_id=$(printf '%s\n' "$append_out" | sed -n 's/.*claim_id=\([^ ]*\).*/\1/p')
  text_hash=$(printf '%s\n' "$append_out" | sed -n 's/.*text_hash=\([^ ]*\).*/\1/p')

  if [ -z "$claim_id" ] || [ -z "$text_hash" ]; then
    echo "AUTO_APPEND_FAIL reason=append_parse_failed output=$append_out" >&2
    exit 1
  fi

  jq -n \
    --arg claim_id "$claim_id" \
    --arg claim_text "$claim_text" \
    --arg line_hint "$line_hint" \
    --arg line_match "$claim_text" \
    --arg text_hash "$text_hash" \
    --arg source_hash "$SOURCE_HASH" \
    --arg extract_hash "$EXTRACT_HASH" \
    '{
      claim_id: $claim_id,
      jurisdiction: "MN",
      claim_type: "budget_line_item",
      claim_text: $claim_text,
      source: {
        agency: "Minnesota Management and Budget",
        document: "February 2026 Budget and Economic Forecast",
        source_file: "sources/mn/mmb-feb-2026-forecast.pdf",
        source_hash: $source_hash,
        extract_file: "_truth/sources/mmb-feb-2026-forecast.txt",
        extract_hash: $extract_hash,
        line_hint: ($line_hint|tonumber),
        line_match: $line_match,
        source_anchor_status: "anchored"
      },
      artifacts: {
        text_hash: $text_hash,
        ledger: "_truth/ledger.jsonl"
      },
      verification: {
        ledger_status: "verified",
        verified_by: "verify.sh"
      },
      status: "source_anchored"
    }' > "$canonical"

  printf '%s\t%s\t%s\t%s\n' "$claim_key_hash" "$label" "$value" "$claim_id" >> "$HASH_REGISTRY"

  echo "AUTO_CANONICAL path=$canonical"
  added=$((added + 1))
  [ "$added" -ge "$LIMIT" ] && break

done < "$CANDIDATES"

if [ "$DRY_RUN" = "1" ]; then
  echo "AUTO_APPEND_DRY_RUN_OK candidates_to_add=$added limit=$LIMIT"
  exit 0
fi

bash scripts/build_verified_claims_manifest.sh
bash scripts/check_verified_claims_manifest.sh

if [ "$AUTO_COMMIT" = "1" ]; then
  git_guard
  if [ "$added" -eq 0 ]; then
    echo "AUTO_COMMIT_SKIP reason=no_new_claims"
  else
    git add _truth/ledger.jsonl docs/verified-claims.json claims/mn/*.canonical.json "$HASH_REGISTRY"
    if git diff --cached --quiet; then
      echo "AUTO_COMMIT_SKIP reason=no_staged_changes"
    else
      ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
      git commit -m "AUTO: ingest ${added} MN budget claims | ${ts}"
      echo "AUTO_COMMIT_OK added=$added"
      if [ "$AUTO_PUSH" = "1" ]; then
        git push origin "$BRANCH"
        echo "AUTO_PUSH_OK branch=$BRANCH"
      fi
    fi
  fi
fi

echo "AUTO_APPEND_OK added=$added manifest=docs/verified-claims.json hash_registry=$HASH_REGISTRY"
