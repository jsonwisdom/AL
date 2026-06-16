#!/usr/bin/env bash
set -euo pipefail

EXPECTED="ALMS/ens/expected/jaywisdom.base.eth.required_txt_v0_1.json"
OBSERVED="ALMS/ens/observed/jaywisdom.base.eth.resolver_txt_v0_1.json"
PENDING="ALMS/ens/receipts/PENDING_UPDATE_jaywisdom.base.eth_REQUIRED_TXT_V0_1.json"

need(){ command -v "$1" >/dev/null 2>&1 || { echo "MISSING_TOOL $1"; exit 2; }; }
need jq
need date

test -f "$EXPECTED" || { echo "RED expected_manifest_missing path=$EXPECTED"; exit 1; }

SUBJECT="$(jq -r '.subject_name' "$EXPECTED")"
mapfile -t REQUIRED < <(jq -r '.required_txt[]' "$EXPECTED")

missing=()
if [ -f "$OBSERVED" ]; then
  for k in "${REQUIRED[@]}"; do
    v="$(jq -r --arg k "$k" '.txt[$k] // empty' "$OBSERVED")"
    [ -n "$v" ] || missing+=("$k")
  done
else
  missing=("${REQUIRED[@]}")
fi

if [ "${#missing[@]}" -eq 0 ]; then
  echo "GREEN subject=$SUBJECT rule=BYTE_MATCH_WITH_RESOLVER_ARTIFACT"
  exit 0
fi

if [ ! -f "$PENDING" ]; then
  echo "RED subject=$SUBJECT rule=MISSING_AND_UNEXPLAINED missing=${missing[*]}"
  exit 1
fi

jq -e '
  .receipt_type == "PENDING_UPDATE_RECEIPT_V0_1"
  and .subject_name == "jaywisdom.base.eth"
  and .no_fake_green == true
  and (.expires_at_utc | type == "string")
' "$PENDING" >/dev/null

EXP="$(jq -r '.expires_at_utc' "$PENDING")"
NOW_EPOCH="$(date -u +%s)"
EXP_EPOCH="$(date -u -d "$EXP" +%s)"

if [ "$NOW_EPOCH" -gt "$EXP_EPOCH" ]; then
  echo "RED_EXPIRED subject=$SUBJECT expired_at=$EXP missing=${missing[*]}"
  exit 1
fi

echo "YELLOW subject=$SUBJECT rule=MISSING_WITH_PENDING_UPDATE_RECEIPT expires_at=$EXP missing=${missing[*]}"
exit 0
