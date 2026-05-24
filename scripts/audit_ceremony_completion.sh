#!/usr/bin/env bash
set -euo pipefail

FAILED=0

declare -A ARTIFACTS=(
  ["_truth/governance/HEARTBEAT_COURT_COMPLETION_SUMMARY_001.json"]="666d5b0b597d5c5df24ac950be91fb16b48a2442"
  ["_truth/governance/CEREMONY_COURT_RULES_V1.json"]="bf427c8ded33e3457883217df4edb1735f015c6a"
  ["_truth/governance/CEREMONY_OPENING_RECEIPT_001.json"]="8c7fe1ba9ed4899c49730e27eb1cb3323828ad83"
  ["_truth/governance/STATE_CHANGE_CERTIFICATE.json"]="62691e2fd3e6a1efa8d8d3bef6e0654952d33ccb"
  ["_truth/governance/CEREMONY_COMPLETION_CRITERIA_V1.json"]="47af030fdca77c9a5cb5095220c602af5100fbab"
)

echo "Ceremony Court Audit — Starting"
echo "================================="

for file in "${!ARTIFACTS[@]}"; do
  expected="${ARTIFACTS[$file]}"

  if [ ! -f "$file" ]; then
    echo "FAIL missing artifact: $file"
    FAILED=1
    continue
  fi

  actual="$(git log -1 --format="%H" -- "$file")"
  if [ "$actual" != "$expected" ]; then
    echo "FAIL commit mismatch: $file"
    echo "expected=$expected"
    echo "actual=$actual"
    FAILED=1
  else
    echo "PASS artifact commit verified: $file"
  fi
done

echo ""
echo "Checking manual_override fields"
for file in "${!ARTIFACTS[@]}"; do
  if grep -q '"manual_override"[[:space:]]*:[[:space:]]*true' "$file" 2>/dev/null; then
    echo "FAIL manual_override=true: $file"
    FAILED=1
  else
    echo "PASS manual_override not true: $file"
  fi
done

echo ""
echo "Checking machine_authority fields"
for file in "${!ARTIFACTS[@]}"; do
  if grep -q '"machine_authority"[[:space:]]*:[[:space:]]*false' "$file" 2>/dev/null; then
    echo "FAIL machine_authority=false: $file"
    FAILED=1
  else
    echo "PASS machine_authority not false: $file"
  fi
done

echo ""
echo "================================="
if [ "$FAILED" -eq 0 ]; then
  echo "AUDIT_STATUS=PASS"
  echo "eligible_for_completion_receipt=true"
  exit 0
else
  echo "AUDIT_STATUS=FAIL"
  echo "eligible_for_completion_receipt=false"
  exit 1
fi
