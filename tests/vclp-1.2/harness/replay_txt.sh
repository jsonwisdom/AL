#!/usr/bin/env bash
# VCLP 1.2 TXT Extraction Replay Harness
# Strict UTF-8, TAINTED on invalid, no replacements

set -euo pipefail

FIXTURE_DIR="tests/vclp-1.2/fixtures/txt"
HASHES_FILE="tests/vclp-1.2/canonical_hashes.txt"
EXTRACTOR="tests/vclp-1.2/extractors/txt_canonicalize.py"

echo "=== VCLP 1.2 TXT Canonical Extraction (Strict) ==="
echo ""

if [ ! -f "$EXTRACTOR" ]; then
    echo "ERROR: Extractor not found: $EXTRACTOR"
    exit 1
fi

echo "# VCLP 1.2 TXT Canonical Extraction Hashes" > "$HASHES_FILE"
echo "# Strict UTF-8, TAINTED on invalid" >> "$HASHES_FILE"
echo "# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" >> "$HASHES_FILE"
echo "" >> "$HASHES_FILE"

failures=0
for fixture in "$FIXTURE_DIR"/*.txt; do
    if [ ! -f "$fixture" ]; then
        continue
    fi
    
    name=$(basename "$fixture")
    output=$(python3 "$EXTRACTOR" "$fixture" 2>&1)
    hash_line=$(echo "$output" | grep -E '^sha256:[a-f0-9]{64}$' | head -1)
    status_line=$(echo "$output" | grep '^STATUS:' | sed 's/STATUS: //')
    
    if [ -n "$hash_line" ] && [ "$status_line" = "OK" ]; then
        echo "$name|$hash_line" >> "$HASHES_FILE"
        echo "  ✓ $name -> $hash_line"
    elif [ "$status_line" = "TAINTED: invalid UTF-8" ]; then
        echo "$name|TAINTED" >> "$HASHES_FILE"
        echo "  ⚠ $name -> TAINTED (invalid UTF-8)"
    else
        echo "  ✗ $name -> FAILED (unexpected output: $status_line)"
        failures=$((failures + 1))
    fi
done

echo ""
if [ $failures -eq 0 ]; then
    echo "✅ All TXT fixtures processed. Hashes frozen in $HASHES_FILE"
    exit 0
else
    echo "❌ $failures fixture(s) failed."
    exit 1
fi
