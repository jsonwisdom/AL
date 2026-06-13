#!/usr/bin/env bash
set -euo pipefail

EMISSION_ID="${1:-}"

if [ -z "$EMISSION_ID" ]; then
  echo "usage: ./verify-brenda.sh <emission_id>"
  exit 1
fi

DID="witnesses/brenda/brenda.did.json"
SPEC="witnesses/brenda/GATE_SPEC_v1.md"
PUB="witnesses/brenda/brenda_ed25519.pub"

EMISSION="external/brenda/emission-${EMISSION_ID}.json"
MANIFEST="external/brenda/MANIFEST"
MANIFEST_SIG="external/brenda/MANIFEST.sig"
BUNDLE="external/brenda/emission-${EMISSION_ID}.tar.gz"
BUNDLE_SHA="external/brenda/emission-${EMISSION_ID}.bundle.sha256"
REPORTED="external/brenda/reported.txt"

VETO="witnesses/brenda/veto.json"
VETO_SIG="witnesses/brenda/veto.sig"

echo "== BRENDA VERIFY =="
echo "emission_id=$EMISSION_ID"

if [ ! -f "$SPEC" ] || [ ! -f "$DID" ]; then
  echo "FAIL gate_1: missing spec or DID"
  exit 1
fi

if grep -q "PLACEHOLDER_NOT_ACTIVE" "$DID"; then
  echo "FAIL gate_1: DID placeholder not active"
  exit 1
fi

if [ ! -f "$PUB" ]; then
  echo "FAIL gate_1: public key missing"
  exit 1
fi

echo "PASS gate_1: DID and public key present"

if [ ! -f "$EMISSION" ] || [ ! -f "$MANIFEST" ] || [ ! -f "$MANIFEST_SIG" ]; then
  echo "FAIL gate_2: missing emission, MANIFEST, or MANIFEST.sig"
  exit 1
fi

echo "PASS gate_2: signed emission materials present"

if [ ! -f "$BUNDLE" ] || [ ! -f "$BUNDLE_SHA" ]; then
  echo "FAIL gate_3: missing bundle or bundle hash"
  exit 1
fi

sha256sum -c "$BUNDLE_SHA"

echo "PASS gate_3: bundle hash verifies"

TMP="$(mktemp -d)"
tar -xzf "$BUNDLE" -C "$TMP"
sha256sum -c "$TMP/artifact_hashes.sha256"

echo "PASS gate_4: unpacked artifact hashes verify"

if [ ! -f "$REPORTED" ]; then
  echo "FAIL gate_5: reported binding missing"
  exit 1
fi

if ! grep -q "BRENDA_EXTERNAL_REPORT" "$REPORTED"; then
  echo "FAIL gate_5: reported binding malformed"
  exit 1
fi

echo "PASS gate_5: reported binding present"

if [ ! -f "$VETO" ] || [ ! -f "$VETO_SIG" ]; then
  echo "FAIL gate_6: veto file or signature missing"
  exit 1
fi

set +e
openssl pkeyutl -verify -rawin -pubin -inkey "$PUB" -sigfile "$VETO_SIG" -in "$VETO" >/tmp/brenda_veto_verify.log 2>&1
SIG_CODE="$?"
set -e

if [ "$SIG_CODE" != "0" ]; then
  cat /tmp/brenda_veto_verify.log
  echo "BRENDA_SIG_INVALID"
  exit 1
fi

if grep -q '"veto"[[:space:]]*:[[:space:]]*true' "$VETO"; then
  echo "BRENDA_VETO_ACTIVE"
  exit 2
fi

EXPIRES="$(jq -r '.expires_at_utc // empty' "$VETO")"

if [ -z "$EXPIRES" ]; then
  echo "FAIL gate_6: veto expires_at_utc missing"
  exit 1
fi

NOW_EPOCH="$(date -u +%s)"
EXP_EPOCH="$(date -u -d "$EXPIRES" +%s 2>/dev/null || echo 0)"

if [ "$EXP_EPOCH" = "0" ]; then
  echo "FAIL gate_6: veto expiry unparsable"
  exit 1
fi

if [ "$NOW_EPOCH" -gt "$EXP_EPOCH" ]; then
  echo "BRENDA_VETO_EXPIRED"
  exit 3
fi

echo "PASS gate_6: veto=false, signature valid, not expired"

RESOLVER_STATUS="witnesses/brenda/resolver_status.json"

if [ ! -f "$RESOLVER_STATUS" ]; then
  echo "FAIL gate_7: resolver status witness missing"
  echo "state=YELLOW_BRENDA_GATE_7_RESOLVER_MISSING"
  exit 1
fi

if ! jq -e '.txt_key == "brenda.status"' "$RESOLVER_STATUS" >/dev/null; then
  echo "FAIL gate_7: resolver txt_key mismatch"
  exit 1
fi

if ! jq -e '.txt_value == "ACTIVE"' "$RESOLVER_STATUS" >/dev/null; then
  echo "FAIL gate_7: brenda.status not ACTIVE"
  exit 1
fi

if ! jq -e '.no_fake_green == true and .authority == false' "$RESOLVER_STATUS" >/dev/null; then
  echo "FAIL gate_7: resolver witness boundary flags invalid"
  exit 1
fi

echo "PASS gate_7: resolver witness ACTIVE"
echo "BRENDA_ALL_LOCAL_GATES_PASS"
echo "state=BRENDA_LOCAL_ENFORCING_CANDIDATE"
exit 0
