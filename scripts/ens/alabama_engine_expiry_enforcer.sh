#!/usr/bin/env bash
set -euo pipefail

JOY_ANCHOR="JOY/eas/anchors/JOY_REPLAY_BOOTSTRAP_V0_1.json"
PENDING="ALMS/ens/receipts/PENDING_UPDATE_jaywisdom.base.eth_REQUIRED_TXT_V0_1.json"
CHECKER="scripts/ens/alabama_engine_divergence_check.sh"

need(){ command -v "$1" >/dev/null 2>&1 || { echo "MISSING_TOOL $1"; exit 2; }; }
need jq
need date

if [ -f "$JOY_ANCHOR" ]; then
  jq -e '
    .anchor_type == "JOY_REPLAY_BOOTSTRAP_V0_1"
    and .chain == "base"
    and .chain_id == 8453
    and .authority == false
    and .verified_replay == false
    and .classification == "BOOTSTRAP_NOT_VERIFIED"
    and .no_fake_green == true
    and .load_verified == false
  ' "$JOY_ANCHOR" >/dev/null || {
    echo "RED joy_eas_anchor_invalid path=$JOY_ANCHOR"
    exit 1
  }

  bash "$CHECKER"
  echo "EXPIRY_ENFORCER_OK joy_eas_anchor_present load_verified=false"
  exit 0
fi

test -f "$PENDING" || {
  echo "RED pending_update_missing"
  exit 1
}

EXP="$(jq -r '.expires_at_utc // empty' "$PENDING")"
NO_FAKE="$(jq -r '.no_fake_green // false' "$PENDING")"

[ "$NO_FAKE" = "true" ] || {
  echo "RED signature_policy_fail no_fake_green_not_true"
  exit 1
}

NOW_EPOCH="$(date -u +%s)"
EXP_EPOCH="$(date -u -d "$EXP" +%s)"

if [ "$NOW_EPOCH" -gt "$EXP_EPOCH" ]; then
  echo "RED_EXPIRED pending_update_expired expires_at=$EXP"
  exit 1
fi

bash "$CHECKER"
echo "EXPIRY_ENFORCER_OK pending_update_unexpired expires_at=$EXP"
