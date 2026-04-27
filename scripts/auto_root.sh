#!/usr/bin/env bash
set -euo pipefail

# === VALIDATE JSONL FIRST ===
./scripts/validate_jsonl.sh

LOG="_truth/logs/execution.log"
mkdir -p _truth/logs

echo "$(date -u +%FT%TZ) RUN auto_root.sh from $(pwd)" >> "$LOG"

PRE_SNAP=$(mktemp)
POST_SNAP=$(mktemp)

# === SNAPSHOT PRE ===
find _truth -type f | sort > "$PRE_SNAP"

# === HASH PRE ===
if [ -f "_truth/root/alms_root.json" ]; then
  HASH_PRE=$(sha256sum _truth/root/alms_root.json | awk '{print $1}')
else
  HASH_PRE="NONE"
fi

# === BUILD ROOT ===
./scripts/build_alms_root.sh

# === SNAPSHOT POST ===
find _truth -type f | sort > "$POST_SNAP"

# === HASH POST ===
HASH_POST=$(sha256sum _truth/root/alms_root.json | awk '{print $1}')

# === CLASSIFY CHANGE ===
CHANGE_TYPE="UNKNOWN"

if [ "$HASH_PRE" != "$HASH_POST" ]; then
  CHANGE_TYPE="ROOT_MUTATION"
elif ! diff "$PRE_SNAP" "$POST_SNAP" >/dev/null; then
  CHANGE_TYPE="FILESET_CHANGE"
else
  CHANGE_TYPE="NO_CHANGE"
fi

echo "CHANGE_TYPE=$CHANGE_TYPE"

# === LOG ROOT EVENT (JSONL SAFE) ===
ROOT_LOG="_truth/logs/root_events.jsonl"

jq -n -cS \
  --arg ts "$(date -u +%FT%TZ)" \
  --arg type "ROOT_EVENT" \
  --arg change "$CHANGE_TYPE" \
  --arg pre "$HASH_PRE" \
  --arg post "$HASH_POST" \
  '{
    ts:$ts,
    type:$type,
    change_type:$change,
    hash_pre:$pre,
    hash_post:$post
  }' >> "$ROOT_LOG"

# === RUN ESCALATION ===
if [ -f "./scripts/escalate_alerts.sh" ]; then
  ./scripts/escalate_alerts.sh
fi

# === BUILD TIMELINE (optional) ===
if [ -f "./scripts/build_timeline.sh" ]; then
  ./scripts/build_timeline.sh
fi

# === CLEANUP ===
rm -f "$PRE_SNAP" "$POST_SNAP"

# === COMMIT IF CHANGE ===
if [ "$CHANGE_TYPE" != "NO_CHANGE" ]; then
  git add \
    _truth/root/alms_root.json \
    _truth/logs/root_events.jsonl \
    _truth/alerts/alerts.jsonl 2>/dev/null || true

  if [ -f "_truth/timeline/timeline.json" ]; then
    git add _truth/timeline/timeline.json
  fi

  git commit -m "Auto-run: root + alerts + timeline"
  git pull --rebase origin master
  git push
fi

echo "AUTO_ROOT_COMPLETE"

# --- WRITE LAST RUN ---
./scripts/write_last_run.sh
cp _truth/status/last_run.json status.json
echo "STATUS_UPDATED"

