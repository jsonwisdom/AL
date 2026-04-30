#!/usr/bin/env bash
# ALMS Master Sync Helper
# Canonical preflight for Cloud Shell / local execution.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

REMOTE="${ALMS_REMOTE:-origin}"
BRANCH="${ALMS_BRANCH:-master}"

git fetch "$REMOTE"
git reset --hard "$REMOTE/$BRANCH"

echo "ALMS_SYNC_OK remote=$REMOTE branch=$BRANCH head=$(git rev-parse HEAD)"
