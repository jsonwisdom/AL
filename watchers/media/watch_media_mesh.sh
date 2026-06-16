#!/usr/bin/env bash
set -euo pipefail

# ALMS MEDIA MESH WATCHER — V1.1
# PURPOSE: Expand URLs → extract normalized host → record redirect count → generate intake JSON
# SCHEMA: schemas/media_source_intake_v1.json

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <input_url> <discovered_from> [event_id]" >&2
  exit 2
fi

INPUT_URL="$1"
DISCOVERED_FROM="$2"
EVENT_ID="${3:-FED.MUSK_OPENAI_TRIAL}"
TIMESTAMP_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

case "$DISCOVERED_FROM" in
  reddit|x|search|article|archive|manual) ;;
  *)
    echo "INVALID_DISCOVERED_FROM=$DISCOVERED_FROM" >&2
    exit 3
    ;;
esac

# 1. Expand URL. No trust in shortlinks.
RESOLVED_URL="$(curl -Ls -o /dev/null -w '%{url_effective}' "$INPUT_URL")"

# 1a. Record redirect chain depth as structural signal only.
REDIRECT_COUNT="$(curl -IL "$INPUT_URL" 2>/dev/null | grep -c '^HTTP/')"

# 2. Extract normalized host/root surface. Registrable-domain reduction is handled by later clusterer.
ROOT_DOMAIN="$(printf '%s\n' "$RESOLVED_URL" | awk -F[/:] '{print tolower($4)}')"

# 3. Publisher identity is unresolved at intake.
PUBLISHER_IDENTITY="UNKNOWN"

# 4. Claim extraction is handled by a later extractor.
CLAIM_EXCERPT=""

# 5. Default classification until matching engine runs.
MATCHES_PRIMARY=false
MUTATION_TYPE="none"
CLASSIFICATION="INVALID"

jq -n -cS \
  --arg classification "$CLASSIFICATION" \
  --arg claim_excerpt "$CLAIM_EXCERPT" \
  --arg discovered_from "$DISCOVERED_FROM" \
  --arg event_id "$EVENT_ID" \
  --arg mutation_type "$MUTATION_TYPE" \
  --arg publisher_identity "$PUBLISHER_IDENTITY" \
  --arg resolved_url "$RESOLVED_URL" \
  --arg root_domain "$ROOT_DOMAIN" \
  --arg source_url "$INPUT_URL" \
  --arg timestamp_utc "$TIMESTAMP_UTC" \
  --argjson matches_primary "$MATCHES_PRIMARY" \
  --argjson redirect_count "$REDIRECT_COUNT" \
  '{classification:$classification,claim_excerpt:$claim_excerpt,discovered_from:$discovered_from,event_id:$event_id,matches_primary:$matches_primary,mutation_type:$mutation_type,publisher_identity:$publisher_identity,redirect_count:$redirect_count,resolved_url:$resolved_url,root_domain:$root_domain,source_url:$source_url,timestamp_utc:$timestamp_utc}'
