#!/usr/bin/env bash
set -euo pipefail

JOY_ANCHOR="JOY/eas/anchors/JOY_REPLAY_BOOTSTRAP_V0_1.json"
EXPECTED_SCHEMA_UID="0x5840bf1e71d72a83b820c132b93b3a284a5a07664928342b205938fda0af8055"
EXPECTED_ATTESTATION_UID="0x065812e1fd3825471415d1e8f7cf38f77a450ac9bf204e45af317e6930639a7e"
EXPECTED_ATTESTATION_TX="0x7c15cd42bdf73b3bae0fa7c16bf81c491fdb72b20289bd0b5a029a78e51eaab4"
EXPECTED_ATTESTER="0xC345B26094c63C69222Ee775189a3d3eaead5a84"

EXPECTED="ALMS/ens/expected/jaywisdom.base.eth.required_txt_v0_1.json"
OBSERVED="ALMS/ens/observed/jaywisdom.base.eth.resolver_txt_v0_1.json"
PENDING="ALMS/ens/receipts/PENDING_UPDATE_jaywisdom.base.eth_REQUIRED_TXT_V0_1.json"

need(){ command -v "$1" >/dev/null 2>&1 || { echo "MISSING_TOOL $1"; exit 2; }; }
need jq
need date

if [ -f "$JOY_ANCHOR" ]; then
  jq -e \
    --arg schema "$EXPECTED_SCHEMA_UID" \
    --arg uid "$EXPECTED_ATTESTATION_UID" \
    --arg tx "$EXPECTED_ATTESTATION_TX" \
    --arg attester "$EXPECTED_ATTESTER" \
    '
      .anchor_type == "JOY_REPLAY_BOOTSTRAP_V0_1"
      and .chain == "base"
      and .chain_id == 8453
      and .schema_uid == $schema
      and .attestation_uid == $uid
      and .attestation_tx == $tx
      and .attester == $attester
      and .transform_version == "v0.1.0"
      and .authority == false
      and .verified_replay == false
      and .classification == "BOOTSTRAP_NOT_VERIFIED"
      and .no_fake_green == true
      and .load_verified == false
    ' "$JOY_ANCHOR" >/dev/null || {
      echo "RED joy_eas_anchor_invalid path=$JOY_ANCHOR"
      exit 1
    }

  echo "PASS_BOOTSTRAP_ATTESTATION_ANCHOR schema_uid=$EXPECTED_SCHEMA_UID attestation_uid=$EXPECTED_ATTESTATION_UID load_verified=false"
  exit 0
fi

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
