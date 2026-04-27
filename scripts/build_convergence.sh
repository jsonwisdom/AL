#!/usr/bin/env bash
set -euo pipefail

MIRROR_DIR="site/mirrors"
OUT="convergence.json"
TMP="$(mktemp)"

# Validate all mirror JSON silently
for f in "$MIRROR_DIR"/*.json; do
  jq . "$f" >/dev/null 2>&1 || { echo "INVALID_MIRROR $f"; exit 1; }
done

# Aggregate
if compgen -G "$MIRROR_DIR/*.json" > /dev/null 2>&1; then
  jq -s '
    {
      nodes: .,
      root_set: (map(.root_sha256) | unique),
      merkle_set: (map(.merkle_root) | unique),
      consensus: (
        (map(.root_sha256) | unique | length == 1)
        and
        (map(.merkle_root) | unique | length == 1)
      )
    }
  ' "$MIRROR_DIR"/*.json > "$TMP"
else
  jq -n '{
    nodes: [],
    root_set: [],
    merkle_set: [],
    consensus: false,
    reason: "no mirrors"
  }' > "$TMP"
fi

mv "$TMP" "$OUT"
echo "CONVERGENCE_BUILT $OUT"
