#!/bin/bash
# BUILD_LIBRARIAN_INDEX_V0_3.sh
# Purpose: derive maintenance index from sealed v0.2 index + final safe status receipts.
# Doctrine: NO_FAKE_GREEN / no hand-entered source URLs.

set -euo pipefail

IN="projects/mn-fiscal-replay/librarian/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_2.json"
OUT="projects/mn-fiscal-replay/librarian/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_3.json"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

if [ ! -f "$IN" ]; then
  echo "BLOCKED_REASON: Missing v0.2 index: $IN"
  exit 1
fi

for id in MN_001 MN_002; do
  final="projects/mn-fiscal-replay/live_fetch/$id/${id}_FINAL_SAFE_STATUS_V0_1.json"
  if [ ! -f "$final" ]; then
    echo "BLOCKED_REASON: Missing final safe status for $id: $final"
    exit 1
  fi

  verdict=$(jq -r '.verdict // empty' "$final")
  delta=$(jq -r '.possible_content_delta' "$final")
  claim=$(jq -r '.public_content_claim // empty' "$final")

  if [ "$verdict" != "PUBLIC_CONTENT_ANOMALY_UNPROVEN" ]; then
    echo "BLOCKED_REASON: $id final verdict is not safe baseline verdict"
    echo "VERDICT=$verdict"
    exit 1
  fi

  if [ "$delta" != "false" ]; then
    echo "BLOCKED_REASON: $id possible_content_delta is not false"
    echo "possible_content_delta=$delta"
    exit 1
  fi

  if [ "$claim" != "BLOCKED" ]; then
    echo "BLOCKED_REASON: $id public_content_claim is not BLOCKED"
    echo "public_content_claim=$claim"
    exit 1
  fi
done

jq -n \
  --arg ts "$TS" \
  --argjson v2 "$(cat "$IN")" \
  --argjson mn1 "$(cat projects/mn-fiscal-replay/live_fetch/MN_001/MN_001_FINAL_SAFE_STATUS_V0_1.json)" \
  --argjson mn2 "$(cat projects/mn-fiscal-replay/live_fetch/MN_002/MN_002_FINAL_SAFE_STATUS_V0_1.json)" \
  '{
    version: "v0_3",
    last_updated: $ts,
    artifact: "MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_3",
    rule: "DISCOVERY_BEFORE_DELEGATION",
    manifest: [
      {
        id: "MN_001",
        status: "MAINTENANCE_SAFE_BASELINE",
        public_content_claim: $mn1.public_content_claim,
        source_url: $v2.components.MN_001.source_url,
        source_manifest: $v2.components.MN_001.source_manifest,
        final_safe_status: $v2.components.MN_001.final_safe_status,
        verdict: $mn1.verdict,
        possible_content_delta: $mn1.possible_content_delta,
        provenance: "SEALED_V0_1"
      },
      {
        id: "MN_002",
        status: "MAINTENANCE_SAFE_BASELINE",
        public_content_claim: $mn2.public_content_claim,
        source_url: $v2.components.MN_002.source_url,
        source_manifest: $v2.components.MN_002.source_manifest,
        final_safe_status: "projects/mn-fiscal-replay/live_fetch/MN_002/MN_002_FINAL_SAFE_STATUS_V0_1.json",
        verdict: $mn2.verdict,
        possible_content_delta: $mn2.possible_content_delta,
        provenance: "SEALED_V0_1"
      }
    ],
    counts: {
      maintenance_safe_baselines: 2,
      public_claims_blocked: 2,
      manual_operator_file_search_required: false
    },
    next_best_target: "BOSS_BRE_V1_6_CLEANUP_OR_DISCOVER_NEXT_MANIFEST",
    global_policy: "NO_FAKE_GREEN_ACTIVE",
    instruction: "Click-paths must point to status definitions and receipts, not raw data dumps.",
    no_fake_green: true
  }' > "$OUT"

cat "$OUT" | jq .

git add \
  projects/mn-fiscal-replay/librarian/BUILD_LIBRARIAN_INDEX_V0_3.sh \
  "$OUT"

git commit -m "Build Librarian Index v0.3 from sealed safe status receipts"
git push origin master
