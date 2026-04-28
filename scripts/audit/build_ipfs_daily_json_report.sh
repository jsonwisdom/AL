#!/usr/bin/env bash
set -euo pipefail

DAY="$(date -u +%F)"
ROOT="_truth/audit/ipfs_daily/$DAY"
mkdir -p "$ROOT" docs/audit/ipfs_daily

INV="$ROOT/inventory.jsonl"
MAN="$ROOT/manifest.json"

: > "$INV"

find _truth docs -type f -name '*.json' \
  ! -path '_truth/audit/ipfs_daily/*' \
  ! -path 'docs/audit/ipfs_daily/latest.json' \
  | LC_ALL=C sort \
  | while read -r f; do
      BYTES="$(wc -c < "$f" | tr -d ' ')"
      HASH="$(sha256sum "$f" | awk '{print $1}')"
      jq -cn \
        --arg path "$f" \
        --arg sha256 "$HASH" \
        --argjson bytes "$BYTES" \
        '{path:$path, sha256:$sha256, bytes:$bytes}'
    done > "$INV"

INV_HASH="$(sha256sum "$INV" | awk '{print $1}')"
COUNT="$(wc -l < "$INV" | tr -d ' ')"

IPFS_STATUS="IPFS_WAIT"
IPFS_CID="PENDING"

if command -v ipfs >/dev/null 2>&1; then
  IPFS_CID="$(ipfs add -Qr --cid-version=1 "$ROOT" || echo PENDING)"
  if [ "$IPFS_CID" != "PENDING" ]; then
    IPFS_STATUS="IPFS_PINNED"
  fi
fi

jq -cn \
  --arg repo "jsonwisdom/AL" \
  --arg system "Jay's Wisdom of Zero Trust" \
  --arg machine_layer "Computer Wisdom" \
  --arg memory_layer "ALMS" \
  --arg day "$DAY" \
  --arg inventory_sha256 "$INV_HASH" \
  --arg ipfs_status "$IPFS_STATUS" \
  --arg ipfs_cid "$IPFS_CID" \
  --argjson json_file_count "$COUNT" \
  '{
    report_id:"ALMS_DAILY_IPFS_JSON_AUDIT",
    repo:$repo,
    system:$system,
    machine_layer:$machine_layer,
    memory_layer:$memory_layer,
    date_utc:$day,
    json_file_count:$json_file_count,
    inventory_sha256:$inventory_sha256,
    ipfs_status:$ipfs_status,
    ipfs_cid:$ipfs_cid,
    verdict: (
      if $ipfs_status == "IPFS_PINNED"
      then "ALMS_IPFS_DAILY_JSON_LOCKED"
      else "ALMS_IPFS_DAILY_JSON_WAIT"
      end
    ),
    rule:"JSON files are inventoried daily, hashed canonically by file bytes, and pinned when IPFS CLI is available."
  }' > "$MAN"

cp "$MAN" docs/audit/ipfs_daily/latest.json

echo "ALMS_DAILY_IPFS_JSON_AUDIT_OK date=$DAY count=$COUNT inventory_sha256=$INV_HASH ipfs_status=$IPFS_STATUS ipfs_cid=$IPFS_CID"
