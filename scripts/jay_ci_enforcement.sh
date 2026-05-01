#!/usr/bin/env bash
# ALMS_CI_ENFORCEMENT_V1
# Standing guard: verify repo structure, safety scan, JSON validity, and required receipt lanes.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
REPORT="$ROOT/_truth/ci/jay_ci_enforcement_report.txt"

mkdir -p "$ROOT/_truth/ci"
cd "$ROOT"

{
  echo "ALMS_CI_ENFORCEMENT_V1"
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "root=$ROOT"
  echo "boundary=Receipts stay. Signing power leaves."
  echo
} > "$REPORT"

pass() {
  echo "PASS $1" | tee -a "$REPORT"
}

fail() {
  echo "FAIL $1" | tee -a "$REPORT"
  echo "ALMS_CI_ENFORCEMENT_FAIL report=$REPORT" | tee -a "$REPORT"
  exit 1
}

echo "→ Checking required directories..." | tee -a "$REPORT"
for d in scripts docs _truth .github .github/workflows; do
  [ -d "$d" ] && pass "dir_exists $d" || fail "missing_dir $d"
done

echo "→ Checking required files..." | tee -a "$REPORT"
for f in \
  "scripts/jay_repo_safety_scan.sh" \
  "docs/training/JASON_GITHUB_DIRECT_REPO_MANUAL.md" \
  ".github/workflows/jay-repo-safety.yml"; do
  [ -f "$f" ] && pass "file_exists $f" || fail "missing_file $f"
done

echo "→ Running Jay repo safety scan..." | tee -a "$REPORT"
bash scripts/jay_repo_safety_scan.sh . | tee -a "$REPORT"

if grep -q "JAY_REPO_SAFETY_OK" _truth/security/jay_repo_safety_report.txt; then
  pass "safety_scan_green"
else
  fail "safety_scan_not_green"
fi

echo "→ Validating JSON files..." | tee -a "$REPORT"
json_fail=0
while IFS= read -r -d '' f; do
  if ! jq empty "$f" >/dev/null 2>&1; then
    echo "INVALID_JSON $f" | tee -a "$REPORT"
    json_fail=1
  fi
done < <(find . -type f -name '*.json' \
  -not -path './.git/*' \
  -not -path './node_modules/*' \
  -not -path './dist/*' \
  -not -path './build/*' \
  -print0)

[ "$json_fail" -eq 0 ] && pass "json_validity" || fail "json_invalid"

echo "→ Verifying receipt lanes..." | tee -a "$REPORT"
[ -f "_truth/security/jay_repo_safety_report.txt" ] && pass "safety_report_exists" || fail "missing_safety_report"

echo "→ Checking workflow presence..." | tee -a "$REPORT"
[ -f ".github/workflows/jay-ci-enforcement.yml" ] && pass "ci_workflow_exists" || fail "missing_ci_workflow"

echo | tee -a "$REPORT"
echo "ALMS_CI_ENFORCEMENT_OK report=$REPORT" | tee -a "$REPORT"
echo "State: CI_GREEN | Receipts stay | Signing power leaves" | tee -a "$REPORT"
