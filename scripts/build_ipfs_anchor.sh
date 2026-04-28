#!/usr/bin/env bash
set -euo pipefail

MANIFEST="${MANIFEST:-docs/verified-claims.json}"
ANCHOR_OUT="${ANCHOR_OUT:-docs/ipfs-anchor.txt}"

command -v jq >/dev/null 2>&1 || { echo "ANCHOR_FAIL reason=missing_jq" >&2; exit 2; }
command -v sha256sum >/dev/null 2>&1 || { echo "ANCHOR_FAIL reason=missing_sha256sum" >&2; exit 2; }

test -f "$MANIFEST" || { echo "ANCHOR_FAIL reason=missing_manifest path=$MANIFEST" >&2; exit 1; }

root="$({
  jq -r '.claims[] | [.claim_id, .text_hash, .canonical_json] | @tsv' "$MANIFEST" | LC_ALL=C sort
} | sha256sum | awk '{print $1}')"

if command -v ipfs >/dev/null 2>&1; then
  cid="$(ipfs add -Q "$MANIFEST" 2>/dev/null || true)"
  [ -n "$cid" ] || cid="ipfs_unavailable"
else
  cid="ipfs_unavailable"
fi

mkdir -p "$(dirname "$ANCHOR_OUT")"
cat > "$ANCHOR_OUT" <<EOF
timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
manifest: $MANIFEST
root_method: sha256(sort(claim_id,text_hash,canonical_json))
merkle_root: sha256:$root
ipfs_cid: $cid
git_commit: $(git rev-parse HEAD 2>/dev/null || echo git_unavailable)
ens_phase_2: pending
EOF

echo "ANCHOR_OK out=$ANCHOR_OUT root=sha256:$root ipfs_cid=$cid"
