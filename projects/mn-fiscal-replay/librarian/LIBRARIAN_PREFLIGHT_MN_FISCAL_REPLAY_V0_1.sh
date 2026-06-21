#!/bin/bash
# LIBRARIAN_PREFLIGHT_MN_FISCAL_REPLAY_V0_1.sh
# Purpose: find existing MN lineage before asking the operator for anything.
# Doctrine: discovery before delegation / NO_FAKE_GREEN.

set -euo pipefail

OUT_DIR="projects/mn-fiscal-replay/librarian"
OUT_JSON="$OUT_DIR/MN_FISCAL_REPLAY_LIBRARIAN_PREFLIGHT_V0_1.json"
OUT_MD="$OUT_DIR/MN_FISCAL_REPLAY_LIBRARIAN_PREFLIGHT_V0_1.md"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

mkdir -p "$OUT_DIR"

echo "=== LIBRARIAN PREFLIGHT: MN FISCAL REPLAY ==="

find_or_empty() {
  local pattern="$1"
  find . -path "$pattern" -type f 2>/dev/null | sed 's#^\./##' | sort || true
}

SOURCE_MANIFESTS=$(find_or_empty "./_sources/MN_*/source_manifest.json")
SOURCE_TEXTS=$(find_or_empty "./_sources/MN_*/source.txt")
SOURCE_BINS=$(find_or_empty "./_sources/MN_*/source.bin")
REPLAY_RECEIPTS=$(find_or_empty "./projects/mn-fiscal-replay/replay/MN_*.replay.json")
ENRICHED_BASELINES=$(find_or_empty "./projects/mn-fiscal-replay/enriched/MN_*.enriched.json")
LIVE_FETCHES=$(find_or_empty "./projects/mn-fiscal-replay/live_fetch/*/*")
BOSS_BRE_ARTIFACTS=$(find_or_empty "./projects/mn-fiscal-replay/boss_bre/*")
FORENSIC_WORKERS=$(find_or_empty "./scripts/*forensic*")
LIBRARIAN_WORKERS=$(find_or_empty "./scripts/*librarian*")

python3 - "$OUT_JSON" "$TS" << 'PY'
import json, sys, subprocess
from pathlib import Path

out = Path(sys.argv[1])
ts = sys.argv[2]

def sh(cmd):
    return subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.splitlines()

def find(pattern):
    return sorted([p[2:] if p.startswith("./") else p for p in sh(f"find . -path '{pattern}' -type f")])

data = {
  "artifact": "MN_FISCAL_REPLAY_LIBRARIAN_PREFLIGHT_V0_1",
  "timestamp": ts,
  "status": "LIBRARIAN_PREFLIGHT_COMPLETE",
  "rule": "DISCOVERY_BEFORE_DELEGATION",
  "source_manifests": find("./_sources/MN_*/source_manifest.json"),
  "source_texts": find("./_sources/MN_*/source.txt"),
  "source_bins": find("./_sources/MN_*/source.bin"),
  "replay_receipts": find("./projects/mn-fiscal-replay/replay/MN_*.replay.json"),
  "enriched_baselines": find("./projects/mn-fiscal-replay/enriched/MN_*.enriched.json"),
  "live_fetch_artifacts": find("./projects/mn-fiscal-replay/live_fetch/*/*"),
  "boss_bre_artifacts": find("./projects/mn-fiscal-replay/boss_bre/*"),
  "forensic_workers": find("./scripts/*forensic*"),
  "librarian_workers": find("./scripts/*librarian*"),
  "next_best_target": "MN_002_FROM_EXISTING_SOURCE_MANIFEST",
  "operator_manual_file_search_required": False,
  "public_content_claim": "BLOCKED",
  "no_fake_green": True
}

out.write_text(json.dumps(data, indent=2) + "\n")
PY

python3 - "$OUT_JSON" "$OUT_MD" << 'PY'
import json, sys
from pathlib import Path

j = json.loads(Path(sys.argv[1]).read_text())
md = Path(sys.argv[2])

def section(title, items):
    lines = [f"## {title}", ""]
    if items:
        lines += [f"- `{x}`" for x in items[:80]]
        if len(items) > 80:
            lines.append(f"- ... truncated in markdown; full list in JSON. count={len(items)}")
    else:
        lines.append("- none found")
    lines.append("")
    return lines

lines = [
"# MN Fiscal Replay Librarian Preflight v0.1",
"",
"`DISCOVERY_BEFORE_DELEGATION`",
"",
"## Ruling",
"",
"Do not ask the operator to find a source file until the Librarian has searched existing repo lineage.",
"",
f"- Status: `{j['status']}`",
f"- Next best target: `{j['next_best_target']}`",
f"- Manual file search required: `{j['operator_manual_file_search_required']}`",
f"- Public content claim: `{j['public_content_claim']}`",
f"- NO_FAKE_GREEN: `{j['no_fake_green']}`",
"",
]

lines += section("Source Manifests", j["source_manifests"])
lines += section("Replay Receipts", j["replay_receipts"])
lines += section("Enriched Baselines", j["enriched_baselines"])
lines += section("Live Fetch Artifacts", j["live_fetch_artifacts"])
lines += section("Boss Bre Artifacts", j["boss_bre_artifacts"])
lines += section("Workers", j["forensic_workers"] + j["librarian_workers"])

md.write_text("\n".join(lines) + "\n")
PY

cat "$OUT_JSON" | jq .
echo ""
echo "=== WROTE ==="
ls -la "$OUT_JSON" "$OUT_MD"
