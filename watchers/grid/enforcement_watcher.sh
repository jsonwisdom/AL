#!/usr/bin/env bash
set -euo pipefail

URL='https://www.whitehouse.gov/presidential-actions/2026/04/presidential-determination-pursuant-to-section-303-of-the-defense-production-act-of-1950-as-amended-on-grid-infrastructure-equipment-and-supply-chain-capacity/'
OUT="_truth/grid_enforcement_$(date -u +%Y%m%dT%H%M%SZ).json"

mkdir -p _truth

TEXT="$(curl -Ls "$URL" | tr '\n' ' ' | sed 's/<[^>]*>/ /g' | tr -s ' ')"

jq -n \
  --arg url "$URL" \
  --arg ts "$(date -u +%FT%TZ)" \
  --arg uptime "$(printf "%s" "$TEXT" | grep -Eio 'uptime|availability' | head -1 || true)" \
  --arg mttr "$(printf "%s" "$TEXT" | grep -Eio 'MTTR|mean time to repair|mean time to recovery' | head -1 || true)" \
  --arg outages "$(printf "%s" "$TEXT" | grep -Eio 'outage counts|outages|interruption' | head -1 || true)" \
  --arg spend "$(printf "%s" "$TEXT" | grep -Eio 'spending|spend|appropriation|funding|dollars|\\$[0-9]' | head -1 || true)" \
  --arg milestones "$(printf "%s" "$TEXT" | grep -Eio 'milestone|deadline|target date|timeline' | head -1 || true)" \
  '{
    watcher: "grid_enforcement",
    source_url: $url,
    checked_at: $ts,
    metrics_detected: {
      uptime: ($uptime != ""),
      mttr: ($mttr != ""),
      outage_counts: ($outages != ""),
      spending: ($spend != ""),
      milestones: ($milestones != "")
    },
    raw_hits: {
      uptime: $uptime,
      mttr: $mttr,
      outage_counts: $outages,
      spending: $spend,
      milestones: $milestones
    }
  }' > "$OUT"

cat "$OUT"
