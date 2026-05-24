#!/usr/bin/env bash
set -euo pipefail

GENESIS="fab0e39388aa37c971ab4d172f189173e19b1d9b"
COUNT=0

# Count frozen GREEN heartbeat receipts at or after the constitutional epoch boundary.
# Pre-fab0e393 construction history is not constitutional history.
while IFS= read -r receipt; do
  [ -n "$receipt" ] || continue

  commit="$(git log -1 --format="%H" -- "$receipt")"

  if ! git merge-base --is-ancestor "$GENESIS" "$commit" 2>/dev/null; then
    continue
  fi

  if git show "$commit:$receipt" 2>/dev/null | grep -q '"status"[[:space:]]*:[[:space:]]*"GREEN"'; then
    COUNT=$((COUNT + 1))
  fi
done < <(git ls-tree --name-only -r HEAD _truth/governance/ | grep 'HEARTBEAT_COURT_GREEN_RECEIPT_.*\.json$' | sort)

echo "$COUNT"
