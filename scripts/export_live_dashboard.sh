#!/usr/bin/env bash
set -euo pipefail

OUT="site/live.json"
MERKLE="_truth/merkle/manifest.json"
ROOT="$(cat _truth/merkle/root.txt 2>/dev/null || echo "NO_ROOT")"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -cn \
  --arg root "$ROOT" \
  --arg ts "$TS" \
  --slurpfile m "$MERKLE" \
'{
  status:"LIVE",
  identity:"jaywisdom.base.eth",
  updated_at:$ts,
  merkle_root:$root,
  leaf_count:($m[0].leaf_count // 0),
  manifest:"/ _truth/merkle/manifest.json",
  verification_path:"ENS → ROOT → MANIFEST → LEAF",
  slogan:"Proof > Narrative"
}' > "$OUT"

echo "LIVE_EXPORT_OK $OUT"
