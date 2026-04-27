#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-data/gov_ncc_001/source.json}"

command -v jq >/dev/null || { echo "MISSING_TOOL jq"; exit 1; }
command -v sha256sum >/dev/null || { echo "MISSING_TOOL sha256sum"; exit 1; }

leaf_id="$(jq -r '.leaf_id' "$FILE")"
schema="$(jq -r '.schema' "$FILE")"
account="$(jq -r '.source.account' "$FILE")"
date="$(jq -r '.source.posted_date' "$FILE")"
quote="$(jq -r '.source.quote' "$FILE")"
actor="$(jq -r '.claim.actor' "$FILE")"
action="$(jq -r '.claim.action' "$FILE")"
partner="$(jq -r '.claim.partner' "$FILE")"
status="$(jq -r '.verification.status' "$FILE")"

test "$leaf_id" = "gov_ncc_001"
test "$schema" = "gov_ncc_event_v1"
test "$account" = "@DOLOIG"
test "$date" = "2026-04-26"
test "$actor" = "DOL OIG"
test "$action" = "joined"
test "$partner" = "Homeland Security Task Force National Coordination Center"
test "$status" = "ASSERTED"

printf '%s\n' "$quote" | grep -F "DOL OIG officially joined" >/dev/null
printf '%s\n' "$quote" | grep -F "National Coordination Center" >/dev/null
printf '%s\n' "$quote" | grep -F "NCC Charter" >/dev/null

canonical="$(jq -cS . "$FILE")"
hash="$(printf '%s' "$canonical" | sha256sum | awk '{print $1}')"

receipt="_truth/receipts/${leaf_id}.receipt.json"

jq -n \
  --arg leaf_id "$leaf_id" \
  --arg schema "$schema" \
  --arg source_file "$FILE" \
  --arg source_hash "$hash" \
  --arg status "PASS" \
  --arg risk "coordination_without_public_shared_state" \
  '{
    leaf_id:$leaf_id,
    schema:$schema,
    status:$status,
    source_file:$source_file,
    canonical_sha256:$source_hash,
    finding:"Official source asserts inter-agency coordination; public shared-state verification not yet present.",
    risk:$risk
  }' | jq -cS . > "$receipt"

echo "GOV_NCC_EVENT_OK leaf=$leaf_id hash=$hash receipt=$receipt"
