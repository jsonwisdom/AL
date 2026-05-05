#!/usr/bin/env bash
set -euo pipefail

# WRITE_RUN_0004 / DIFF_ENGINE_V1
# Scope: manifest-pair only. No content fetch. No promotion. No gate movement.
# Usage: scripts/diff_manifests_v1.sh old_manifest.json new_manifest.json <out_dir>

OLD="${1:-}"
NEW="${2:-}"
OUT_DIR="${3:-_truth/diff_engine/$(date -u +%Y-%m-%dT%H-%M-%SZ)}"

if [ -z "$OLD" ] || [ -z "$NEW" ]; then
  echo "Usage: $0 old_manifest.json new_manifest.json <out_dir>"
  exit 1
fi

if [ ! -f "$OLD" ] || [ ! -f "$NEW" ]; then
  echo "MANIFEST_NOT_FOUND"
  exit 1
fi

mkdir -p "$OUT_DIR"

OLD_SHA=$(sha256sum "$OLD" | awk '{print $1}')
NEW_SHA=$(sha256sum "$NEW" | awk '{print $1}')
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Normalize supported file arrays. Prefer .id, fallback .path, then .file_id.
jq -r '.files[]? | [(.id // .file_id // .path), .sha256, (.path // .id // .file_id)] | @tsv' "$OLD" | sort > "$OUT_DIR/old.tsv"
jq -r '.files[]? | [(.id // .file_id // .path), .sha256, (.path // .id // .file_id)] | @tsv' "$NEW" | sort > "$OUT_DIR/new.tsv"

cut -f1 "$OUT_DIR/old.tsv" | sort > "$OUT_DIR/old.ids"
cut -f1 "$OUT_DIR/new.tsv" | sort > "$OUT_DIR/new.ids"

comm -13 "$OUT_DIR/old.ids" "$OUT_DIR/new.ids" > "$OUT_DIR/added.ids"
comm -23 "$OUT_DIR/old.ids" "$OUT_DIR/new.ids" > "$OUT_DIR/removed.ids"
comm -12 "$OUT_DIR/old.ids" "$OUT_DIR/new.ids" > "$OUT_DIR/common.ids"

: > "$OUT_DIR/changed.tsv"
while IFS= read -r id; do
  old_sha=$(awk -F '\t' -v id="$id" '$1==id {print $2; exit}' "$OUT_DIR/old.tsv")
  new_sha=$(awk -F '\t' -v id="$id" '$1==id {print $2; exit}' "$OUT_DIR/new.tsv")
  if [ "$old_sha" != "$new_sha" ]; then
    printf '%s\t%s\t%s\n' "$id" "$old_sha" "$new_sha" >> "$OUT_DIR/changed.tsv"
  fi
done < "$OUT_DIR/common.ids"

ADDED_COUNT=$(wc -l < "$OUT_DIR/added.ids" | tr -d ' ')
REMOVED_COUNT=$(wc -l < "$OUT_DIR/removed.ids" | tr -d ' ')
CHANGED_COUNT=$(wc -l < "$OUT_DIR/changed.tsv" | tr -d ' ')

jq -n \
  --arg artifact "DIFF_REPORT_V1" \
  --arg ts "$TS" \
  --arg old_manifest "$OLD" \
  --arg new_manifest "$NEW" \
  --arg old_manifest_sha256 "$OLD_SHA" \
  --arg new_manifest_sha256 "$NEW_SHA" \
  --argjson added_count "$ADDED_COUNT" \
  --argjson removed_count "$REMOVED_COUNT" \
  --argjson changed_count "$CHANGED_COUNT" \
  --slurpfile added <(jq -Rn '[inputs | select(length>0)]' < "$OUT_DIR/added.ids") \
  --slurpfile removed <(jq -Rn '[inputs | select(length>0)]' < "$OUT_DIR/removed.ids") \
  --slurpfile changed <(awk -F '\t' '{print "{\"id\":\""$1"\",\"old_sha256\":\""$2"\",\"new_sha256\":\""$3"\"}"}' "$OUT_DIR/changed.tsv" | jq -s '.') \
'{
  artifact: $artifact,
  timestamp_utc: $ts,
  old_manifest: $old_manifest,
  new_manifest: $new_manifest,
  old_manifest_sha256: $old_manifest_sha256,
  new_manifest_sha256: $new_manifest_sha256,
  added_count: $added_count,
  removed_count: $removed_count,
  changed_count: $changed_count,
  added: $added[0],
  removed: $removed[0],
  changed: $changed[0],
  claim_scope: "SNAPSHOT_DIFF_ONLY",
  promotion: false,
  write_run_0004: "UNCHANGED",
  gate_status: "CLOSED"
}' > "$OUT_DIR/diff_report.json"

sha256sum "$OUT_DIR/diff_report.json" | awk '{print $1}' > "$OUT_DIR/diff_report.sha256"

cat "$OUT_DIR/diff_report.json"
echo "DIFF_REPORT_SHA256=$(cat "$OUT_DIR/diff_report.sha256")"
