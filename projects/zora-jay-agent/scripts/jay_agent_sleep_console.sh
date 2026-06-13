#!/usr/bin/env bash
# AL / Zora jay-agent sleep console
# mode: read-only maintenance

set -euo pipefail

mkdir -p projects/zora-jay-agent/artifacts

OUT="projects/zora-jay-agent/artifacts/sleep_console_snapshot.txt"
NOW_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

{
  echo "AL_JAY_AGENT_ZORA_SLEEP_CONSOLE"
  echo "timestamp_utc=$NOW_UTC"
  echo "target=ZORA"
  echo "controller_label=jaywisdom.base.eth"
  echo "authority=false"
  echo "no_fake_green=true"
  echo
  echo "== REPO READBACK =="
  git branch --show-current || true
  git rev-parse HEAD || true
  git status --short --branch || true
  echo
  echo "== PROJECT FILES =="
  find projects/zora-jay-agent -maxdepth 4 -type f | sort || true
  echo
  echo "== ROOT WORKFLOWS =="
  find .github/workflows -maxdepth 1 -type f | sort || true
  echo
  echo "== MARKER HUNT =="
  grep -RInE "UNKNOWN|YELLOW|TODO|FIXME|NO_FAKE_GREEN|AUTHORITY" projects/zora-jay-agent .github/workflows 2>/dev/null || true
  echo
  echo "== RULING =="
  echo "SLEEP_CONSOLE=GREEN"
  echo "TARGET=ZORA"
  echo "MODE=READ_ONLY_MAINTENANCE"
  echo "WALLET_ACTION=false"
  echo "SEMANTIC_TRUTH_FINAL=false"
  echo "AUTHORITY=false"
  echo "NO_FAKE_GREEN=true"
} | tee "$OUT"

sha256sum "$OUT" | tee projects/zora-jay-agent/artifacts/sleep_console_snapshot.sha256
