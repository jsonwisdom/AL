#!/usr/bin/env bash
# Handoff script: AL -> COMPUTERWISDOM
# Copies latest DOJ data.json diff report into COMPUTERWISDOM incoming registry

set -euo pipefail

AL_REPO_PATH="$(pwd)"
CW_REPO_PATH="${CW_REPO_PATH:-../COMPUTERWISDOM}"
SOURCE_DIR="$AL_REPO_PATH/_truth/doj_data_json/diff_reports"
TARGET_DIR="$CW_REPO_PATH/_truth/doj_data_json/incoming"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

LATEST_REPORT="$(find "$SOURCE_DIR" -maxdepth 1 -type f -name 'diff_report_*.json' 2>/dev/null | sort | tail -n 1 || true)"

if [[ -z "$LATEST_REPORT" ]]; then
  echo "[ERROR] No diff report found to transmit in $SOURCE_DIR"
  echo "[HINT] Run scripts/analyze_doj_diff.sh first"
  exit 1
fi

if [[ ! -d "$CW_REPO_PATH" ]]; then
  echo "[ERROR] COMPUTERWISDOM repo path not found: $CW_REPO_PATH"
  echo "[HINT] Set CW_REPO_PATH=/path/to/COMPUTERWISDOM"
  exit 1
fi

jq empty "$LATEST_REPORT"
mkdir -p "$TARGET_DIR"

REPORT_BASENAME="$(basename "$LATEST_REPORT")"
TARGET_FILE="$TARGET_DIR/$REPORT_BASENAME"
cp "$LATEST_REPORT" "$TARGET_FILE"

SOURCE_HASH="$(sha256sum "$LATEST_REPORT" | awk '{print $1}')"
TARGET_HASH="$(sha256sum "$TARGET_FILE" | awk '{print $1}')"

if [[ "$SOURCE_HASH" != "$TARGET_HASH" ]]; then
  echo "[ERROR] Handoff hash mismatch"
  echo "SOURCE_HASH=$SOURCE_HASH"
  echo "TARGET_HASH=$TARGET_HASH"
  exit 1
fi

cat > "$TARGET_DIR/HANDOFF_${REPORT_BASENAME%.json}.manifest.json" <<EOF
{
  "handoff_at": "$TIMESTAMP",
  "source_repo": "jsonwisdom/AL",
  "target_repo": "jsonwisdom/COMPUTERWISDOM",
  "source_file": "$LATEST_REPORT",
  "target_file": "$TARGET_FILE",
  "hash_sha256": "$SOURCE_HASH",
  "authority": false,
  "verification_state": "HANDOFF_NOT_INTERPRETED"
}
EOF

echo "[SUCCESS] Report transmitted to COMPUTERWISDOM for analysis"
echo "SOURCE=$LATEST_REPORT"
echo "TARGET=$TARGET_FILE"
echo "HASH_SHA256=$SOURCE_HASH"
echo "AUTHORITY=false"
