#!/usr/bin/env bash
set -euo pipefail

URL="${1:-https://al-dnlo.onrender.com}"
TMPDIR="${TMPDIR:-/tmp}"
REPORT="$TMPDIR/ev015-report.txt"

: > "$REPORT"

log() {
  echo "$@" | tee -a "$REPORT"
}

check_200() {
  local path="$1"
  local label="$2"
  local body status
  body="$(curl --max-time 30 -sS -w '\nHTTP_STATUS=%{http_code}\n' "$URL$path")"
  status="$(printf '%s' "$body" | awk -F= '/HTTP_STATUS=/{print $2}' | tail -1)"
  log "=== $label $path ==="
  printf '%s\n' "$body" | tee -a "$REPORT"
  if [ "$status" != "200" ]; then
    log "FAIL: $label returned HTTP $status"
    return 1
  fi
}

log "EV-015 AUTHORITY GATE"
log "url=$URL"
log "authority_target=false"
log ""

check_200 "/" "root"
check_200 "/health" "health"
check_200 "/identity" "identity"
check_200 "/hash" "hash"
check_200 "/replay_url" "replay_url"

log "=== emit #1 ==="
emit1="$(curl --max-time 30 -sS "$URL/emit")"
printf '%s\n' "$emit1" | tee -a "$REPORT"
printf '%s' "$emit1" | grep -q 'EXIT_CODE=0'
uid1="$(printf '%s' "$emit1" | sed -n 's/^EMITTED uid://p' | tail -1)"

log "=== verify #1 ==="
verify1="$(curl --max-time 30 -sS "$URL/verify")"
printf '%s\n' "$verify1" | tee -a "$REPORT"
printf '%s' "$verify1" | grep -q 'REPLAY_OK'
printf '%s' "$verify1" | grep -q 'EXIT_CODE=0'

log "=== emit #2 ==="
emit2="$(curl --max-time 30 -sS "$URL/emit")"
printf '%s\n' "$emit2" | tee -a "$REPORT"
printf '%s' "$emit2" | grep -q 'EXIT_CODE=0'
uid2="$(printf '%s' "$emit2" | sed -n 's/^EMITTED uid://p' | tail -1)"

log "=== verify #2 ==="
verify2="$(curl --max-time 30 -sS "$URL/verify")"
printf '%s\n' "$verify2" | tee -a "$REPORT"
printf '%s' "$verify2" | grep -q 'REPLAY_OK'
printf '%s' "$verify2" | grep -q 'EXIT_CODE=0'

log ""
log "uid1=$uid1"
log "uid2=$uid2"
log "surface=PASS"
log "identity=PASS"
log "commit_hash=PASS"
log "replay_url=PASS"
log "witness_emit=PASS"
log "witness_replay=PASS"
log "authority=false"
log "classification=READY_FOR_AUTHORITY_GATE"

if command -v sha256sum >/dev/null 2>&1; then
  digest="$(sha256sum "$REPORT" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  digest="$(shasum -a 256 "$REPORT" | awk '{print $1}')"
else
  digest="sha256_unavailable"
fi

log "receipt_sha256=$digest"
log "next_action=HOLD_AUTHORITY_FALSE_UNTIL_POLICY_SIGNOFF"
