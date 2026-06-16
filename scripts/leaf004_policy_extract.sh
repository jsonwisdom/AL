#!/usr/bin/env bash
set -euo pipefail

PDF="stcloud_2026_governmental_funds_budget.pdf"
OUT="out.txt"
PAGES_DIR="pages"
LEAF="004"

EXPECTED_PDF_SHA256="ae7c557e1ac30c9ad08fc60609d6e40550740db429ac167e3a8a473acdb1770f"

echo "[0] VERIFY SOURCE PDF"
sha256sum "$PDF"
ACTUAL_PDF_SHA256="$(sha256sum "$PDF" | awk '{print $1}')"
if [ "$ACTUAL_PDF_SHA256" != "$EXPECTED_PDF_SHA256" ]; then
  echo "PDF_SHA256_FAIL expected=$EXPECTED_PDF_SHA256 actual=$ACTUAL_PDF_SHA256"
  exit 1
fi
file "$PDF"
wc -c "$PDF"

if ! command -v pdftotext >/dev/null 2>&1; then
  echo "pdftotext missing. Run: sudo apt-get update && sudo apt-get install -y poppler-utils"
  exit 1
fi

mkdir -p "$PAGES_DIR"

echo "[1] EXTRACT FULL TEXT"
pdftotext -layout -nopgbrk "$PDF" "$OUT"
sha256sum "$OUT"
wc -c "$OUT"

echo "[2] POLICY GREP HITS"
grep -n -i "fund balance policy" "$OUT" | head -20 || true
grep -n -i "general fund balance" "$OUT" | head -20 || true
grep -n -i "policy requires" "$OUT" | head -20 || true
grep -n -i "35%-50%" "$OUT" | head -20 || true
grep -n -i "35%" "$OUT" | head -20 || true
grep -n -i "50%" "$OUT" | head -20 || true

echo "[3] EXTRACT PAGE FILES"
rm -f "$PAGES_DIR"/page_*.txt
for p in $(seq 1 250); do
  pdftotext -layout -nopgbrk -f "$p" -l "$p" "$PDF" "$PAGES_DIR/page_$p.txt" 2>/dev/null || break
  if [ ! -s "$PAGES_DIR/page_$p.txt" ]; then
    rm -f "$PAGES_DIR/page_$p.txt"
    break
  fi
done

echo "[4] PAGE GREP HITS"
grep -Rni "fund balance policy" "$PAGES_DIR" | head -20 || true
grep -Rni "general fund balance" "$PAGES_DIR" | head -20 || true
grep -Rni "policy requires" "$PAGES_DIR" | head -20 || true
grep -Rni "35%-50%" "$PAGES_DIR" | head -20 || true
grep -Rni "35%" "$PAGES_DIR" | head -20 || true
grep -Rni "50%" "$PAGES_DIR" | head -20 || true

echo "[5] NEXT"
echo "Pick exact page(s) from PAGE GREP HITS, then run:"
echo "cat pages/page_XX.txt pages/page_YY.txt > stcloud_leaf004_zone.txt"
echo "sha256sum stcloud_leaf004_zone.txt"
echo "wc -c stcloud_leaf004_zone.txt"
echo "sed -n '1,160p' stcloud_leaf004_zone.txt"
