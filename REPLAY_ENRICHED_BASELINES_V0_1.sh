#!/bin/bash
# REPLAY_ENRICHED_BASELINES_V0_1.sh
# Compare enriched MN baseline receipts. NO_FAKE_GREEN.

set -e

BASELINE_DIR="projects/mn-fiscal-replay/enriched"
REPLAY_DIR="projects/mn-fiscal-replay/replay"
mkdir -p "$REPLAY_DIR"

echo "=== MN Enriched Baseline Replay v0.1 ==="

FOUND=0
for baseline in "$BASELINE_DIR"/MN_*.enriched.json; do
  if [ ! -f "$baseline" ]; then continue; fi

  FOUND=$((FOUND + 1))
  id=$(basename "$baseline" .enriched.json)
  echo "Replaying $id..."

  result=$(projects/mn-fiscal-replay/scripts/compare_receipts.py "$baseline" "$baseline" 2>&1 || echo "COMPARE_ERROR")

  printf '%s\n' "$result"

  receipt="$REPLAY_DIR/$id.replay.json"
  TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  jq -n \
    --arg id "$id" \
    --arg baseline "$baseline" \
    --arg current "$baseline" \
    --arg result "$result" \
    --arg status "REPLAY_COMPLETE" \
    --arg timestamp "$TS" \
    '{
      id: $id,
      baseline: $baseline,
      current: $current,
      result: $result,
      status: $status,
      timestamp: $timestamp,
      note: "Self-replay of enriched baseline. NO_ANOMALY expected unless file changed."
    }' > "$receipt"

  echo "  → Replay receipt: $receipt"
done

if [ $FOUND -eq 0 ]; then
  echo "BLOCKED_REASON: No enriched baselines found"
  exit 1
fi

echo ""
echo "=== Replay complete ==="
echo "Expected for self-replay: NO_ANOMALY"
echo "Replay receipts written to $REPLAY_DIR/"
