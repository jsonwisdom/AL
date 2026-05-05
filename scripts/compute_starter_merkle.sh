#!/usr/bin/env bash
set -euo pipefail

# Compute a simple deterministic Merkle root over a directory of files
# Rule: ALMS_STARTER_MERKLE_V1

DIR="${1:-_truth/write_runs/fixtures}"
OUT_DIR="_truth/merkle"
mkdir -p "$OUT_DIR"

LEAVES_JSONL="$OUT_DIR/starter_leaves.jsonl"
MANIFEST="$OUT_DIR/starter_manifest.json"
ROOT_FILE="$OUT_DIR/starter_root.txt"

# 1. sort file paths
mapfile -t FILES < <(find "$DIR" -type f | sort)

# 2. hash each file
: > "$LEAVES_JSONL"
for f in "${FILES[@]}"; do
  H=$(sha256sum "$f" | awk '{print $1}')
  printf '{"path":"%s","sha256":"%s"}\n' "$f" "$H" >> "$LEAVES_JSONL"
done

# build list of hashes
mapfile -t HASHES < <(jq -r '.sha256' "$LEAVES_JSONL")

if [ "${#HASHES[@]}" -eq 0 ]; then
  echo "No files to hash" >&2
  exit 1
fi

# 4-6. compute root
while [ "${#HASHES[@]}" -gt 1 ]; do
  NEW=()
  for ((i=0; i<${#HASHES[@]}; i+=2)); do
    if [ $((i+1)) -lt ${#HASHES[@]} ]; then
      COMBINED="${HASHES[$i]}${HASHES[$((i+1))]}"
      H=$(printf '%s' "$COMBINED" | sha256sum | awk '{print $1}')
      NEW+=("$H")
    else
      NEW+=("${HASHES[$i]}")
    fi
  done
  HASHES=("${NEW[@]}")
done

ROOT="${HASHES[0]}"
echo "$ROOT" > "$ROOT_FILE"

# 7. write manifest
cat > "$MANIFEST" <<JSON
{
  "rule_id": "ALMS_STARTER_MERKLE_V1",
  "leaf_count": ${#FILES[@]},
  "leaves_file": "$(basename "$LEAVES_JSONL")",
  "root": "$ROOT"
}
JSON

echo "MERKLE_OK"
echo "ROOT=$ROOT"
echo "MANIFEST=$MANIFEST"
