#!/usr/bin/env bash
set -euo pipefail
CANDIDATE_JSON="${1:-}"
[[ -f "$CANDIDATE_JSON" ]] || { echo "Usage: emit_claim_candidate.sh <candidate.json>" >&2; exit 1; }
jq -e '
  .source_id and .detected_at and
  .claim.subject and .claim.predicate and .claim.object and
  .evidence.raw_hash and .evidence.normalized_hash and .evidence.artifact_path and
  .norm_spec and .routing.vector
' "$CANDIDATE_JSON" >/dev/null 2>&1 || { echo "FAIL: missing required fields" >&2; exit 1; }
PREV_HASH="$(jq -r '.evidence.previous_normalized_hash // ""' "$CANDIDATE_JSON")"
if [[ "$PREV_HASH" == "" ]]; then
  EVENT="BASELINE_ESTABLISHED"
else
  EVENT="CHANGE_DETECTED"
fi
SOURCE_ID="$(jq -r '.source_id' "$CANDIDATE_JSON")"
SUBJECT="$(jq -r '.claim.subject' "$CANDIDATE_JSON")"
PREDICATE="$(jq -r '.claim.predicate' "$CANDIDATE_JSON")"
OBJECT="$(jq -r '.claim.object' "$CANDIDATE_JSON")"
DETECTED_AT="$(jq -r '.detected_at' "$CANDIDATE_JSON")"
VECTOR="$(jq -r '.routing.vector | @csv' "$CANDIDATE_JSON" | tr -d '"' | tr -d ' ')"
CLAIM_TEXT="$(printf "%s %s %s" "$SUBJECT" "$PREDICATE" "$OBJECT" | perl -MUnicode::Normalize -pe '$_ = NFC($_)' | perl -pe 's/[[:space:]]+/ /g; s/^ //; s/ $//')"
B64_CLAIM="$(printf "%s" "$CLAIM_TEXT" | base64 | tr -d '\n')"
INPUT="ALMS|v=1.1|t=${DETECTED_AT}|vector=[${VECTOR}]|claim_b64=${B64_CLAIM}"
cat <<OUTPUT
{"event":"${EVENT}","input":"${INPUT}","candidate":$(cat "$CANDIDATE_JSON")}
OUTPUT
