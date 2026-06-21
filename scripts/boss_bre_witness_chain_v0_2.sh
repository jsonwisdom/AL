#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
BASE="$ROOT/projects/mn-fiscal-replay/boss_bre"
WITNESS="$BASE/witness_feed"
EVENT="$WITNESS/latest_witness_event.json"
CHAIN="$WITNESS/witness_chain.jsonl"
MANIFEST="$WITNESS/latest_witness_manifest.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$WITNESS"

sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}

if [ ! -s "$EVENT" ]; then
  jq -n \
    --arg utc "$UTC" \
    '{artifact:"latest_witness_manifest.json",version:"0.2",generated_utc:$utc,status:"WITNESS_EVENT_MISSING",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",human_review_required:true,no_fake_green:true}' \
    > "$MANIFEST"
  echo "WITNESS_CHAIN_BLOCKED: latest_witness_event.json missing"
  exit 0
fi

previous_event_sha256="GENESIS"
if [ -s "$CHAIN" ]; then
  previous_event_sha256="$(tail -n 1 "$CHAIN" | sha256sum | awk '{print $1}')"
fi

current_event_sha256="$(sha_file "$EVENT")"
chain_event_id="sha256:$(printf '%s|%s|%s' "$previous_event_sha256" "$current_event_sha256" "$UTC" | sha256sum | awk '{print $1}')"

jq -c \
  --arg chain_event_id "$chain_event_id" \
  --arg previous_event_sha256 "$previous_event_sha256" \
  --arg current_event_sha256 "$current_event_sha256" \
  '. + {chain_event_id:$chain_event_id, previous_event_sha256:$previous_event_sha256, current_event_sha256:$current_event_sha256}' \
  "$EVENT" >> "$CHAIN"

chain_count="$(wc -l < "$CHAIN" | tr -d ' ')"
chain_sha256="$(sha_file "$CHAIN")"

jq -n \
  --arg utc "$UTC" \
  --arg latest_event "${EVENT#$ROOT/}" \
  --arg current_event_sha256 "$current_event_sha256" \
  --arg previous_event_sha256 "$previous_event_sha256" \
  --arg chain "${CHAIN#$ROOT/}" \
  --arg chain_sha256 "$chain_sha256" \
  --argjson chain_count "$chain_count" \
  '{artifact:"latest_witness_manifest.json",version:"0.2",generated_utc:$utc,status:"WITNESS_CHAIN_UPDATED",latest_event_path:$latest_event,latest_event_sha256:$current_event_sha256,previous_event_sha256:$previous_event_sha256,chain_path:$chain,chain_sha256:$chain_sha256,chain_event_count:$chain_count,claim_status:"WITNESS_EVENT_ONLY",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",human_review_required:true,no_fake_green:true}' \
  > "$MANIFEST"

echo "WITNESS_CHAIN_UPDATED"
echo "previous_event_sha256=$previous_event_sha256"
echo "current_event_sha256=$current_event_sha256"
echo "chain_sha256=$chain_sha256"
echo "PUBLIC_CONTENT_CLAIM=BLOCKED_PENDING_HUMAN_REVIEW"
echo "NO_FAKE_GREEN=ACTIVE"
