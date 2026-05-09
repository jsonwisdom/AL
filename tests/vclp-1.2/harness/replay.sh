#!/usr/bin/env bash
# VCLP 1.2 Extraction Replay Harness
# Tests canonical extraction without verifying claims

set -euo pipefail

FIXTURE_DIR="tests/vclp-1.2/fixtures"
HASHES_FILE="tests/vclp-1.2/canonical_hashes.txt"

echo "=== VCLP 1.2 Extraction Replay ==="
echo "Goal: Lock canonical extraction behavior before verifier changes"
echo ""

# Define extraction function (to be replaced with actual implementation)
extract_text() {
    local file="$1"
    local media_type="$2"
    
    # Placeholder — actual implementation will use:
    # - cat for text/plain with LF normalization
    # - htmlq or pup for HTML with entity decode + whitespace collapse
    # - pdftotext for PDF (deferred)
    
    case "$media_type" in
        text/plain)
            # Normalize line endings to LF, strip BOM, replace invalid UTF-8
            cat "$file" | sed 's/\r$//' | iconv -f UTF-8 -t UTF-8//IGNORE 2>/dev/null || true
            ;;
        text/html)
            # Placeholder: just cat for now
            cat "$file"
            ;;
        *)
            echo "ERROR: Unsupported media_type: $media_type" >&2
            return 1
            ;;
    esac
}

# Generate canonical hashes
echo "Generating canonical hashes..."
echo "# VCLP 1.2 Canonical Extraction Hashes" > "$HASHES_FILE"
echo "# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" >> "$HASHES_FILE"
echo "" >> "$HASHES_FILE"

for media_dir in txt html; do
    for fixture in "$FIXTURE_DIR/$media_dir"/*; do
        if [ -f "$fixture" ]; then
            name=$(basename "$fixture")
            case "$media_dir" in
                txt) media_type="text/plain" ;;
                html) media_type="text/html" ;;
            esac
            
            # Extract canonical text
            canonical=$(extract_text "$fixture" "$media_type")
            
            # Hash it
            hash=$(printf "%s" "$canonical" | sha256sum | cut -d' ' -f1)
            
            echo "$media_type|$name|sha256:$hash" >> "$HASHES_FILE"
            echo "  $media_type/$name -> sha256:$hash"
        fi
    done
done

echo ""
echo "Canonical hashes written to: $HASHES_FILE"
echo ""
echo "Next steps:"
echo "  1. Implement actual extraction (htmlq, pdftotext, etc.)"
echo "  2. Verify hashes don't change across implementations"
echo "  3. Lock hashes in protocol spec"
echo "  4. Add verification to CI gate"
