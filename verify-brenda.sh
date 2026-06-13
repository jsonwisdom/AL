#!/usr/bin/env bash
set -euo pipefail

EMISSION_ID="${1:-}"

if [ -z "$EMISSION_ID" ]; then
  echo "usage: ./verify-brenda.sh <emission_id>"
  exit 1
fi

DID="witnesses/brenda/brenda.did.json"
SPEC="witnesses/brenda/GATE_SPEC_v1.md"
EMISSION="external/brenda/emission-${EMISSION_ID}.json"
MANIFEST="external/brenda/MANIFEST"
MANIFEST_SIG="external/brenda/MANIFEST.sig"
BUNDLE="external/brenda/emission-${EMISSION_ID}.tar.gz"
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

if [ ! -f "$EMISSION" ] || [ ! -f "$MANIFEST" ] || [ ! -f "$MANIFEST_SIG" ]; then
  echo "FAIL gate_2: missing emission, MANIFEST, or MANIFEST.sig"
  exit 1
fi

if [ ! -f "$BUNDLE" ]; then
  echo "FAIL gate_3: missing external bundle"
  exit 1
fi

if [ -f "$VETO" ] && grep -q '"veto"[[:space:]]*:[[:space:]]*true' "$VETO"; then
  if [ -f "$VETO_SIG" ]; then
    echo "RED gate_6: signed veto active"
    exit 2
  fi
  echo "FAIL gate_6: veto true but signature missing"
  exit 1
fi

if ! grep -q '"expires_at"' "$EMISSION" 2>/dev/null; then
  echo "FAIL gate_7: expires_at missing"
  exit 1
fi

echo "FAIL: cryptographic signature verification not enabled yet"
echo "state=YELLOW_BRENDA_WITNESS_ONLY"
exit 1
