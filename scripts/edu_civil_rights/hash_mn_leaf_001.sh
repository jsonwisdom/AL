#!/usr/bin/env bash
set -euo pipefail

LEAF="_truth/edu_civil_rights/mn/MN_EDU_CIVIL_RIGHTS_001.leaf.json"

jq -S . "$LEAF" | \
  tr -d '\r' | \
  openssl dgst -sha256 | \
  sed 's/^.* //'