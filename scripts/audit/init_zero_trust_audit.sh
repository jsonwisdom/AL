#!/usr/bin/env bash
set -euo pipefail

mkdir -p _truth/audit scripts/audit

cat > _truth/audit/repo_map.json <<'JSON'
{
  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",
  "version": "001",
  "repo": "jsonwisdom/AL",
  "roots": [
    "contracts/",
    "docs/",
    "site/",
    "_truth/",
    "scripts/",
    ".github/workflows/"
  ],
  "status": "SCAFFOLDED"
}
JSON

cat > _truth/audit/truth_surface_inventory.json <<'JSON'
{
  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",
  "version": "001",
  "truth_surfaces": [
    "status.json",
    "_truth/status/last_run.json",
    "_truth/root_history/root_history.jsonl",
    "_truth/timeline/timeline.json",
    "_truth/alerts/alerts.jsonl",
    "docs/goblin-court/",
    "site/goblin-court/",
    "docs/goblin-court/case-005-forged-consensus/CASE_005_DOCKET.md",
    "_truth/goblin-court/case-005-forged-consensus/runner_payload.json",
    "_truth/goblin-court/case-005-forged-consensus/public_anchor.json",
    "site/goblin-court/case-004-green/index.html"
  ],
  "status": "SCAFFOLDED"
}
JSON

cat > _truth/audit/zero_trust_audit_manifest.json <<'JSON'
{
  "track": "ZERO_TRUST_GITHUB_DIRECT_REPO_AUDIT",
  "version": "001",
  "state": "LIVE",
  "gates": [
    "repo_map",
    "truth_surface_inventory",
    "replay_truth_surface",
    "consistency_check",
    "ghost_anchor_detector",
    "ci_gate"
  ],
  "policy": "repo_proves_itself_no_narration"
}
JSON

printf 'ZERO_TRUST_AUDIT_INIT_OK\n'
