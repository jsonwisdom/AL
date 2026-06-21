#!/bin/bash
# MN_002_CHUNK_DIFF_AND_CLASSIFY_V0_1.sh
# Doctrine: NO_FAKE_GREEN / chunk diff before public claim.

set -euo pipefail

ID="MN_002"
BASELINE_TEXT="_sources/$ID/source.txt"
LIVE_TEXT="projects/mn-fiscal-replay/live_fetch/$ID/${ID}_live_source.txt"
OUT_DIR="projects/mn-fiscal-replay/live_fetch/$ID/chunks"

mkdir -p "$OUT_DIR"

B_CHUNKS="$OUT_DIR/${ID}_baseline_chunks.txt"
L_CHUNKS="$OUT_DIR/${ID}_live_chunks.txt"
B_HASHES="$OUT_DIR/${ID}_baseline_chunk_hashes.txt"
L_HASHES="$OUT_DIR/${ID}_live_chunk_hashes.txt"
DIFF_FILE="$OUT_DIR/${ID}_chunked_sectional.diff"
VERDICT_JSON="$OUT_DIR/${ID}.chunked_verdict.json"

echo "=== $ID CHUNK DIFF AND CLASSIFY ==="

if [ ! -f "$BASELINE_TEXT" ]; then
  echo "BLOCKED_REASON: Missing baseline text: $BASELINE_TEXT"
  exit 1
fi

if [ ! -f "$LIVE_TEXT" ]; then
  echo "BLOCKED_REASON: Missing live text: $LIVE_TEXT"
  exit 1
fi

python3 - "$BASELINE_TEXT" "$B_CHUNKS" << 'PY'
import re, sys
from pathlib import Path

inp = Path(sys.argv[1])
out = Path(sys.argv[2])
text = inp.read_text(encoding="utf-8", errors="replace")
text = re.sub(r"\s+", " ", text).strip()
chunks = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"“])", text)

with out.open("w", encoding="utf-8") as f:
    for i, chunk in enumerate([c.strip() for c in chunks if c.strip()], start=1):
        f.write(f"{i:06d}\t{chunk}\n")
PY

python3 - "$LIVE_TEXT" "$L_CHUNKS" << 'PY'
import re, sys
from pathlib import Path

inp = Path(sys.argv[1])
out = Path(sys.argv[2])
text = inp.read_text(encoding="utf-8", errors="replace")
text = re.sub(r"\s+", " ", text).strip()
chunks = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"“])", text)

with out.open("w", encoding="utf-8") as f:
    for i, chunk in enumerate([c.strip() for c in chunks if c.strip()], start=1):
        f.write(f"{i:06d}\t{chunk}\n")
PY

python3 - "$B_CHUNKS" "$B_HASHES" << 'PY'
import hashlib, sys
from pathlib import Path

inp = Path(sys.argv[1])
out = Path(sys.argv[2])

with inp.open("r", encoding="utf-8", errors="replace") as src, out.open("w", encoding="utf-8") as dst:
    for line in src:
        line = line.rstrip("\n")
        if not line:
            continue
        chunk_id, chunk = line.split("\t", 1)
        h = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
        dst.write(f"{chunk_id}\t{h}\t{chunk}\n")
PY

python3 - "$L_CHUNKS" "$L_HASHES" << 'PY'
import hashlib, sys
from pathlib import Path

inp = Path(sys.argv[1])
out = Path(sys.argv[2])

with inp.open("r", encoding="utf-8", errors="replace") as src, out.open("w", encoding="utf-8") as dst:
    for line in src:
        line = line.rstrip("\n")
        if not line:
            continue
        chunk_id, chunk = line.split("\t", 1)
        h = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
        dst.write(f"{chunk_id}\t{h}\t{chunk}\n")
PY

set +e
diff -u "$B_HASHES" "$L_HASHES" > "$DIFF_FILE"
DIFF_EXIT=$?
set -e

if [ "$DIFF_EXIT" -eq 0 ]; then
  VERDICT="NO_CHUNK_DIFF"
  CLAIM_STATUS="BLOCKED_NOT_NEEDED"
  HUMAN_CLASSIFICATION="NO_CHUNK_DIFF"
  POSSIBLE_CONTENT_DELTA=false
elif [ "$DIFF_EXIT" -eq 1 ]; then
  VERDICT="CHUNK_DIFF_DETECTED"
  CLAIM_STATUS="BLOCKED_PENDING_HUMAN_CHUNK_REVIEW"
  HUMAN_CLASSIFICATION="PENDING_HUMAN_REVIEW"
  POSSIBLE_CONTENT_DELTA=null
else
  echo "BLOCKED_REASON: diff failed with exit code $DIFF_EXIT"
  exit 1
fi

BASE_CHUNKS=$(wc -l < "$B_CHUNKS" | tr -d ' ')
LIVE_CHUNKS=$(wc -l < "$L_CHUNKS" | tr -d ' ')
DIFF_LINES=$(wc -l < "$DIFF_FILE" | tr -d ' ')
ADDED_LINES=$(grep -E '^\+[^+]' "$DIFF_FILE" | wc -l | tr -d ' ')
REMOVED_LINES=$(grep -E '^\-[^-]' "$DIFF_FILE" | wc -l | tr -d ' ')
DIFF_HASH=$(sha256sum "$DIFF_FILE" | awk '{print $1}')
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

jq -n \
  --arg id "$ID" \
  --arg timestamp "$TS" \
  --arg verdict "$VERDICT" \
  --arg claim_status "$CLAIM_STATUS" \
  --arg classification "$HUMAN_CLASSIFICATION" \
  --arg base_chunks "$BASE_CHUNKS" \
  --arg live_chunks "$LIVE_CHUNKS" \
  --arg diff_lines "$DIFF_LINES" \
  --arg added_lines "$ADDED_LINES" \
  --arg removed_lines "$REMOVED_LINES" \
  --arg diff_hash "$DIFF_HASH" \
  --arg diff_file "$DIFF_FILE" \
  '{
    id: $id,
    timestamp: $timestamp,
    verdict: $verdict,
    claim_status: $claim_status,
    human_review_classification: $classification,
    baseline_chunk_count: $base_chunks,
    live_chunk_count: $live_chunks,
    diff_line_count: $diff_lines,
    added_diff_lines: $added_lines,
    removed_diff_lines: $removed_lines,
    chunked_diff_sha256: $diff_hash,
    chunked_diff_file: $diff_file,
    public_content_claim: "BLOCKED",
    next_step: "HUMAN_CHUNK_REVIEW_OR_FINAL_SAFE_STATUS",
    no_fake_green: true
  }' > "$VERDICT_JSON"

cat "$VERDICT_JSON" | jq .

echo ""
echo "=== FIRST 120 DIFF LINES ==="
sed -n '1,120p' "$DIFF_FILE"
