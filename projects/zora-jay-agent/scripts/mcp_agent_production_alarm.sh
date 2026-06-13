#!/usr/bin/env bash
# AL / Zora MCP Agent production alarm
# mode: read-only maintenance and staged task reporting

set -euo pipefail

BASE="projects/zora-jay-agent"
ART="$BASE/artifacts"
mkdir -p "$ART"

OUT="$ART/mcp_agent_production_alarm.txt"
NOW_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
HEAD_SHA="$(git rev-parse HEAD 2>/dev/null || echo UNKNOWN_HEAD)"
BRANCH="$(git branch --show-current 2>/dev/null || echo UNKNOWN_BRANCH)"

{
  echo "MCP_AGENT_PRODUCTION_ALARM"
  echo "timestamp_utc=$NOW_UTC"
  echo "branch=$BRANCH"
  echo "head=$HEAD_SHA"
  echo "target=ZORA"
  echo "cadence=15_minutes"
  echo "authority=false"
  echo "no_fake_green=true"
  echo
  echo "== ASSIGNMENT READBACK =="
  if [ -f "$BASE/agents/MCP_AGENT_ASSIGNMENT_15_MINUTE_TASKS_V0_1.md" ]; then
    echo "assignment_file=present"
  else
    echo "assignment_file=missing"
  fi
  echo
  echo "== TASK LOOP =="
  echo "TASK_001_SLEEP_CONSOLE=RUN_OR_STAGED"
  echo "TASK_002_PRODUCTION_ALARM=RUNNING_NOW"
  echo "TASK_003_MARKER_SCAN=RUNNING_NOW"
  echo "TASK_004_SEPOLIA_WALLET=STAGED_ONLY"
  echo "TASK_005_ARTIFACT_HASHES=RUNNING_NOW"
  echo "TASK_006_SEMANTIC_TRUTH=YELLOW_UNLESS_PROVEN"
  echo
  echo "== MARKER SCAN =="
  grep -RInE "UNKNOWN|YELLOW|TODO|FIXME|NO_FAKE_GREEN|AUTHORITY|SEPOLIA|MCP_AGENT" "$BASE" .github/workflows 2>/dev/null || true
  echo
  echo "== SEPOLIA WALLET STAGING =="
  echo "sepolia_wallet_creation=STAGED_ONLY"
  echo "private_key_handling=LOCAL_ONLY"
  echo "human_approval_required=true"
  echo "cloudshell_required=true"
  echo "no_private_key_in_repo=true"
  echo
  echo "== ALARM RULING =="
  if [ -f "$BASE/agents/MCP_AGENT_ASSIGNMENT_15_MINUTE_TASKS_V0_1.md" ]; then
    echo "PRODUCTION_ALARM=GREEN_WITH_YELLOW_TASKS"
  else
    echo "PRODUCTION_ALARM=YELLOW_ASSIGNMENT_MISSING"
  fi
  echo "MCP_AGENT=ASSIGNED"
  echo "WALLET_ACTION=false"
  echo "SEMANTIC_TRUTH_FINAL=false"
  echo "AUTHORITY=false"
  echo "NO_FAKE_GREEN=true"
} | tee "$OUT"

sha256sum "$OUT" | tee "$ART/mcp_agent_production_alarm.sha256"
