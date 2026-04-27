#!/usr/bin/env bash
set -euo pipefail

echo "→ rebuilding ALMS root"
./scripts/build_alms_root.sh

echo "→ committing root update"
git add _truth/root/alms_root.json

git diff --cached --quiet || git commit -m "Auto-update ALMS root"

git pull --rebase origin master
git push

echo "AUTO_ROOT_DONE"
