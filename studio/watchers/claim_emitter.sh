#!/usr/bin/env bash
set -euo pipefail

emit_claim() {
  local claim_text="$1"
  local source_doc="$2"
  local line_hint="$3"

  mkdir -p _truth
  touch _truth/ledger.jsonl

  local claim_id
  claim_id="al_$(date +%s)_$$"

  local text_hash
  text_hash="$(printf "%s" "$claim_text" | sha256sum | awk '{print "sha256:"$1}')"

  local prev_hash="null"
  if [[ -s "_truth/ledger.jsonl" ]]; then
    local prev_line
    prev_line="$(tail -n 1 _truth/ledger.jsonl)"
    prev_hash="$(printf "%s" "$prev_line" | sha256sum | awk '{print "sha256:"$1}')"
  fi

  jq -cn \
    --arg claim_id "$claim_id" \
    --arg claim_text "$claim_text" \
    --arg source_doc "$source_doc" \
    --argjson line_hint "$line_hint" \
    --arg text_hash "$text_hash" \
    --arg prev_hash "$prev_hash" \
    '{
      claim_id:$claim_id,
      claim_text:$claim_text,
      source:{
        document:$source_doc,
        line_hint:$line_hint,
        watcher:"claim_emitter.sh"
      },
      artifacts:{
        text_hash:$text_hash
      },
      prev_hash:$prev_hash,
      status:"verified"
    }' >> _truth/ledger.jsonl
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  if [[ "$#" -lt 3 ]]; then
    echo "Usage: $0 CLAIM_TEXT SOURCE_DOC LINE_HINT" >&2
    exit 1
  fi
  emit_claim "$1" "$2" "$3"
fi
