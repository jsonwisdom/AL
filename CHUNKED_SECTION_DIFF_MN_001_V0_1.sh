#!/bin/bash
# CHUNKED_SECTION_DIFF_MN_001_V0_1.sh
# Sentence-like chunk diff for MN_001. NO_FAKE_GREEN.

set -euo pipefail

BASELINE_TEXT="_sources/MN_001/source.txt"
LIVE_TEXT="projects/mn-fiscal-replay/live_fetch/MN_001/MN_001_live_source.txt"
CHUNK_DIR="projects/mn-fiscal-replay/live_fetch/MN_001/chunks"

mkdir -p "$CHUNK_DIR"

B_CHUNKS="$CHUNK_DIR/MN_001_baseline_chunks.txt"
L_CHUNKS="$CHUNK_DIR/MN_001_live_chunks.txt"
B_HASHES="$CHUNK_DIR/MN_001_baseline_chunk_hashes.txt"
L_HASHES="$CHUNK_DIR/MN_001_live_chunk_hashes.txt"
DIFF_FILE="$CHUNK_DIR/MN_001_chunked_sectional.diff"
VERDICT_JSON="$CHUNK_DIR/MN_001.chunked_verdict.json"

echo "=== CHUNKED_SECTION_DIFF_MN_001_V0_1 ==="

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
elif [ "$DIFF_EXIT" -eq 1 ]; then
  VERDICT="CHUNK_DIFF_DETECTED"
  CLAIM_STATUS="BLOCKED_PENDING_HUMAN_CHUNK_REVIEW"
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

python3 - "$VERDICT_JSON" "$DIFF_FILE" "$VERDICT" "$CLAIM_STATUS" "$BASE_CHUNKS" "$LIVE_CHUNKS" "$DIFF_LINES" "$ADDED_LINES" "$REMOVED_LINES" "$DIFF_HASH" "$TS" << 'PY'
import json, sys
from pathlib import Path

out = Path(sys.argv[1])
diff_file = Path(sys.argv[2])
preview = diff_file.read_text(encoding="utf-8", errors="replace").splitlines()[:120]

receipt = {
  "id": "MN_001",
  "verdict": sys.argv[3],
  "claim_status": sys.argv[4],
  "baseline_chunk_count": sys.argv[5],
  "live_chunk_count": sys.argv[6],
  "diff_line_count": sys.argv[7],
  "added_diff_lines": sys.argv[8],
  "removed_diff_lines": sys.argv[9],
  "chunked_diff_sha256": sys.argv[10],
  "chunked_diff_file": str(diff_file),
  "diff_preview_max_lines": 120,
  "diff_preview": preview,
  "classification": "CHUNKED_SECTIONAL_REVIEW",
  "public_content_change_claim": "BLOCKED_UNTIL_HUMAN_CHUNK_REVIEW",
  "timestamp": sys.argv[11],
  "no_fake_green": True
}

out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
PY

cat "$VERDICT_JSON" | jq .

echo ""
echo "=== FIRST 160 DIFF LINES ==="
sed -n '1,160p' "$DIFF_FILE"
