#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%FT%TZ)"
OUT="_truth/base/unified_mesh_feed.json"
SITE_OUT="site/unified-mesh.json"

mkdir -p _truth/base site

NITRO_FILE="_truth/base/nitro_observer_feed.json"
SYSTEMCONFIG_FILE="_truth/base/systemconfig_observer_feed.json"
PORTAL_FILE="_truth/base/optimismportal_observer_feed.json"
BRIDGE_FILE="_truth/base/l1standardbridge_observer_feed.json"

jq -n \
  --arg ts "$TS" \
  --slurpfile nitro "$NITRO_FILE" \
  --slurpfile systemconfig "$SYSTEMCONFIG_FILE" \
  --slurpfile portal "$PORTAL_FILE" \
  --slurpfile bridge "$BRIDGE_FILE" \
  '
  def raw_status($x):
    if $x == null then "UNKNOWN"
    elif (($x.status | type) == "object") then ($x.status.visibility // "UNKNOWN")
    elif (($x.status | type) == "string") then $x.status
    else "UNKNOWN"
    end;

  def norm($s):
    if ($s == "GREEN" or $s == "L1_TARGET_CONFIRMED") then "GREEN"
    elif ($s == "RED") then "RED"
    else "YELLOW"
    end;

  ($nitro[0] // null) as $n |
  ($systemconfig[0] // null) as $s |
  ($portal[0] // null) as $p |
  ($bridge[0] // null) as $b |
  (norm(raw_status($s))) as $systemconfig_status |
  (norm(raw_status($p))) as $portal_status |
  (norm(raw_status($b))) as $bridge_status |
  (norm(raw_status($n))) as $nitro_status |
  ([$systemconfig_status, $portal_status, $bridge_status, $nitro_status]) as $v |
  {
    generated_at: $ts,
    observer: "base_unified_mesh",
    spine: {
      l1_systemconfig: $systemconfig_status,
      l1_optimismportal: $portal_status,
      l1_standardbridge: $bridge_status,
      l2_nitro_verifier: $nitro_status
    },
    global: (
      if ($v | index("RED")) then
        {visibility:"RED", reason:"one_or_more_layers_red", status_color:"🔴"}
      elif ($v | index("YELLOW")) then
        {visibility:"YELLOW", reason:"degraded_or_missing_visibility", status_color:"🟡"}
      else
        {visibility:"GREEN", reason:"full_visibility", status_color:"🟢"}
      end
    ),
    details: {
      systemconfig: $s,
      portal: $p,
      bridge: $b,
      nitro: $n
    }
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
cp "$OUT" "$SITE_OUT"

echo "$TS UNIFIED_MESH_BUILT_WITH_BRIDGE $OUT -> $SITE_OUT"
jq '.spine, .global' "$OUT"
