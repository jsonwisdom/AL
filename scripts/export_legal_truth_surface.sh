#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%FT%TZ)"
OUT="_truth/law/legal_truth_surface.json"

MANUAL="_truth/law/doj/manual_doj_receipts_feed.json"
INGESTOR="_truth/law/law_ingestor_feed.json"

jq -n \
  --arg ts "$TS" \
  --slurpfile manual "$MANUAL" \
  --slurpfile ingestor "$INGESTOR" \
  '
  def vis_manual($m):
    if $m == null then "YELLOW"
    elif ($m.status.visibility == "GREEN") then "GREEN"
    else "YELLOW"
    end;

  def vis_ingestor($i; lane):
    if $i == null then "YELLOW"
    else ($i.lanes[lane].status // "YELLOW")
    end;

  ($manual[0] // null) as $m |
  ($ingestor[0] // null) as $i |

  (vis_manual($m)) as $doj_status |
  (vis_ingestor($i; "cases")) as $cases_status |
  (vis_ingestor($i; "lawbooks")) as $law_status |

  ([$doj_status, $cases_status, $law_status]) as $v |

  {
    observer: "legal_truth_surface_v1",
    generated_at: $ts,
    spine: {
      doj_manual: $doj_status,
      cases: $cases_status,
      lawbooks: $law_status
    },
    global:
      if ($v | index("RED")) then
        {visibility:"RED", reason:"one_or_more_layers_red", status_color:"🔴"}
      elif ($v | index("YELLOW")) then
        {visibility:"YELLOW", reason:"degraded_or_missing_visibility", status_color:"🟡"}
      else
        {visibility:"GREEN", reason:"all_layers_green", status_color:"🟢"}
      end,
    details: {
      doj_manual: $m,
      ingestor: $i
    }
  }' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$TS LEGAL_TRUTH_SURFACE_BUILT $OUT"
jq '.spine, .global' "$OUT"
