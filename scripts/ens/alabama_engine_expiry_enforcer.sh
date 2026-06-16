#!/usr/bin/env bash
set -euo pipefail

PENDING="ALMS/ens/receipts/PENDING_UPDATE_jaywisdom.base.eth_REQUIRED_TXT_V0_1.json"
CHECKER="scripts/ens/alabama_engine_divergence_check.sh"

need(){ command -v "$1" >/dev/null 2>&1 || { echo "MISSING_TOOL $1"; exit 2; }; }
need jq
need date

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
