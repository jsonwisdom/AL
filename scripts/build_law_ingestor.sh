#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%FT%TZ)"
ROOT="_truth/law"
SRC="law/ingest/law_sources.json"
OUT="$ROOT/law_ingestor_feed.json"
LOG="_truth/logs/law_ingestor.log"

mkdir -p "$ROOT" _truth/logs

if [ ! -f "$SRC" ]; then
  echo "$TS ERROR missing $SRC" | tee -a "$LOG"
  exit 1
fi

CANON="$ROOT/sources.canonical.json"
jq -cS . "$SRC" > "$CANON"

HASH="$(sha256sum "$CANON" | awk '{print $1}')"

jq -n \
  --arg ts "$TS" \
  --arg hash "$HASH" \
  --slurpfile sources "$CANON" \
  '{
    observer: "law_ingestor_v1",
    generated_at: $ts,
    rule: "ingest_normalize_hash_verify_surface",
    source_manifest_hash: $hash,
    sources: $sources[0].sources,
    lanes: {
      lawbooks: {
        status: "GREEN",
        reason: "static source manifest normalized"
      },
      cases: {
        status: "YELLOW",
        reason: "public API seed registered; no docket-specific watch active yet"
      },
      doj: {
        status: "YELLOW",
        reason: "DOJ source registered; no claim-specific receipt bound yet"
      }
    },
    requirements: [
      "source",
      "timestamp",
      "type",
      "lane",
      "hash"
    ],
    global: {
      visibility: "YELLOW",
      reason: "source manifest exists; live ingestion adapters not yet attached"
    }
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS LAW_INGESTOR_BUILT hash=$HASH" | tee -a "$LOG"
