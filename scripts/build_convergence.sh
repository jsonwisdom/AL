#!/usr/bin/env bash
set -euo pipefail

MIRROR_DIR="site/mirrors"
OUT="convergence.json"
TMP="$(mktemp)"

# Validate all mirror JSON silently
for f in "$MIRROR_DIR"/*.json; do
  jq . "$f" >/dev/null 2>&1 || { echo "INVALID_MIRROR $f"; exit 1; }
done

# Load canonical truth
STATUS_ROOT=$(jq -r '.root_sha256' status.json)
STATUS_MERKLE=$(jq -r '.merkle_root' status.json)

# Aggregate with truth-based consensus
if compgen -G "$MIRROR_DIR/*.json" > /dev/null 2>&1; then
  jq -s \
    --arg root "$STATUS_ROOT" \
    --arg merkle "$STATUS_MERKLE" \
    '
    {
      nodes: .,
      canonical_root: $root,
      canonical_merkle: $merkle,
      root_set: (map(.root_sha256) | unique),
      merkle_set: (map(.merkle_root) | unique),
      matches_root: (map(.root_sha256 == $root)),
      matches_merkle: (map(.merkle_root == $merkle)),
      consensus: (
        (length > 0)
        and
        (map(.root_sha256 == $root) | all)
        and
        (map(.merkle_root == $merkle) | all)
      )
    }
    ' "$MIRROR_DIR"/*.json > "$TMP"
else
  jq -n '{
    nodes: [],
    canonical_root: "",
    canonical_merkle: "",
    root_set: [],
    merkle_set: [],
    matches_root: [],
    matches_merkle: [],
    consensus: false,
    reason: "no mirrors"
  }' > "$TMP"
fi

mv "$TMP" "$OUT"
echo "CONVERGENCE_BUILT $OUT"
