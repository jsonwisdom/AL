#!/usr/bin/env bash
# VCLP 1.2 HTML Extraction Replay Harness (Lab Code - Not Locked)
# Parser: html5lib 1.1, strict UTF-8, TAINTED on invalid/parse error

set -euo pipefail

FIXTURE_DIR="tests/vclp-1.2/fixtures/html"
HASHES_FILE="tests/vclp-1.2/canonical_hashes_html.txt"
EXTRACTOR="tests/vclp-1.2/extractors/html_canonicalize.py"

echo "=== VCLP 1.2 HTML Canonical Extraction (Lab - Unlocked) ==="
echo ""

if [ ! -f "$EXTRACTOR" ]; then
    echo "ERROR: Extractor not found: $EXTRACTOR"
    exit 1
fi

if ! python3 -c "import html5lib" 2>/dev/null; then
    echo "ERROR: html5lib not installed. Run: pip3 install html5lib==1.1"
    exit 1
fi

echo "# VCLP 1.2 HTML Canonical Extraction Hashes (Lab)" > "$HASHES_FILE"
echo "# Parser: html5lib 1.1" >> "$HASHES_FILE"
echo "# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" >> "$HASHES_FILE"
echo "# NOTE: These hashes are NOT frozen until replay is deterministic" >> "$HASHES_FILE"
echo "" >> "$HASHES_FILE"

failures=0
for fixture in "$FIXTURE_DIR"/*.html; do
    if [ ! -f "$fixture" ]; then
        continue
    fi
    
    name=$(basename "$fixture")
    output=$(python3 "$EXTRACTOR" "$fixture" 2>&1)
    hash_line=$(echo "$output" | grep -E '^sha256:[a-f0-9]{64}$' | head -1)
    status_line=$(echo "$output" | grep '^STATUS:' | sed 's/STATUS: //')
    
    if [ -n "$hash_line" ] && [ "$status_line" = "OK" ]; then
        echo "HTML|$name|$hash_line" >> "$HASHES_FILE"
        echo "  ✓ $name -> $hash_line"
    elif [[ "$status_line" =~ ^TAINTED ]]; then
        echo "HTML|$name|TAINTED" >> "$HASHES_FILE"
        echo "  ⚠ $name -> TAINTED ($status_line)"
    else
        echo "  ✗ $name -> FAILED (unexpected output: $status_line)"
        failures=$((failures + 1))
    fi
done

echo ""
if [ $failures -eq 0 ]; then
    echo "✅ All HTML fixtures processed (lab mode, not locked)."
    echo "📋 Hashes written to: $HASHES_FILE"
    exit 0
else
    echo "❌ $failures fixture(s) failed."
    exit 1
fi
