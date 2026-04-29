#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="_truth/audit/alms_copilot_ready_${TS}.txt"
mkdir -p _truth/audit

{
echo "ALMS_COPILOT_READY_AUDIT_V1"
echo "time=$TS"
echo

echo "=== ROOT SURFACE CHECK ==="
CANON_ROOT="$(cat _truth/merkle/root.txt 2>/dev/null | tr -d '\n' || true)"
MANIFEST_ROOT="$(jq -r '.root // empty' _truth/merkle/manifest.json 2>/dev/null | sed 's/^sha256://')"
STATUS_ROOT="$(jq -r '.merkle_root // empty' status.json 2>/dev/null || true)"

echo "canonical_root=$CANON_ROOT"
echo "manifest_root=$MANIFEST_ROOT"
echo "status_root=$STATUS_ROOT"

[ "$CANON_ROOT" = "$MANIFEST_ROOT" ] && echo "CANONICAL_ROOT_MATCH=YES" || echo "CANONICAL_ROOT_MATCH=NO"
[ "$STATUS_ROOT" = "$CANON_ROOT" ] && echo "STATUS_MATCHES_CANONICAL=YES" || echo "CLASSIFICATION=ROOT_SURFACE_DRIFT"

echo
echo "=== PREFLIGHT ==="
./scripts/preflight_repo_audit.sh || true

echo
echo "AUDIT_REPORT=$OUT"
} | tee "$OUT"
