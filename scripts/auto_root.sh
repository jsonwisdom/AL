#!/usr/bin/env bash
set -euo pipefail

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

# === OPTIONAL: LOG JSONL EVENT ===
EVENT_LOG="_truth/logs/root_events.jsonl"

jq -n \
  --arg ts "$(date -u +%FT%TZ)" \
  --arg type "$CHANGE_TYPE" \
  --arg pre "$HASH_PRE" \
  --arg post "$HASH_POST" \
  '{
    ts:$ts,
    change_type:$type,
    hash_pre:$pre,
    hash_post:$post
  }' >> "$EVENT_LOG"

# === CLEANUP ===
rm -f "$PRE_SNAP" "$POST_SNAP"

# === COMMIT IF ROOT CHANGED ===
if [ "$CHANGE_TYPE" = "ROOT_MUTATION" ]; then
  git add _truth/root/alms_root.json
  git commit -m "Auto-update ALMS root"
  git pull --rebase origin master
  git push
fi

echo "AUTO_ROOT_DONE"
