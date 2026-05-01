#!/usr/bin/env bash
set -euo pipefail

# ALMS Anchor Verification Suite
# Verifies all leaves in AL/_truth/anchors/

ANCHOR_DIR="_truth/anchors"

if [ ! -d "$ANCHOR_DIR" ]; then
  echo "ANCHOR_DIR_MISSING path=$ANCHOR_DIR" >&2
  exit 1
fi

echo "--- STARTING ANCHOR VERIFICATION ---"

for leaf_dir in "$ANCHOR_DIR"/leaf*; do
    if [ -d "$leaf_dir" ]; then
        leaf_name=$(basename "$leaf_dir")
        echo "Checking $leaf_name..."
        
        payload="$leaf_dir/payload.b64"
        if [ -f "$payload" ]; then
            echo "  [DECODE] $payload"
            out_json="$leaf_dir/${leaf_name}_verified.json"
            base64 -d "$payload" > "$out_json"
            
            echo "  [VALIDATE] $out_json"
            if jq . "$out_json" > /dev/null 2>&1; then
                sha=$(sha256sum "$out_json" | awk '{print $1}')
                size=$(wc -c < "$out_json" | tr -d ' ')
                echo "  [OK] $leaf_name verified (sha=$sha, size=$size)"
            else
                echo "  [FAIL] $leaf_name JSON invalid" >&2
            fi
        else
            echo "  [SKIP] No payload.b64 found in $leaf_dir"
        fi
    fi
done

echo "--- VERIFICATION COMPLETE ---"
