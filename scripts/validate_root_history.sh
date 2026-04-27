#!/usr/bin/env bash
set -euo pipefail

jq -c . _truth/root_history/root_history.jsonl > /dev/null

echo "ROOT_HISTORY_VALID"
