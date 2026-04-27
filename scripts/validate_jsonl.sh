#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-_truth}"

FAIL=0

while IFS= read -r f; do
  if ! jq -c . "$f" >/dev/null 2>&1; then
    echo "INVALID_JSONL $f"
    FAIL=1
  else
    echo "VALID_JSONL $f"
  fi
done < <(find "$TARGET" -type f -name "*.jsonl" | sort)

if [ "$FAIL" -ne 0 ]; then
  echo "JSONL_VALIDATION_FAILED"
  exit 1
fi

echo "JSONL_VALIDATION_OK"
