#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "ALMS_BROWSER_WORKFLOW_PLACEMENTS"
echo "docs/browser-wallet/METAMASK_WORKFLOW.md"
echo "docs/workflows/ALMS_HUMAN_RECEIPT_LOOP.md"
echo "docs/ens/ALMS_ENS_RECORDS.md"
echo "docs/alms-browser/index.html"
echo "docs/tools/README.md"
echo "_truth/browser/placement_manifest.json"
echo
cat _truth/browser/placement_manifest.json
