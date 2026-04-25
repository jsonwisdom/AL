#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/base/base_trust_surface_mesh.json"
LOG="_truth/logs/base_trust_surface_mesh.log"
TS="$(date -u +%FT%TZ)"

NITRO="_truth/base/nitro_observer_feed.json"
SYSTEMCONFIG="_truth/base/systemconfig_observer_feed.json"
PORTAL="_truth/base/optimismportal_observer_feed.json"

mkdir -p _truth/base _truth/logs

jq -n \
  --arg ts "$TS" \
  --slurpfile nitro "$NITRO" \
  --slurpfile systemconfig "$SYSTEMCONFIG" \
  --slurpfile portal "$PORTAL" \
  '
  def vis($x):
    if $x == null then "MISSING"
    elif (($x.status | type) == "object") then ($x.status.visibility // "UNKNOWN")
    elif (($x.status | type) == "string") then $x.status
    else "UNKNOWN"
    end;

  ($nitro[0] // null) as $n |
  ($systemconfig[0] // null) as $s |
  ($portal[0] // null) as $p |
  ([vis($s), vis($p), vis($n)]) as $v |
  {
    mesh: "base_trust_surface",
    generated_at: $ts,
    spine: ["L1 SystemConfig", "L1 OptimismPortal", "L2 NitroEnclaveVerifier"],
    layers: {
      l1_config: $s,
      l1_portal: $p,
      l2_verifier: $n
    },
    layer_visibility: {
      systemconfig: vis($s),
      portal: vis($p),
      nitro: vis($n)
    },
    global_status:
      (
        if ($v | index("RED")) then
          {visibility:"RED", reason:"one_or_more_layers_red"}
        elif (($v | index("YELLOW")) or ($v | index("MISSING")) or ($v | index("UNKNOWN"))) then
          {visibility:"YELLOW", reason:"degraded_or_missing_visibility"}
        else
          {visibility:"GREEN", reason:"all_layers_green"}
        end
      )
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS MESH_EXPORTED $OUT" | tee -a "$LOG"
