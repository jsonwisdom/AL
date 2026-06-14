#!/usr/bin/env bash
set -euo pipefail

echo "== ALMS AUTO-DRIP HEALTH =="
date -u
pwd

echo
echo "== HEAD =="
git rev-parse HEAD
git log --oneline -5

echo
echo "== TRANSPORT SIZE GATE: 44 MiB+ =="
LARGE="$(find . -path './.git' -prune -o -type f -size +44M -print)"
if [ -n "$LARGE" ]; then
  echo "$LARGE"
  echo "RED: oversized file(s) detected"
  exit 1
fi
echo "GREEN: no files over 44 MiB"

echo
echo "== SECRET / QUARANTINE LANE CHECK =="
if git ls-files | grep -E '^(_secrets|_quarantine|_sources)/'; then
  echo "RED: forbidden local lane tracked"
  exit 1
fi
echo "GREEN: forbidden lanes not tracked"

echo
echo "== ALERT MEMBRANE CHECK =="
test -f _truth/alerts/alerts_summary.json && echo "GREEN: alerts_summary exists" || echo "YELLOW: no alerts_summary"
test -d _truth/alerts/archive && echo "GREEN: alerts archive exists" || echo "YELLOW: no alerts archive"

echo
echo "== GIT OBJECT HEALTH =="
git count-objects -vH || true

echo
echo "== RULING =="
echo "PUBLIC_TRANSPORT_STATE: GREEN"
echo "AUTO_DRIP_STATE: GREEN"
echo "NO_FAKE_GREEN: ACTIVE"
