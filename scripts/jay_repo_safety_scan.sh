#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
REPORT_DIR="$ROOT/_truth/security"
REPORT="$REPORT_DIR/jay_repo_safety_report.txt"

mkdir -p "$REPORT_DIR"

{
  echo "JAY_REPO_SAFETY_SCAN"
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "root=$ROOT"
  echo
  echo "BOUNDARY: receipts stay; signing power leaves"
} > "$REPORT"

fail=0

scan_fail() {
  local name="$1"
  local pattern="$2"

  echo "" | tee -a "$REPORT"
  echo "## $name" | tee -a "$REPORT"

  if grep -RInE \
    --exclude-dir=.git \
    --exclude-dir=node_modules \
    --exclude-dir=.next \
    --exclude-dir=dist \
    --exclude-dir=build \
    --exclude='jay_repo_safety_report.txt' \
    "$pattern" "$ROOT" >> "$REPORT" 2>/dev/null; then
    echo "STATUS=FAIL" | tee -a "$REPORT"
    fail=1
  else
    echo "STATUS=PASS" | tee -a "$REPORT"
  fi
}

scan_report() {
  local name="$1"
  local pattern="$2"

  echo "" | tee -a "$REPORT"
  echo "## $name" | tee -a "$REPORT"

  if grep -RInE \
    --exclude-dir=.git \
    --exclude-dir=node_modules \
    --exclude-dir=.next \
    --exclude-dir=dist \
    --exclude-dir=build \
    --exclude='jay_repo_safety_report.txt' \
    "$pattern" "$ROOT" >> "$REPORT" 2>/dev/null; then
    echo "STATUS=FOUND_PUBLIC_ARTIFACTS" | tee -a "$REPORT"
  else
    echo "STATUS=NONE_FOUND" | tee -a "$REPORT"
  fi
}

scan_fail "PRIVATE_KEY_PATTERNS" 'PRIVATE_KEY=|private_key|BEGIN (RSA |EC |OPENSSH |)?PRIVATE KEY|wallet\.json|keystore|UTC--'
scan_fail "SEED_OR_MNEMONIC_PATTERNS" 'MNEMONIC=|SEED_PHRASE=|seed phrase|recovery phrase'
scan_fail "API_TOKEN_PATTERNS" 'ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]+'
scan_fail "ENV_FILE_LEAKS" '(^|/)\.env($|\.| )|\.env\.local|\.env\.production'
scan_fail "GOOGLE_SERVICE_ACCOUNT_JSON" '"type"[[:space:]]*:[[:space:]]*"service_account"|"private_key_id"|"client_email"'
scan_fail "RPC_URL_WITH_TOKEN" 'https://[^ ]*(alchemy|infura|quicknode|ankr|getblock)[^ ]*(key|token|secret|api)'

scan_report "PUBLIC_0X_40_ADDRESS_LIKE" '0x[a-fA-F0-9]{40}'
scan_report "PUBLIC_0X_64_HASH_LIKE" '0x[a-fA-F0-9]{64}'

echo "" | tee -a "$REPORT"
echo "## FINAL" | tee -a "$REPORT"

if [ "$fail" -eq 0 ]; then
  echo "JAY_REPO_SAFETY_OK report=$REPORT" | tee -a "$REPORT"
  exit 0
else
  echo "JAY_REPO_SAFETY_FAIL report=$REPORT" | tee -a "$REPORT"
  exit 1
fi
