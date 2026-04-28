#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
OUT_DIR="_truth/merkle"
LEAVES="$OUT_DIR/leaves.jsonl"
MANIFEST="$OUT_DIR/manifest.json"
ROOT_FILE="$OUT_DIR/root.txt"

mkdir -p "$OUT_DIR"

: > "$LEAVES"

find _truth/receipts receipts -type f -name '*.json' 2>/dev/null | LC_ALL=C sort | while read -r f; do
  canon="$(jq -cS . "$f")"
  hash="$(printf '%s' "$canon" | sha256sum | awk '{print $1}')"
  jq -cn --arg path "$f" --arg hash "$hash" '{path:$path,hash:$hash}' >> "$LEAVES"
done

COUNT="$(wc -l < "$LEAVES" | tr -d ' ')"

test "$COUNT" -gt 0 || { echo "NO_LEAVES"; exit 1; }

CURRENT="$(mktemp)"
NEXT="$(mktemp)"

jq -r '.hash' "$LEAVES" | LC_ALL=C sort > "$CURRENT"

while [ "$(wc -l < "$CURRENT" | tr -d ' ')" -gt 1 ]; do
  : > "$NEXT"

  while read -r left; do
    read -r right || right="$left"
    printf '%s%s' "$left" "$right" | sha256sum | awk '{print $1}' >> "$NEXT"
  done < "$CURRENT"

  mv "$NEXT" "$CURRENT"
  NEXT="$(mktemp)"
done

ROOT="$(cat "$CURRENT")"

printf '%s\n' "$ROOT" > "$ROOT_FILE"

jq -cn \
  --arg generated_at "$TS" \
  --arg root "sha256:$ROOT" \
  --arg leaves "$COUNT" \
  --arg identity "jaywisdom.base.eth" \
  --slurpfile leaf_list "$LEAVES" \
  '{
    type:"ALMS_MERKLE_ROOT_V1",
    identity:$identity,
    generated_at:$generated_at,
    leaf_count:($leaves|tonumber),
    root:$root,
    leaves:$leaf_list
  }' > "$MANIFEST"

echo "MERKLE_ROOT_OK root=sha256:$ROOT leaves=$COUNT manifest=$MANIFEST"
