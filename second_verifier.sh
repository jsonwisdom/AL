#!/usr/bin/env bash
set -e

FREEZE="2835802fc42867853caad8cd98a6467655a57e56"
TAG="arcade-v1-sealed"

git fetch --tags origin

OBS_TAG="$(git rev-parse "$TAG")"
OBS_COMMIT="$(git rev-parse HEAD)"
OBS_TREE="$(git rev-parse HEAD^{tree})"

TEST_OUT="$(PYTHONPATH=. python3 tests/T01_T08_status_engine.py 2>&1)"
echo "$TEST_OUT" | grep "Passed: 8/8" >/dev/null

STATUS_OUT="$(git status --porcelain)"

cat > evidence.json <<EOF
{
  "schema_id": "ARCADE_SECOND_VERIFIER_EVIDENCE_V1",
  "freeze_point": "$FREEZE",
  "tag": "$TAG",
  "observed_tag_resolution": "$OBS_TAG",
  "observed_commit_hash": "$OBS_COMMIT",
  "observed_tree_hash": "$OBS_TREE",
  "test_pass": "8/8",
  "working_tree_clean": false,
  "git_status": $(printf '%s' "$STATUS_OUT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
}
EOF

cat evidence.json
