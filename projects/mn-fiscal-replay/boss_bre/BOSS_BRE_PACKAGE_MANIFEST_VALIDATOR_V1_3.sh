#!/usr/bin/env bash
# Boss Bre Package Manifest Validator v1.3
# Validates the populated machine-readable review package manifest.
# Doctrine: NO_FAKE_GREEN. Missing files or hash mismatches produce FAIL/BLOCKED receipts.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
MANIFEST="$ROOT/projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MACHINE_READABLE_PACKAGE_MANIFEST_V1_1_POPULATED.json"
RECEIPT="$ROOT/projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MANIFEST_VALIDATOR_V1_3_RECEIPT.json"
DETAILS="$ROOT/projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MANIFEST_VALIDATOR_V1_3_DETAILS.jsonl"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$(dirname "$RECEIPT")"
: > "$DETAILS"

sha_file() {
  sha256sum "$1" | awk '{print "sha256:" $1}'
}

write_receipt() {
  local status="$1"
  local reason="$2"
  local component_count="$3"
  local mismatch_count="$4"
  local missing_count="$5"
  local full_expected="$6"
  local full_actual="$7"
  jq -n \
    --arg utc "$UTC" \
    --arg status "$status" \
    --arg reason "$reason" \
    --arg manifest_path "${MANIFEST#$ROOT/}" \
    --arg details_path "${DETAILS#$ROOT/}" \
    --arg full_expected "$full_expected" \
    --arg full_actual "$full_actual" \
    --argjson component_count "$component_count" \
    --argjson mismatch_count "$mismatch_count" \
    --argjson missing_count "$missing_count" \
    '{artifact:"BOSS_BRE_MANIFEST_VALIDATOR_V1_3_RECEIPT",version:"1.3",generated_utc:$utc,status:$status,reason:$reason,manifest_path:$manifest_path,details_path:$details_path,component_count:$component_count,mismatch_count:$mismatch_count,missing_count:$missing_count,full_package_sha256_expected:$full_expected,full_package_sha256_actual:$full_actual,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_status:"PACKAGE_MANIFEST_VALIDATOR_ONLY",human_review_required:true,no_fake_green:true}' \
    > "$RECEIPT"
}

if [ ! -s "$MANIFEST" ]; then
  write_receipt "VALIDATE_BLOCKED" "POPULATED_MANIFEST_MISSING" 0 0 0 "" ""
  echo "VALIDATE_BLOCKED: POPULATED_MANIFEST_MISSING"
  exit 0
fi

component_count="$(jq '.components | length' "$MANIFEST")"
mismatch_count=0
missing_count=0

for i in $(seq 0 $((component_count - 1))); do
  component="$(jq -r ".components[$i].component" "$MANIFEST")"
  version="$(jq -r ".components[$i].version" "$MANIFEST")"
  path="$(jq -r ".components[$i].path" "$MANIFEST")"
  expected="$(jq -r ".components[$i].sha256" "$MANIFEST")"

  if [ ! -s "$ROOT/$path" ]; then
    missing_count=$((missing_count + 1))
    jq -nc \
      --arg component "$component" \
      --arg version "$version" \
      --arg path "$path" \
      --arg expected "$expected" \
      '{component:$component,version:$version,path:$path,status:"MISSING",expected_sha256:$expected,actual_sha256:""}' \
      >> "$DETAILS"
    continue
  fi

  actual="$(sha_file "$ROOT/$path")"
  if [ "$actual" = "$expected" ]; then
    status="PASS"
  else
    status="MISMATCH"
    mismatch_count=$((mismatch_count + 1))
  fi

  jq -nc \
    --arg component "$component" \
    --arg version "$version" \
    --arg path "$path" \
    --arg status "$status" \
    --arg expected "$expected" \
    --arg actual "$actual" \
    '{component:$component,version:$version,path:$path,status:$status,expected_sha256:$expected,actual_sha256:$actual}' \
    >> "$DETAILS"
done

component_hashes="$(jq -r '.components[] | [.component,.version,.path,.commit_ref,.sha256] | @tsv' "$MANIFEST")"
full_actual="sha256:$(printf '%s\n' "$component_hashes" | sha256sum | awk '{print $1}')"
full_expected="$(jq -r '.full_package_sha256 // ""' "$MANIFEST")"

reason="OK"
status="PASS"
if [ "$missing_count" -gt 0 ]; then
  status="FAIL"
  reason="COMPONENT_FILE_MISSING"
elif [ "$mismatch_count" -gt 0 ]; then
  status="FAIL"
  reason="COMPONENT_HASH_MISMATCH"
elif [ "$full_actual" != "$full_expected" ]; then
  status="FAIL"
  reason="FULL_PACKAGE_HASH_MISMATCH"
fi

write_receipt "$status" "$reason" "$component_count" "$mismatch_count" "$missing_count" "$full_expected" "$full_actual"

echo "VALIDATION_STATUS=$status"
echo "reason=$reason"
echo "component_count=$component_count"
echo "mismatch_count=$mismatch_count"
echo "missing_count=$missing_count"
echo "full_package_sha256_expected=$full_expected"
echo "full_package_sha256_actual=$full_actual"
echo "receipt=$RECEIPT"
echo "NO_FAKE_GREEN=ACTIVE"
