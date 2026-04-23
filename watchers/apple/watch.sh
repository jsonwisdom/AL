#!/usr/bin/env bash
set -euo pipefail
TARGET_URL="https://www.apple.com/legal/privacy/"
SOURCE_ID="apple_privacy_page"
TIMESTAMP="$(date -u +%FT%TZ)"
STATE_FILE="_truth/state.json"
python3 -c 'import bs4' >/dev/null 2>&1 || { echo "FAIL: missing python3 bs4" >&2; exit 1; }
RAW_DIR="_truth/detect/${SOURCE_ID}"
mkdir -p "$RAW_DIR"
RAW_FILE="${RAW_DIR}/${TIMESTAMP}.html"
NORM_FILE="${RAW_DIR}/${TIMESTAMP}.txt"
HTTP_STATUS="$(curl --max-time 30 -A "ALMS-Watcher/1.0" -sL -w '%{http_code}' -o "$RAW_FILE" "$TARGET_URL")" || { echo "FAIL: fetch" >&2; exit 1; }
[[ "$HTTP_STATUS" == "200" ]] || { echo "FAIL: http ${HTTP_STATUS}" >&2; exit 1; }
./normalize/html_to_text.sh "$RAW_FILE" > "$NORM_FILE"
RAW_HASH="$(sha256sum "$RAW_FILE" | cut -d' ' -f1)"
NORM_HASH="$(sha256sum "$NORM_FILE" | cut -d' ' -f1)"
PREV_HASH=""
PREV_NORM_ARTIFACT=""
if [[ -f "$STATE_FILE" ]]; then
  PREV_HASH="$(jq -r ".${SOURCE_ID}.last_normalized_hash // empty" "$STATE_FILE")"
  PREV_NORM_ARTIFACT="$(jq -r ".${SOURCE_ID}.last_normalized_artifact_path // empty" "$STATE_FILE")"
fi
if [[ -z "${PREV_HASH}" ]]; then
  EVENT_KIND="BASELINE_ESTABLISHED"
  CLAIM_PREDICATE="established"
  CLAIM_OBJECT="baseline public content"
elif [[ "sha256:${NORM_HASH}" == "${PREV_HASH}" ]]; then
  echo "{\"event\":\"NO_CHANGE\",\"source_id\":\"${SOURCE_ID}\",\"detected_at\":\"${TIMESTAMP}\"}"
  exit 0
else
  EVENT_KIND="CHANGE_DETECTED"
  CLAIM_PREDICATE="changed"
  CLAIM_OBJECT="public content"
fi
CANDIDATE_FILE="${RAW_DIR}/${TIMESTAMP}_candidate.json"
cat > "$CANDIDATE_FILE" <<JSON
{"type":"CLAIM_CANDIDATE","version":"1.0","source_id":"${SOURCE_ID}","detected_at":"${TIMESTAMP}","fetch":{"url":"${TARGET_URL}","method":"GET","status":${HTTP_STATUS}},"evidence":{"raw_hash":"sha256:${RAW_HASH}","normalized_hash":"sha256:${NORM_HASH}","previous_normalized_hash":"${PREV_HASH}","diff_summary":"","artifact_path":"${RAW_DIR}/${TIMESTAMP}.html"},"claim":{"subject":"${SOURCE_ID}","predicate":"${CLAIM_PREDICATE}","object":"${CLAIM_OBJECT}"},"norm_spec":"v1","routing":{"vector":[0,1,1],"priority":"high","verify_mode":"document_diff"}}
JSON
EMIT_JSON="$(./claims/emit_claim_candidate.sh "$CANDIDATE_FILE")"
INPUT="$(jq -r '.input' <<< "$EMIT_JSON")"
HASH_JSON="$(./verify.sh "$INPUT")"
HASH="$(printf "%s" "$HASH_JSON" | jq -r .hash)"
[[ ${#HASH} -eq 64 ]] || { echo "FAIL: verify.sh returned invalid hash" >&2; exit 1; }
jq --arg ts "$TIMESTAMP" --arg hash "sha256:${NORM_HASH}" --arg raw "$RAW_FILE" --arg norm "$NORM_FILE" --arg verified_hash "$HASH" --arg candidate "$CANDIDATE_FILE" ".${SOURCE_ID}.last_detected_at = \$ts | .${SOURCE_ID}.last_normalized_hash = \$hash | .${SOURCE_ID}.last_raw_artifact_path = \$raw | .${SOURCE_ID}.last_normalized_artifact_path = \$norm | .${SOURCE_ID}.last_verified_hash = \$verified_hash | .${SOURCE_ID}.last_candidate_path = \$candidate" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
echo "{\"event\":\"${EVENT_KIND}\",\"source_id\":\"${SOURCE_ID}\",\"detected_at\":\"${TIMESTAMP}\",\"verified_hash\":\"${HASH}\"}"
